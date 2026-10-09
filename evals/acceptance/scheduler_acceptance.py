"""Evaluator-owned acceptance checks for the `scheduler` fixture (eval id 9).

Usage: python -I scheduler_acceptance.py <candidate copy> <pristine fixture>

Expected values were produced by an independent brute-force oracle (scan every UTC minute and apply
docs/schedule.md literally) and cross-checked against the 2026 tz transitions of each zone. The pristine
tests are also run against the candidate code. Executes candidate code: sandbox only.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound; a correct implementation answers all cases in well under a second.
TIMEOUT_SECONDS = 120

CASES = [
    ("Berlin spring-forward: run when clocks jump", "Europe/Berlin", "02:30", "2026-03-28T12:00:00+01:00", "2026-03-29T03:00:00+02:00"),
    ("Berlin: after the jump run, next day", "Europe/Berlin", "02:30", "2026-03-29T03:00:00+02:00", "2026-03-30T02:30:00+02:00"),
    ("Berlin: after exactly the jump instant (UTC input)", "Europe/Berlin", "02:30", "2026-03-29T01:00:00+00:00", "2026-03-30T02:30:00+02:00"),
    ("Berlin: just before the jump, input in Tokyo time", "Europe/Berlin", "02:30", "2026-03-29T09:59:00+09:00", "2026-03-29T03:00:00+02:00"),
    ("Berlin fall-back: first occurrence", "Europe/Berlin", "02:30", "2026-10-24T12:00:00+02:00", "2026-10-25T02:30:00+02:00"),
    ("Berlin fall-back: no second run after the first", "Europe/Berlin", "02:30", "2026-10-25T02:30:00+02:00", "2026-10-26T02:30:00+01:00"),
    ("Berlin fall-back: between the two occurrences (UTC input)", "Europe/Berlin", "02:30", "2026-10-25T00:45:00+00:00", "2026-10-26T02:30:00+01:00"),
    ("Berlin fall-back: during the repeated hour", "Europe/Berlin", "02:30", "2026-10-25T02:15:00+01:00", "2026-10-26T02:30:00+01:00"),
    ("Berlin normal day, UTC input", "Europe/Berlin", "02:30", "2026-06-01T00:10:00+00:00", "2026-06-01T02:30:00+02:00"),
    ("New York spring-forward", "America/New_York", "02:30", "2026-03-07T12:00:00-05:00", "2026-03-08T03:00:00-04:00"),
    ("Lord Howe 30-minute spring-forward", "Australia/Lord_Howe", "02:15", "2026-10-03T12:00:00+10:30", "2026-10-04T02:30:00+11:00"),
    ("Lord Howe 30-minute fall-back: first occurrence", "Australia/Lord_Howe", "01:45", "2026-04-04T12:00:00+11:00", "2026-04-05T01:45:00+11:00"),
    ("Lord Howe fall-back: no second run", "Australia/Lord_Howe", "01:45", "2026-04-05T01:45:00+11:00", "2026-04-06T01:45:00+10:30"),
    ("Santiago midnight spring-forward", "America/Santiago", "00:30", "2026-09-05T12:00:00-04:00", "2026-09-06T01:00:00-03:00"),
    ("Santiago midnight fall-back: first occurrence", "America/Santiago", "23:30", "2026-04-04T12:00:00-03:00", "2026-04-04T23:30:00-03:00"),
    ("Santiago fall-back: no second run", "America/Santiago", "23:30", "2026-04-04T23:30:00-03:00", "2026-04-05T23:30:00-04:00"),
    ("Santiago fall-back: during the repeated hour", "America/Santiago", "23:30", "2026-04-04T23:45:00-04:00", "2026-04-05T23:30:00-04:00"),
]

PROBE = r"""
import json, sys
from datetime import datetime
sys.path.insert(0, sys.argv[1])
from scheduler.core import next_run
out = []
for tz, at, after in json.loads(sys.argv[2]):
    try:
        out.append(next_run({"at": at, "tz": tz}, datetime.fromisoformat(after)).isoformat())
    except Exception as exc:
        out.append(f"{type(exc).__name__}: {exc}"[:120])
print(json.dumps(out))
"""


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    inputs = [[tz, at, after] for _, tz, at, after, _ in CASES]
    proc = subprocess.run([sys.executable, "-B", "-c", PROBE, str(root), json.dumps(inputs)], capture_output=True,
                          text=True, timeout=TIMEOUT_SECONDS, env=env)
    try:
        got = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        got = [proc.stderr[-120:]] * len(CASES)
    for (name, _, _, _, expected), value in zip(CASES, got):
        check(f"{name}: {expected}", value == expected, value)
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe"
        shutil.copytree(root, probe, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.rmtree(probe / "tests")
        shutil.copytree(pristine / "tests", probe / "tests")
        proc = subprocess.run([sys.executable, "-B", "run_tests.py"], cwd=probe, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
        check("original tests pass against the candidate code", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    proc = subprocess.run([sys.executable, "-B", "run_tests.py"], cwd=root, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
    check("candidate's own suite passes", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
