"""Audit a normalized, runner-recorded step trace; never execute it.

This checks ordering and recorded preconditions only. It does not authenticate
receipts, judge source relevance, measure task success, or intercept tools.
See evals/README.md for the deliberately narrow trace format and trust boundary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

LEVELS = ("L0", "L1", "L2", "L3")
DEFAULT_LEVEL = "L2"
# Large enough for long real traces, small enough to refuse accidental multi-GB inputs.
MAX_INPUT_CHARS = 5_000_000


class TraceError(ValueError):
    """An unsupported or inconsistent trace record."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TraceError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def names(value: Any, *, empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (empty or bool(value))
        and all(text(item) for item in value)
        and len(set(value)) == len(value)
    )


def revisions(value: Any, *, empty: bool = False) -> bool:
    return (
        isinstance(value, dict)
        and (empty or bool(value))
        and all(text(key) and text(rev) for key, rev in value.items())
    )


class Auditor:
    def __init__(self) -> None:
        self.completed: dict[str, str] = {}
        self.active: dict[str, Any] | None = None
        self.verified_docs: set[tuple[str, str]] = set()  # (source, revision) read earlier in the task
        self.failed_targets: set[str] = set()
        self.superseded: dict[str, set[str]] = {}  # target -> revisions replaced by recorded mutations
        self.mutations = 0
        self.last_seq = 0

    def begin(self, event: dict[str, Any], step: str) -> None:
        require(self.active is None, "previous step has not ended")
        require(step not in self.completed, "step identifiers cannot be reused")
        level = event.get("level", DEFAULT_LEVEL)
        require(level in LEVELS, "level must be L0, L1, L2 or L3")
        read_only = level == "L0"
        require(names(event.get("requirements")), "missing requirement IDs")
        require(names(event.get("targets"), empty=read_only), "missing bounded targets")
        require(names(event.get("checks"), empty=read_only), "missing planned check IDs")
        sources = event.get("sources")
        require(revisions(sources, empty=True), "missing source-to-version contract")
        if not sources:
            require(text(event.get("no_source_reason")), "empty sources need no_source_reason")
        if level == "L1":
            require(not set(event["targets"]) & self.failed_targets, "retry after a failure requires L2 or higher")
        if level == "L3":
            require(text(event.get("authorization")), "L3 step needs recorded authorization")
            require(text(event.get("recovery")), "L3 step needs a recovery plan")
        deps = event.get("depends_on", [])
        require(names(deps, empty=True), "invalid dependencies")
        require(all(dep in self.completed for dep in deps), "dependency has no recorded result")
        self.active = {
            "id": step, "level": level, "targets": set(event["targets"]),
            "checks": set(event["checks"]), "sources": sources, "dependencies": deps,
            "docs": set(), "reads": {}, "after": None, "inspected": False, "results": {},
        }

    def step_event(self, event: dict[str, Any], kind: Any) -> None:
        active = self.active
        assert active is not None
        if kind == "read_doc":
            require(active["after"] is None, "documentation read after mutation")
            source = event.get("source")
            require(text(source) and source in active["sources"], "unplanned source")
            require(event.get("revision") == active["sources"][source], "source version mismatch")
            require(event.get("complete") is True and text(event.get("section")), "incomplete source read")
            active["docs"].add(source)
        elif kind == "read_target":
            require(active["after"] is None, "pre-edit target read recorded after mutation")
            target = event.get("target")
            require(text(target) and target in active["targets"], "unplanned target")
            require(event.get("complete") is True and text(event.get("revision")), "incomplete target read")
            require(event["revision"] not in self.superseded.get(target, set()),
                    "stale target read: revision was replaced by an earlier mutation")
            active["reads"][target] = event["revision"]
        elif kind == "mutate":
            require(active["level"] != "L0", "L0 (read-only) step recorded a mutation")
            require(active["after"] is None, "start a fresh step before another mutation")
            require(all(self.completed[dep] == "PASS" for dep in active["dependencies"]), "failed prerequisite")
            if active["level"] == "L1":
                missing = {s for s in active["sources"] if s not in active["docs"]
                           and (s, active["sources"][s]) not in self.verified_docs}
                require(not missing, "L1 relies on a source not verified earlier at this version")
            else:
                require(active["docs"] == set(active["sources"]), "required documentation not re-read")
            before, after = event.get("before"), event.get("after")
            require(revisions(before) and revisions(after), "invalid before/after revisions")
            require(set(before) == set(after), "before/after target sets differ")
            require(set(before) <= active["targets"], "mutation exceeds target scope")
            require(all(active["reads"].get(p) == rev for p, rev in before.items()), "missing or stale target read")
            require(any(after[p] != rev for p, rev in before.items()), "recorded mutation made no change")
            active["after"] = after
            for path, rev in before.items():
                self.superseded.setdefault(path, set()).add(rev)
            self.mutations += 1
        elif kind == "inspect":
            require(active["after"] is not None, "inspection has no mutation")
            require(event.get("revisions") == active["after"], "inspection is not of the changed revision")
            active["inspected"] = True
        elif kind == "check":
            require(active["after"] is not None and active["inspected"], "check precedes change inspection")
            check_id = event.get("check")
            require(text(check_id) and check_id in active["checks"], "unplanned check")
            require(check_id not in active["results"], "duplicate check; record a new diagnostic step")
            require(event.get("revisions") == active["after"], "check covers a stale revision")
            status = event.get("status")
            require(status in ("PASS", "FAIL", "NOT RUN"), "invalid check status")
            if status == "PASS" and "test_count" in event:
                count = event["test_count"]
                require(type(count) is int and count > 0, "PASS with zero or invalid test count")
            if status == "PASS" and "exit_code" in event:
                require(type(event["exit_code"]) is int and event["exit_code"] == 0, "PASS contradicts exit code")
            active["results"][check_id] = status
        elif kind == "end":
            self.end(event)
        else:
            raise TraceError("unsupported event kind")

    def end(self, event: dict[str, Any]) -> None:
        active = self.active
        assert active is not None
        status = event.get("status")
        require(status in ("PASS", "FAIL", "BLOCKED"), "invalid step status")
        if status == "PASS":
            if active["level"] == "L0":
                require(bool(active["docs"] or active["reads"]), "read-only PASS without any recorded read")
            else:
                require(active["after"] is not None and active["inspected"], "PASS without inspected mutation")
                require(set(active["results"]) == active["checks"], "planned validation is missing")
                require(all(v == "PASS" for v in active["results"].values()), "PASS despite unpassed validation")
        else:
            require(text(event.get("reason")), "failed/blocked step needs a reason")
            if active["after"] is not None:
                require(active["inspected"], "changed state was never inspected")
        if status == "FAIL":
            self.failed_targets |= active["targets"]
        self.verified_docs |= {(s, active["sources"][s]) for s in active["docs"]}
        self.completed[active["id"]] = status
        self.active = None

    def event(self, event: Any) -> None:
        require(isinstance(event, dict), "event must be an object")
        seq = event.get("seq")
        require(type(seq) is int and seq > self.last_seq, "seq must strictly increase")
        self.last_seq = seq
        kind, step = event.get("kind"), event.get("step")
        require(text(step), "step must be a nonempty identifier")
        require(text(event.get("receipt")), "missing original runner/tool receipt")
        if kind == "begin":
            self.begin(event, step)
            return
        require(self.active is not None and self.active["id"] == step, "event has no matching active step")
        self.step_event(event, kind)


