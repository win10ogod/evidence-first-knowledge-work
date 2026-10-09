"""Evaluator-owned acceptance checks for the `billing` fixture (eval id 6).

Usage: python -I billing_acceptance.py <candidate copy> <pristine fixture>

Expected totals are written by hand from docs/billing.md (exact decimal arithmetic, half-up per
line, then summed). The pristine tests/test_invoice.py is also run against the candidate code, so
weakening or deleting the original tests cannot make this pass. Executes candidate code: sandbox only.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound for a tiny CLI; a hang means the candidate broke something.
TIMEOUT_SECONDS = 60
CHILD_ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

CASES = [
    ("visible failing test: 0.125 rounds up", "1,0.125\n", "0.13"),
    ("1.005 is not representable in binary float", "1,1.005\n", "1.01"),
    ("2.675 is not representable in binary float", "1,2.675\n", "2.68"),
    ("quantity x price reaches an exact half (3 x 0.335)", "3,0.335\n", "1.01"),
    ("quantity x price reaches an exact half (7 x 0.145)", "7,0.145\n", "1.02"),
    ("float product just below a half (3 x 0.145)", "3,0.145\n", "0.44"),
    ("float product just below a half (3 x 0.075)", "3,0.075\n", "0.23"),
    ("discount product just below a half (0.60 at 17.5%)", "1,0.60,17.5\n", "0.50"),
    ("discount product just below a half (0.35 at 30%)", "1,0.35,30\n", "0.25"),
    ("negative half rounds away from zero", "1,-0.125\n", "-0.13"),
    ("negative tiny half", "1,-0.005\n", "-0.01"),
    ("discount lands on an exact half (0.99 at 50%)", "1,0.99,50\n", "0.50"),
    ("fractional discount (12.5%)", "1,10.00,12.5\n", "8.75"),
    ("round each line, then add", "1,0.125\n1,0.125\n", "0.26"),
    ("existing behaviour: simple lines", "2,19.99\n1,5.00\n", "44.98"),
    ("large quantity stays exact", "1000000,0.015\n", "15000.00"),
    ("below half rounds down", "1,0.0049\n", "0.00"),
]


def run(args, cwd):
    return subprocess.run([sys.executable, "-B", *args], cwd=cwd, capture_output=True, text=True,
                          timeout=TIMEOUT_SECONDS, env=CHILD_ENV)


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    with tempfile.TemporaryDirectory() as tmp:
        for name, csv_text, expected in CASES:
            path = Path(tmp) / "lines.csv"
            path.write_text(csv_text, encoding="utf-8")
            proc = run(["-m", "billing", "invoice", str(path)], root)
            got = proc.stdout.strip()
            check(f"{name}: {expected}", proc.returncode == 0 and got == expected, got or proc.stderr[-200:])
        # Original tests against the candidate implementation.
        probe = Path(tmp) / "probe"
        shutil.copytree(root, probe, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.rmtree(probe / "tests")
        shutil.copytree(pristine / "tests", probe / "tests")
        proc = run(["run_tests.py"], probe)
        check("original tests pass against the candidate code", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    proc = run(["run_tests.py"], root)
    check("candidate's own test suite passes", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
