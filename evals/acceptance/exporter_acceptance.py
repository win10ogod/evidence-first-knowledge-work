"""Evaluator-owned acceptance checks for the `exporter` fixture (eval id 1).

Usage: python -I exporter_acceptance.py <candidate copy of evals/fixtures/exporter>

This executes the candidate's code, so run it only inside the evaluation sandbox.
Keep this file outside the candidate's writable workspace. Expected values come from
the fixture's docs/formats.md, not from the candidate's implementation.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# The fixture ships with two tests; a collected new test must raise the count.
BASELINE_TEST_COUNT = 2
# Generous bound for a tiny CLI; a hang means the candidate broke something.
TIMEOUT_SECONDS = 60


def run(cwd, args, stdin=""):
    return subprocess.run([sys.executable, *args], cwd=cwd, input=stdin, capture_output=True,
                          text=True, encoding="utf-8", timeout=TIMEOUT_SECONDS)


def cli(cwd, fmt, records):
    return run(cwd, ["-m", "exporter.cli", "--format", fmt], json.dumps(records, ensure_ascii=False))


def main():
    root = Path(sys.argv[1]).resolve()
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    sample = [{"b": 1, "a": "é"}, {"x": None}]
    proc = cli(root, "lines", sample)
    check("lines: one sorted record per line, non-ASCII kept",
          proc.returncode == 0 and proc.stdout == '{"a": "é", "b": 1}\n{"x": null}\n', repr(proc.stdout or proc.stderr)[:200])
    proc = cli(root, "lines", [])
    check("lines: empty input produces empty output", proc.returncode == 0 and proc.stdout == "", repr(proc.stdout or proc.stderr)[:200])
    proc = cli(root, "json", [{"b": 1, "a": 2}])
    check("json output unchanged", proc.returncode == 0 and proc.stdout == '[\n  {\n    "a": 2,\n    "b": 1\n  }\n]\n', repr(proc.stdout)[:200])
    proc = run(root, ["run_tests.py"])
    output = proc.stdout + proc.stderr
    ran = re.search(r"^Ran (\d+) tests?", output, re.MULTILINE)
    count = int(ran.group(1)) if ran else 0
    check("project test runner passes", proc.returncode == 0, output[-300:])
    check("a new test is actually collected by run_tests.py", count > BASELINE_TEST_COUNT, f"ran {count}")
    check("a collected test exercises the lines format", re.search(r"lines", output, re.IGNORECASE) is not None, "")
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
