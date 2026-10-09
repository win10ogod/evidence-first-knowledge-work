#!/usr/bin/env python3
"""Claude Code PostToolUse hook: flag test runs that selected zero relevant tests.

Reads the hook payload from stdin. When a Bash result contains a zero-selection
signal (no tests collected, all deselected or skipped, "running 0 tests", ...),
it adds context telling Claude the run is not validation. It never blocks, never
rewrites tool output and always exits 0, so a parsing problem cannot disrupt work.

Signals were taken from real output of Python 3.13 unittest, pytest 9.1, Jest 29.7,
Vitest 2.1, Go 1.24 and Cargo 1.97; other versions may word them differently.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

# Truncate echoed commands so the injected context stays short.
MAX_COMMAND_CHARS = 120

SIMPLE_SIGNALS = [
    (re.compile(r"\bRan 0 tests\b"), "unittest ran 0 tests"),
    (re.compile(r"\bno tests ran\b", re.IGNORECASE), "no tests ran"),
    (re.compile(r"\bNo tests found\b"), "Jest found no tests"),
    (re.compile(r"\bNo test files found\b"), "Vitest found no test files"),
    (re.compile(r"\[no tests to run\]|testing: warning: no tests to run"), "go test filter matched no tests"),
]
PYTEST_SUMMARY = re.compile(r"^=+ (?P<body>.+?) in [\d.]+s(?: \([^)]*\))? =+$", re.MULTILINE)
JEST_SUMMARY = re.compile(r"^Tests:\s+(?P<body>.+)$", re.MULTILINE)
CARGO_RUNNING = re.compile(r"^running (\d+) tests?$", re.MULTILINE)
GO_NO_FILES = re.compile(r"\[no test files\]")
GO_RAN = re.compile(r"^(ok|FAIL|--- )", re.MULTILINE)
EXECUTED_WORDS = ("passed", "failed", "error")


def zero_test_signals(text: str) -> list[str]:
    """Return human-readable reasons why this output shows no relevant test executed."""
    found = [label for pattern, label in SIMPLE_SIGNALS if pattern.search(text)]
    for match in PYTEST_SUMMARY.finditer(text):
        body = match.group("body")
        if any(word in body for word in ("deselected", "skipped")) and not any(w in body for w in EXECUTED_WORDS):
            found.append(f"pytest executed nothing: '{body}'")
    for match in JEST_SUMMARY.finditer(text):
        body = match.group("body")
        if not any(word in body for word in EXECUTED_WORDS):
            found.append(f"Jest executed nothing: '{body}'")
    counts = [int(n) for n in CARGO_RUNNING.findall(text)]
    if counts and not any(counts):
        found.append("cargo ran 0 tests in every target")
    if GO_NO_FILES.search(text) and not GO_RAN.search(text):
        found.append("go test found no test files")
    return list(dict.fromkeys(found))


def build_context(payload: dict[str, Any]) -> str | None:
    if payload.get("tool_name") != "Bash":
        return None
    response = payload.get("tool_response")
    if not isinstance(response, dict):
        return None
    text = "\n".join(str(response.get(key) or "") for key in ("stdout", "stderr"))
    signals = zero_test_signals(text)
    if not signals:
        return None
    command = str((payload.get("tool_input") or {}).get("command", ""))[:MAX_COMMAND_CHARS]
    return (
        f"Zero-test signal in `{command}`: {'; '.join(signals)}. "
        "This run does not validate the change. Confirm the relevant tests were selected "
        "(list or verbose mode, check the new test's name) and report this check as NOT RUN "
        "or FAIL, not PASS."
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    context = build_context(payload) if isinstance(payload, dict) else None
    if context:
        json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
