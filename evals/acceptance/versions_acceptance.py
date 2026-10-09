"""Evaluator-owned acceptance checks for the `versions` fixture (eval id 12).

Usage: python -I versions_acceptance.py <candidate copy> <pristine fixture>

Every expected answer was produced by npm's own `semver` package (7.6.0, `semver.satisfies`) and agrees
with docs/ranges.md: 77 named cases grouped by rule, plus a differential grid of 29 versions x 27 ranges
whose answers are packed into GRID_BITS (one bit per range-major pair, 1 = satisfies). Executes candidate
code: sandbox only.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound; a few hundred calls to a pure function.
TIMEOUT_SECONDS = 60

CASES = [
    ('caret', '0.2.9', '^0.2.3', True),
    ('caret', '0.3.0', '^0.2.3', False),
    ('caret', '0.0.3', '^0.0.3', True),
    ('caret', '0.0.4', '^0.0.3', False),
    ('caret', '1.9.9', '^1.2.3', True),
    ('caret', '2.0.0', '^1.2.3', False),
    ('caret', '1.2.2', '^1.2.3', False),
    ('caret', '0.0.9', '^0.0.x', True),
    ('caret', '0.1.0', '^0.0.x', False),
    ('caret', '0.0.5', '^0.0', True),
    ('caret', '0.1.0', '^0.0', False),
    ('caret', '0.9.9', '^0.x', True),
    ('caret', '1.0.0', '^0.x', False),
    ('caret', '0.5.0', '^0', True),
    ('caret', '1.0.0', '^0', False),
    ('caret', '1.9.0', '^1.x', True),
    ('caret', '2.0.0', '^1', False),
    ('caret', '1.3.0', '^1.2.x', True),
    ('caret', '1.1.9', '^1.2.x', False),
    ('tilde', '1.2.9', '~1.2.3', True),
    ('tilde', '1.3.0', '~1.2.3', False),
    ('tilde', '1.2.0', '~1.2', True),
    ('tilde', '1.3.0', '~1.2', False),
    ('tilde', '1.9.0', '~1', True),
    ('tilde', '2.0.0', '~1', False),
    ('tilde', '0.2.5', '~0.2.3', True),
    ('tilde', '0.3.0', '~0.2.3', False),
    ('xrange', '1.9.9', '1.x', True),
    ('xrange', '2.0.0', '1.x', False),
    ('xrange', '1.2.7', '1.2.x', True),
    ('xrange', '1.3.0', '1.2.X', False),
    ('xrange', '1.2.7', '1.2', True),
    ('xrange', '1.5.0', '1', True),
    ('xrange', '3.0.0', '*', True),
    ('xrange', '0.0.1', '', True),
    ('xrange', '1.2.4', '1.2.*', True),
    ('hyphen', '1.2.3', '1.2.3 - 2.3.4', True),
    ('hyphen', '2.3.4', '1.2.3 - 2.3.4', True),
    ('hyphen', '2.3.5', '1.2.3 - 2.3.4', False),
    ('hyphen', '1.2.0', '1.2 - 2.3.4', True),
    ('hyphen', '2.3.9', '1.2.3 - 2.3', True),
    ('hyphen', '2.4.0', '1.2.3 - 2.3', False),
    ('hyphen', '2.9.9', '1.2.3 - 2', True),
    ('hyphen', '3.0.0', '1.2.3 - 2', False),
    ('order', '1.0.0', '>1.0.0-rc.1', True),
    ('order', '1.0.0-beta.11', '>1.0.0-beta.2', True),
    ('order', '1.0.0-beta.2', '>1.0.0-beta.11', False),
    ('order', '1.0.0-alpha.beta', '>1.0.0-alpha.1', True),
    ('order', '1.0.0-alpha.1', '>1.0.0-alpha', True),
    ('order', '1.0.0-beta', '>1.0.0-alpha.beta', True),
    ('order', '1.0.0-rc.1', '<1.0.0', False),
    ('order', '1.0.0-alpha.1', '>1.0.0-alpha.beta', False),
    ('order', '1.0.0-rc.1', '>=1.0.0-rc.1 <=1.0.0-rc.1', True),
    ('prerelease', '1.2.3-alpha.7', '>1.2.3-alpha.3', True),
    ('prerelease', '3.4.5-alpha.9', '>1.2.3-alpha.3', False),
    ('prerelease', '1.2.4-beta.1', '^1.2.3', False),
    ('prerelease', '1.2.3-beta.4', '^1.2.3-beta.2', True),
    ('prerelease', '1.2.4-beta.4', '^1.2.3-beta.2', False),
    ('prerelease', '1.2.4', '^1.2.3-beta.2', True),
    ('prerelease', '2.0.0-rc.1', '^1.2.3', False),
    ('prerelease', '1.2.3-rc.1', '*', False),
    ('prerelease', '1.3.0-beta', '>=1.2.0 <1.4.0', False),
    ('prerelease', '1.2.3-beta.3', '~1.2.3-beta.2', True),
    ('prerelease', '1.2.3-beta.1', '~1.2.3-beta.2', False),
    ('prerelease', '1.2.5-beta.3', '~1.2.3-beta.2', False),
    ('prerelease', '1.2.3-beta.3', '<1.0.0 || >=1.2.3-beta.1 <1.2.4', True),
    ('build', '1.2.3+build.5', '1.2.3', True),
    ('build', '1.2.3+a', '=1.2.3+b', True),
    ('build', '1.2.4+exp.sha.5114f85', '^1.2.3', True),
    ('build', '1.0.0-rc.1+b.7', '>=1.0.0-rc.1 <1.0.0', True),
    ('syntax', 'v1.2.3', '1.2.3', True),
    ('syntax', '1.2.3', '=v1.2.3', True),
    ('syntax', '1.2.3', '>= 1.2.3', True),
    ('syntax', '1.5.0', '>=1.2.3   <2.0.0', True),
    ('syntax', '4.0.0', '^1.0.0 || ^3.0.0 || >=4.0.0', True),
    ('syntax', '2.5.0', '^1.0.0||^3.0.0', False),
    ('syntax', '1.2.3', '=1.2.3', True),
]
GRID_VERSIONS = ["0.0.0", "0.0.3", "0.0.4", "0.1.0", "0.2.3", "0.2.9", "0.3.0", "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0", "1.2.0", "1.2.3-beta.2", "1.2.3-beta.10", "1.2.3", "1.2.4-rc.1", "1.2.9", "1.3.0-0", "1.3.0", "1.9.9+build.1", "2.0.0-rc.1", "2.0.0", "2.3.4", "2.3.5", "2.4.0", "3.0.0", "v3.1.0"]
GRID_RANGES = ["^0.2.3", "^0.0.3", "^0.0", "^0", "^1.2.3", "^1.2.3-beta.2", "^1.x", "~1.2.3", "~1.2", "~1", "~0.2.3", "~1.2.3-beta.2", "1.x", "1.2.x", "*", "1", "1.2.3 - 2.3.4", "1.2 - 2.3", "1.2.3 - 2", ">1.0.0-alpha <1.0.0", ">=1.0.0-beta.2 <1.0.0-rc.1", ">1.2.3-beta.2", "<=1.2.3", ">= 1.2.0 < 2.0.0", "^0.2.3 || ^2.0.0", "~1.2.3 || 3.x", "=1.0.0+meta"]
GRID_BITS = '0c00000200000038000001fc000000000ac00001d6000032b0000014000004a000006560030000000007400000cac000025003f832b7e00195800000ad8000256e00002b7801e000000600000000d6fff83200000095800c0001e0000500c0020000'

PROBE = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
from versions import satisfies
pairs = json.loads(sys.stdin.read())
out = []
for version, range_text in pairs:
    try:
        out.append(bool(satisfies(version, range_text)))
    except Exception as exc:
        out.append(f"{type(exc).__name__}: {exc}")
print(json.dumps(out))
"""


