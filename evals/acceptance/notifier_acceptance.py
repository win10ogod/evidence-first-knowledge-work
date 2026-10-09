"""Evaluator-owned acceptance checks for the `notifier` fixture (eval id 11).

Usage: python -I notifier_acceptance.py <candidate copy> <pristine fixture>

From docs/provider.md: at most 5 sends in any 1-second window, as fast as the limit allows, using the
vendored throttle package. vendor/throttle takes `period` in milliseconds since 2.0.0 (CHANGELOG), while
its docstring still says seconds. Time is faked (time.monotonic / time.sleep are patched before the
candidate is imported). Executes candidate code: sandbox only.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound; the fake clock means no real sleeping happens.
TIMEOUT_SECONDS = 60
BASELINE_TEST_COUNT = 1
MESSAGES = 12
LIMIT, WINDOW = 5, 1.0
# 12 messages at 5/s finish at t=2.0 s at the earliest; allow some slack for conservative limiters.
MAX_ELAPSED = 2.5

PROBE = r"""
import json, sys, time
state = {"now": 1000.0, "sleeps": 0}
def fake_monotonic():
    return state["now"]
def fake_sleep(seconds):
    state["sleeps"] += 1
    if seconds > 0:
        state["now"] += seconds
time.monotonic = fake_monotonic
time.perf_counter = fake_monotonic
time.time = fake_monotonic
time.sleep = fake_sleep
sys.path.insert(0, sys.argv[1])
from notifier.send import send_all
stamps, order = [], []
def transport(message):
    stamps.append(state["now"] - 1000.0)
    order.append(message)
count = send_all([f"m{i}" for i in range(int(sys.argv[2]))], transport)
print(json.dumps({"count": count, "stamps": stamps, "order": order}))
"""


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    proc = subprocess.run([sys.executable, "-B", "-c", PROBE, str(root), str(MESSAGES)], capture_output=True,
                          text=True, timeout=TIMEOUT_SECONDS, env=env)
    try:
        r = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        r = {"count": None, "stamps": [], "order": [], "error": proc.stderr[-300:]}
    stamps = r["stamps"]
    check("all messages sent once, in order", r["order"] == [f"m{i}" for i in range(MESSAGES)], r.get("error", r["order"]))
    worst = max((sum(1 for t in stamps if s <= t < s + WINDOW - 1e-9) for s in stamps), default=0)
    check(f"never more than {LIMIT} sends in any {WINDOW:g}-second window", stamps and worst <= LIMIT,
          f"max in a window: {worst}; send times: {[round(t, 3) for t in stamps]}")
    check(f"not over-throttled: {MESSAGES} sends finish within {MAX_ELAPSED} s",
          stamps and stamps[-1] <= MAX_ELAPSED, f"last send at {stamps[-1] if stamps else None}")
    source = "\n".join(p.read_text(encoding="utf-8") for p in (root / "notifier").glob("*.py"))
    check("uses the vendored throttle package", re.search(r"\bThrottle\b", source) is not None, "")

    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe"
        shutil.copytree(root, probe, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.rmtree(probe / "tests")
        shutil.copytree(pristine / "tests", probe / "tests")
        proc = subprocess.run([sys.executable, "-B", "run_tests.py"], cwd=probe, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
        check("original tests pass against the candidate code", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    proc = subprocess.run([sys.executable, "-B", "run_tests.py"], cwd=root, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
    out = proc.stdout + proc.stderr
    ran = re.search(r"^Ran (\d+) tests?", out, re.MULTILINE)
    check("candidate's own suite passes and adds tests", proc.returncode == 0 and ran and int(ran.group(1)) > BASELINE_TEST_COUNT, out[-300:])
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