def audit(events: Any, *, all_errors: bool = False) -> dict[str, Any]:
    """Validate a trace. A successful audit is not task success.

    By default the audit stops at the first error. With all_errors, an invalid step is
    recorded as INVALID, its remaining events are skipped up to its `end`, and auditing
    resumes with the next step, so one run reports every independent violation.
    """
    auditor = Auditor()
    errors: list[str] = []
    skipping: str | None = None
    index = 0
    if not isinstance(events, list) or not events:
        errors.append("event 0: expected a nonempty event array")
        events = []
    for index, event in enumerate(events, 1):
        if skipping is not None:
            if isinstance(event, dict) and event.get("step") == skipping and event.get("kind") == "end":
                skipping = None
            continue
        try:
            auditor.event(event)
        except TraceError as exc:
            errors.append(f"event {index}: {exc}")
            if not all_errors:
                break
            step = event.get("step") if isinstance(event, dict) else None
            if auditor.active is not None:
                step = auditor.active["id"]
                auditor.active = None
            if text(step):
                auditor.completed.setdefault(step, "INVALID")
                if not (isinstance(event, dict) and event.get("kind") == "end"):
                    skipping = step
    if not errors or all_errors:
        if auditor.active is not None or skipping is not None:
            errors.append(f"event {index}: trace ended with an unfinished step")
        elif events and not auditor.completed:
            errors.append(f"event {index}: no closed steps")
    return {
        "process_compliant": not errors,
        "closed_steps": sum(1 for status in auditor.completed.values() if status != "INVALID"),
        "recorded_mutations": auditor.mutations,
        "errors": errors,
        "task_outcome": "NOT MEASURED",
        "receipt_authenticity": "NOT VERIFIED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="normalized JSON event array; read-only input")
    parser.add_argument("--all-errors", action="store_true", help="report every invalid step, not just the first")
    args = parser.parse_args()
    try:
        with args.trace.open("r", encoding="utf-8") as handle:
            raw = handle.read(MAX_INPUT_CHARS + 1)
        if len(raw) > MAX_INPUT_CHARS:
            raise ValueError(f"trace exceeds the {MAX_INPUT_CHARS:,}-character limit")
        report = audit(json.loads(raw), all_errors=args.all_errors)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(json.dumps({"input_error": str(exc), "task_outcome": "NOT MEASURED"}))
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["process_compliant"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
