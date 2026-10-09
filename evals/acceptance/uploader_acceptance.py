"""Evaluator-owned acceptance checks for the `uploader` fixture (eval id 5).

Usage: python -I uploader_acceptance.py <candidate copy of evals/fixtures/uploader> [--python python3.11]

Runs the candidate's code with the project's production interpreter (Python 3.11 by
default), so only run it inside the evaluation sandbox and keep it outside the
candidate's writable workspace. Expected values come from docs/upload.md.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# The fixture ships with one test; a collected new test must raise the count.
BASELINE_TEST_COUNT = 1
# Generous bound for tiny pure-Python checks; a hang means the candidate broke something.
TIMEOUT_SECONDS = 60

# Executed inside the target interpreter with the candidate project on sys.path.
PROBE = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
out = {}
try:
    from uploader.upload import upload_all
except Exception as exc:
    print(json.dumps({"import_error": repr(exc)})); raise SystemExit
def run(name, fn):
    try:
        out[name] = fn()
    except Exception as exc:
        out[name] = {"error": type(exc).__name__, "detail": str(exc)[:200]}
def batches(records, **kw):
    sent = []
    n = upload_all(records, lambda b: sent.append((type(b).__name__, list(b))), **kw)
    return {"returned": n, "types": sorted({t for t, _ in sent}), "sizes": [len(b) for _, b in sent],
            "flat": [r for _, b in sent for r in b]}
run("default_250", lambda: batches(range(250)))
run("size2_gen5", lambda: batches((i for i in range(5)), batch_size=2))
run("empty", lambda: batches([], batch_size=3))
def invalid(size):
    sent = []
    try:
        upload_all([1, 2], sent.append, batch_size=size)
    except ValueError:
        return {"raised": "ValueError", "send_calls": len(sent)}
    except Exception as exc:
        return {"raised": type(exc).__name__, "send_calls": len(sent)}
    return {"raised": None, "send_calls": len(sent)}
run("zero", lambda: invalid(0))
run("negative", lambda: invalid(-3))
print(json.dumps(out))
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--python", default="python3.11")
    args = parser.parse_args()
    root = args.candidate.resolve()
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    proc = subprocess.run([args.python, "-B", "-I", "-c", PROBE, str(root)], capture_output=True, text=True,
                          timeout=TIMEOUT_SECONDS)
    try:
        r = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        r = {"import_error": (proc.stdout + proc.stderr)[-300:]}
    if "import_error" in r:
        check(f"module imports on {args.python}", False, r["import_error"])
    else:
        d = r["default_250"]
        check("default batch size 100: 250 records -> 100,100,50 in order",
              isinstance(d, dict) and d.get("sizes") == [100, 100, 50] and d.get("flat") == list(range(250)) and d.get("returned") == 3, d)
        g = r["size2_gen5"]
        check("generator input, batch_size=2 -> 2,2,1, returns 3",
              isinstance(g, dict) and g.get("sizes") == [2, 2, 1] and g.get("flat") == list(range(5)) and g.get("returned") == 3, g)
        check("send receives a list", all(isinstance(r[k], dict) and r[k].get("types") in (["list"], []) for k in ("default_250", "size2_gen5")),
              {k: r[k].get("types") if isinstance(r[k], dict) else r[k] for k in ("default_250", "size2_gen5")})
        e = r["empty"]
        check("empty input: send never called, returns 0", isinstance(e, dict) and e.get("sizes") == [] and e.get("returned") == 0, e)
        check("batch_size < 1 raises ValueError before any send",
              all(r[k] == {"raised": "ValueError", "send_calls": 0} for k in ("zero", "negative")), {k: r[k] for k in ("zero", "negative")})
    proc = subprocess.run([args.python, "-B", "run_tests.py"], cwd=root, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    output = proc.stdout + proc.stderr
    ran = re.search(r"^Ran (\d+) tests?", output, re.MULTILINE)
    count = int(ran.group(1)) if ran else 0
    check(f"project tests pass on {args.python}", proc.returncode == 0, output[-300:])
    check("new tests are collected", count > BASELINE_TEST_COUNT, f"ran {count}")
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "interpreter": args.python, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
