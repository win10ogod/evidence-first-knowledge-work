"""Audit a normalized, runner-recorded file-mutation trace; never execute it.

This checks ordering and recorded preconditions only. It does not authenticate
receipts, judge source relevance, measure task success, or intercept tools.
See evals/README.md for the deliberately narrow trace format and trust boundary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


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


def revisions(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and bool(value)
        and all(text(key) and text(rev) for key, rev in value.items())
    )


def audit(events: Any) -> dict[str, Any]:
    """Fail at the first invalid event; successful audit is not task success."""
    completed: dict[str, str] = {}
    active: dict[str, Any] | None = None
    mutation_count = 0
    index = 0
    last_seq = 0
    errors: list[str] = []
    try:
        require(isinstance(events, list) and bool(events), "expected a nonempty event array")
        for index, event in enumerate(events, 1):
            require(isinstance(event, dict), "event must be an object")
            seq = event.get("seq")
            require(type(seq) is int and seq > last_seq, "seq must strictly increase")
            last_seq = seq
            kind, step = event.get("kind"), event.get("step")
            require(text(step), "step must be a nonempty identifier")
            require(text(event.get("receipt")), "missing original runner/tool receipt")
            if kind == "begin":
                require(active is None, "previous step has not ended")
                require(step not in completed, "step identifiers cannot be reused")
                require(names(event.get("requirements")), "missing requirement IDs")
                require(names(event.get("targets")), "missing bounded targets")
                require(names(event.get("checks")), "missing planned check IDs")
                require(revisions(event.get("sources")), "missing source-to-version contract")
                deps = event.get("depends_on", [])
                require(names(deps, empty=True), "invalid dependencies")
                require(all(dep in completed for dep in deps), "dependency has no recorded result")
                active = {
                    "id": step, "targets": set(event["targets"]),
                    "checks": set(event["checks"]), "sources": event["sources"],
                    "dependencies": deps, "docs": set(), "reads": {},
                    "after": None, "inspected": False, "results": {},
                }
                continue
            require(active is not None and active["id"] == step, "event has no matching active step")
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
                active["reads"][target] = event["revision"]
            elif kind == "mutate":
                require(active["after"] is None, "start a fresh step before another mutation")
                require(all(completed[dep] == "PASS" for dep in active["dependencies"]), "failed prerequisite")
                require(active["docs"] == set(active["sources"]), "required documentation not re-read")
                before, after = event.get("before"), event.get("after")
                require(revisions(before) and revisions(after), "invalid before/after revisions")
                require(set(before) == set(after), "before/after target sets differ")
                require(set(before) <= active["targets"], "mutation exceeds target scope")
                require(all(active["reads"].get(p) == rev for p, rev in before.items()), "missing or stale target read")
                require(any(after[p] != rev for p, rev in before.items()), "recorded mutation made no change")
                active["after"] = after
                mutation_count += 1
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
                status = event.get("status")
                require(status in ("PASS", "FAIL", "BLOCKED"), "invalid step status")
                if status == "PASS":
                    require(active["after"] is not None and active["inspected"], "PASS without inspected mutation")
                    require(set(active["results"]) == active["checks"], "planned validation is missing")
                    require(all(v == "PASS" for v in active["results"].values()), "PASS despite unpassed validation")
                else:
                    require(text(event.get("reason")), "failed/blocked step needs a reason")
                    if active["after"] is not None:
                        require(active["inspected"], "changed state was never inspected")
                completed[step] = status
                active = None
            else:
                raise TraceError("unsupported event kind")
        require(active is None, "trace ended with an unfinished step")
        require(bool(completed), "no closed steps")
    except TraceError as exc:
        errors.append(f"event {index}: {exc}")
    return {
        "process_compliant": not errors,
        "closed_steps": len(completed),
        "recorded_mutations": mutation_count,
        "errors": errors,
        "task_outcome": "NOT MEASURED",
        "receipt_authenticity": "NOT VERIFIED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="normalized JSON event array; read-only input")
    args = parser.parse_args()
    try:
        with args.trace.open("r", encoding="utf-8") as handle:
            raw = handle.read(5_000_001)
        if len(raw) > 5_000_000:
            raise ValueError("trace exceeds the 5,000,000-character limit")
        report = audit(json.loads(raw))
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(json.dumps({"input_error": str(exc), "task_outcome": "NOT MEASURED"}))
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["process_compliant"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
