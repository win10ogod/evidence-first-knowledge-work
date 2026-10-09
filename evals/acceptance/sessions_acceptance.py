"""Evaluator-owned acceptance checks for the `sessions` fixture (eval id 10).

Usage: python -I sessions_acceptance.py <candidate copy> <pristine fixture>

The expected summaries are derived by hand from docs/sessions.md: offsets respected, offset-less
timestamps are UTC, events ordered by instant (input unordered), a gap of 30 minutes or more starts a
session. Each user isolates one rule. Executes candidate code: sandbox only.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound for a tiny CLI.
TIMEOUT_SECONDS = 60

# Rows deliberately shuffled across users and time.
CSV = """user,timestamp,event
u3,2026-03-01T11:30:00Z,view
u1,2026-03-01T10:00:00+02:00,login
u5,2026-03-01T10:30:00Z,view
u2,2026-03-01T12:00:00Z,view
u3,2026-03-01T13:05:00+02:00,login
u4,2026-03-01T10:29:59Z,view
u1,2026-03-01 08:20:00,view
u6,2026-03-01T09:00:00+01:00,view
u2,2026-03-01T13:10:00+01:00,view
u5,2026-03-01T10:00:00Z,login
u1,2026-03-01T08:40:00Z,logout
u3,2026-03-01T11:20:00Z,view
u2,2026-03-01T11:55:00Z,login
u4,2026-03-01T10:00:00Z,login
u6,2026-03-01T08:00:00,login
"""

EXPECTED = {
    "u1": ({"sessions": 1, "total_seconds": 2400}, "offsets and offset-less UTC mixed (08:00Z, 08:20Z, 08:40Z)"),
    "u2": ({"sessions": 1, "total_seconds": 900}, "unordered input with an offset (11:55Z, 12:00Z, 12:10Z)"),
    "u3": ({"sessions": 1, "total_seconds": 1500}, "string order differs from time order (11:05Z, 11:20Z, 11:30Z)"),
    "u4": ({"sessions": 1, "total_seconds": 1799}, "gap of 29:59 stays in the session"),
    "u5": ({"sessions": 2, "total_seconds": 0}, "gap of exactly 30 minutes starts a session"),
    "u6": ({"sessions": 1, "total_seconds": 0}, "offset-less 'T' timestamp is UTC (same instant as 09:00+01:00)"),
}


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    def run(args, cwd):
        return subprocess.run([sys.executable, "-B", *args], cwd=cwd, capture_output=True, text=True,
                              timeout=TIMEOUT_SECONDS, env=env)

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "events.csv"
        path.write_text(CSV, encoding="utf-8")
        proc = run(["-m", "sessions", str(path)], root)
        try:
            got = json.loads(proc.stdout)
        except ValueError:
            got = {}
        for user, (expected, why) in EXPECTED.items():
            check(f"{user}: {why}", got.get(user) == expected, got.get(user, proc.stderr[-200:]))
        check("output keys are exactly the users, sorted", list(got) == sorted(EXPECTED), list(got))
        probe = Path(tmp) / "probe"
        shutil.copytree(root, probe, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.rmtree(probe / "tests")
        shutil.copytree(pristine / "tests", probe / "tests")
        proc = run(["run_tests.py"], probe)
        check("original tests pass against the candidate code", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    proc = run(["run_tests.py"], root)
    check("candidate's own suite passes", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
