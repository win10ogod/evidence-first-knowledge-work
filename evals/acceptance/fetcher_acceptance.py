"""Evaluator-owned acceptance checks for the `fetcher` fixture (eval id 7).

Usage: python -I fetcher_acceptance.py <candidate copy> <pristine fixture>

Expected values come from docs/config.md: seconds on every surface, precedence
flag > FETCHER_TIMEOUT > fetcher.toml > default 10, `error: timeout must be > 0` with exit 2,
and the value applied to every request of both `fetch` and `fetch-all`. The client takes
milliseconds (fetcher/client.py). The pristine tests are also run against the candidate code.
Executes candidate code: sandbox only.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound for in-process CLI calls with a fake transport.
TIMEOUT_SECONDS = 60
BASELINE_TEST_COUNT = 4

# Runs inside a child interpreter: fake transport, isolated cwd/env, one CLI invocation.
PROBE = r"""
import io, json, os, sys, contextlib
root, cwd, argv, env_json = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), json.loads(sys.argv[4])
sys.path.insert(0, root)
for k in [k for k in os.environ if k.startswith("FETCHER_")]:
    del os.environ[k]
os.environ.update(env_json)
os.chdir(cwd)
from fetcher import client
from fetcher import __main__ as cli
calls = []
def fake(url, timeout_ms):
    calls.append(timeout_ms)
    return b"hello"
client.TRANSPORT = fake
err = io.StringIO()
code = None
with contextlib.redirect_stderr(err):
    try:
        code = cli.main(argv, out=io.StringIO())
    except SystemExit as exc:
        code = exc.code
print(json.dumps({"code": code, "timeouts": calls, "stderr": err.getvalue()[-300:]}))
"""


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    def invoke(args_global, args_tail, environ=None, toml=None):
        """Run with --timeout before the subcommand; if argparse rejects that, retry after it."""
        with tempfile.TemporaryDirectory() as cwd:
            Path(cwd, "urls.txt").write_text("https://e.test/a\nhttps://e.test/b\n", encoding="utf-8")
            if toml is not None:
                Path(cwd, "fetcher.toml").write_text(f"[fetcher]\n{toml}\n", encoding="utf-8")
            results = []
            for argv in (args_global + args_tail, args_tail[:1] + args_global + args_tail[1:]):
                proc = subprocess.run([sys.executable, "-B", "-c", PROBE, str(root), cwd, json.dumps(argv),
                                       json.dumps(environ or {})], capture_output=True, text=True,
                                      timeout=TIMEOUT_SECONDS, env=env)
                try:
                    result = json.loads(proc.stdout.strip().splitlines()[-1])
                except (ValueError, IndexError):
                    result = {"code": None, "timeouts": [], "stderr": proc.stderr[-300:]}
                results.append(result)
                if not args_global or "unrecognized arguments" not in result["stderr"]:
                    return result
            return results[-1]

    def ms(result, expected):
        return result["code"] == 0 and result["timeouts"] and all(t == expected for t in result["timeouts"])

    url = ["fetch", "https://e.test/a"]
    r = invoke(["--timeout", "5"], url); check("flag --timeout 5 -> 5000 ms", ms(r, 5000), r)
    r = invoke(["--timeout", "2.5"], url); check("fractional seconds 2.5 -> 2500 ms", ms(r, 2500), r)
    r = invoke([], url, {"FETCHER_TIMEOUT": "4"}); check("FETCHER_TIMEOUT=4 -> 4000 ms", ms(r, 4000), r)
    r = invoke([], url, toml="timeout = 7"); check("fetcher.toml timeout = 7 -> 7000 ms", ms(r, 7000), r)
    r = invoke(["--timeout", "3"], url, {"FETCHER_TIMEOUT": "4"}, "timeout = 7"); check("flag beats env and file", ms(r, 3000), r)
    r = invoke([], url, {"FETCHER_TIMEOUT": "4"}, "timeout = 7"); check("env beats file", ms(r, 4000), r)
    r = invoke([], url); check("default 10 s -> 10000 ms", ms(r, 10000), r)
    batch = ["fetch-all", "urls.txt"]
    r = invoke(["--timeout", "5"], batch); check("fetch-all honours the flag on every request", ms(r, 5000) and len(r["timeouts"]) == 2, r)
    r = invoke([], batch, {"FETCHER_TIMEOUT": "4"}); check("fetch-all honours the env var", ms(r, 4000), r)
    r = invoke(["--timeout", "0"], url); check("--timeout 0 -> exit 2, 'error: timeout must be > 0'", r["code"] == 2 and "error: timeout must be > 0" in r["stderr"] and not r["timeouts"], r)
    r = invoke([], url, {"FETCHER_TIMEOUT": "abc"}); check("non-numeric env value -> exit 2 with 'error:'", r["code"] == 2 and "error:" in r["stderr"] and not r["timeouts"], r)
    r = invoke([], url, toml="timeout = -1"); check("negative value in file -> exit 2", r["code"] == 2 and "timeout must be > 0" in r["stderr"], r)

    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "probe"
        shutil.copytree(root, probe, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.rmtree(probe / "tests")
        shutil.copytree(pristine / "tests", probe / "tests")
        proc = subprocess.run([sys.executable, "-B", "run_tests.py"], cwd=probe, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
        check("original tests pass against the candidate code", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    proc = subprocess.run([sys.executable, "-B", "run_tests.py"], cwd=root, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
    out = proc.stdout + proc.stderr
    import re
    ran = re.search(r"^Ran (\d+) tests?", out, re.MULTILINE)
    check("candidate's own suite passes and adds tests", proc.returncode == 0 and ran and int(ran.group(1)) > BASELINE_TEST_COUNT, out[-300:])
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