def grid_expected():
    bits = "".join(f"{int(c, 16):04b}" for c in GRID_BITS)
    pairs = [(v, r) for r in GRID_RANGES for v in GRID_VERSIONS]
    return pairs, [b == "1" for b in bits[:len(pairs)]]


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    def run(args, cwd, stdin=None):
        return subprocess.run([sys.executable, "-B", *args], cwd=cwd, input=stdin, capture_output=True, text=True,
                              timeout=TIMEOUT_SECONDS, env=env)

    grid_pairs, grid_want = grid_expected()
    pairs = [(v, r) for _, v, r, _ in CASES] + grid_pairs
    proc = run(["-c", PROBE, str(root)], root, json.dumps(pairs))
    try:
        got = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        got = [f"probe crashed: {proc.stderr[-200:]}"] * len(pairs)
    named, grid = got[:len(CASES)], got[len(CASES):]
    for category in dict.fromkeys(c[0] for c in CASES):
        wrong = [f"satisfies({v!r}, {r!r}) -> {g} (want {want})" for (cat, v, r, want), g in zip(CASES, named)
                 if cat == category and g is not want]
        total = sum(1 for c in CASES if c[0] == category)
        check(f"{category}: {total - len(wrong)}/{total} cases", not wrong, "; ".join(wrong))
    wrong = [f"satisfies({v!r}, {r!r}) -> {g} (want {w})" for (v, r), g, w in zip(grid_pairs, grid, grid_want) if g is not w]
    check(f"differential grid vs npm semver: {len(grid_pairs) - len(wrong)}/{len(grid_pairs)}", not wrong,
          f"{len(wrong)} wrong, e.g. " + "; ".join(wrong[:4]))

    with tempfile.TemporaryDirectory() as tmp:
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
