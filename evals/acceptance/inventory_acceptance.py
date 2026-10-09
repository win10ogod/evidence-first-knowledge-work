"""Evaluator-owned acceptance checks for the `inventory` fixture (eval id 13).

Usage: python -I inventory_acceptance.py <candidate copy> <pristine fixture>

Derived by hand from docs/discounts.md and docs/storage.md. The discount touches the model, the file
format (bump to 3 plus a 2->3 migration and a format-2 sample), the CLI (option, exit status 2 with an
exact message, list suffix), the CSV column, and both money paths: export goes through pricing.py while
`value` goes through report.py, which repeats the arithmetic. Line totals round half up per line:
1 x 10.01 at 50% is 5.005 -> 5.01. Executes candidate code: sandbox only.
"""

import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Generous bound for a tiny CLI.
TIMEOUT_SECONDS = 60
BASELINE_TEST_COUNT = 6
MESSAGE = "error: discount must be a whole number from 0 to 100"
HEADER = ["sku", "name", "qty", "price", "discount", "total"]

PROBE = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
from inventory import store
samples = []
for path in sorted((store.Path(sys.argv[1]) / "tests" / "data").glob("*.json")):
    try:
        fmt = json.loads(path.read_text(encoding="utf-8")).get("format")
        store.load(path)
        samples.append([path.name, fmt, "ok"])
    except Exception as exc:
        samples.append([path.name, None, f"{type(exc).__name__}: {exc}"])
print(json.dumps({"current": store.CURRENT_FORMAT, "migrations": sorted(store.MIGRATIONS), "samples": samples}))
"""


def main():
    root, pristine = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": str(detail)[:300]})

    def run(args, cwd=root):
        return subprocess.run([sys.executable, "-B", *args], cwd=cwd, capture_output=True, text=True,
                              timeout=TIMEOUT_SECONDS, env=env)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        inv = tmp / "inv.json"
        shutil.copy(pristine / "data" / "inventory.json", inv)

        def cli(*argv, file=inv):
            return run(["-m", "inventory", "--file", str(file), *argv])

        def rows(proc):
            return list(csv.reader(io.StringIO(proc.stdout)))

        got = rows(cli("export"))
        check("format-2 file exports with the discount column (0)",
              got[:2] == [HEADER, ["A1", "Widget", "3", "12.50", "0", "37.50"]], got[:2])
        added = [cli("add", "--sku", "E5", "--name", "Valve", "--qty", "1", "--price", "10.01", "--discount", "50"),
                 cli("add", "--sku", "F6", "--name", "Hose", "--qty", "3", "--price", "3.33", "--discount", "15"),
                 cli("add", "--sku", "G7", "--name", "Free", "--qty", "2", "--price", "1.00", "--discount", "100"),
                 cli("add", "--sku", "H8", "--name", "Plain", "--qty", "1", "--price", "2.00")]
        check("add accepts --discount 50, 15, 100 and no --discount", all(p.returncode == 0 for p in added),
              [p.stderr[-120:] for p in added if p.returncode])
        try:
            saved = json.loads(inv.read_text(encoding="utf-8"))
        except ValueError as exc:
            saved = {"error": str(exc)}
        by_sku = {i.get("sku"): i for i in saved.get("items", [])}
        check("saved file is format 3", saved.get("format") == 3, saved.get("format"))
        check("saved items store discount_pct (50, 15, 100, default 0, migrated 0)",
              [by_sku.get(s, {}).get("discount_pct") for s in ("E5", "F6", "G7", "H8", "A1")] == [50, 15, 100, 0, 0],
              {s: i.get("discount_pct") for s, i in by_sku.items()})
        got = {r[0]: r for r in rows(cli("export"))[1:]}
        want = {"E5": ["E5", "Valve", "1", "10.01", "50", "5.01"], "F6": ["F6", "Hose", "3", "3.33", "15", "8.49"],
                "G7": ["G7", "Free", "2", "1.00", "100", "0.00"], "H8": ["H8", "Plain", "1", "2.00", "0", "2.00"]}
        for sku, row in want.items():
            check(f"export row {sku}: {','.join(row)}", got.get(sku) == row, got.get(sku))
        proc = cli("value")
        # 37.50 + 47.88 + 5.01 + 8.49 + 0.00 + 2.00
        check("value uses discounted, per-line half-up totals (100.88)", proc.stdout == "stock value: 100.88\n",
              proc.stdout + proc.stderr[-100:])
        lines = cli("list").stdout.splitlines()
        check("list shows the discount suffix only when non-zero",
              "E5  Valve  qty=1  price=10.01 (-50%)" in lines and "A1  Widget  qty=3  price=12.50" in lines, lines)
        before = inv.read_text(encoding="utf-8")
        for bad in ("101", "-1", "12.5", "abc"):
            proc = cli("add", "--sku", "Z9", "--name", "Bad", "--qty", "1", "--price", "1.00", "--discount", bad)
            check(f"--discount {bad} is rejected with exit 2 and the documented message",
                  proc.returncode == 2 and MESSAGE in proc.stderr, f"exit {proc.returncode}: {proc.stderr.strip()[-150:]}")
        check("rejected adds leave the file unchanged", inv.read_text(encoding="utf-8") == before, "")

        got = rows(cli("export", file=pristine / "tests" / "data" / "format1.json"))
        check("format-1 file still loads (discount 0)", ["D4", "Bolt", "100", "0.29", "0", "29.00"] in got, got)
        future = tmp / "future.json"
        future.write_text(json.dumps({"format": 4, "items": []}), encoding="utf-8")
        proc = cli("export", file=future)
        check("format-4 file is rejected as unsupported", proc.returncode != 0 and "unsupported format 4" in proc.stderr,
              proc.stderr[-150:])

        proc = run(["-c", PROBE, str(root)])
        try:
            meta = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            meta = {"current": None, "migrations": [], "samples": [], "error": proc.stderr[-200:]}
        check("CURRENT_FORMAT is 3 with migrations 1->2 and 2->3", meta["current"] == 3 and meta["migrations"] == [1, 2], meta)
        check("tests/data has a loadable format-2 sample (storage.md rule 3)",
              any(fmt == 2 and status == "ok" for _, fmt, status in meta["samples"]), meta["samples"])

        probe = tmp / "probe"
        shutil.copytree(root, probe, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.rmtree(probe / "tests")
        shutil.copytree(pristine / "tests", probe / "tests")
        proc = run(["run_tests.py"], probe)
        check("original tests pass against the candidate code", proc.returncode == 0, (proc.stdout + proc.stderr)[-300:])
    proc = run(["run_tests.py"])
    out = proc.stdout + proc.stderr
    ran = [int(line.split()[1]) for line in out.splitlines() if line.startswith("Ran ")]
    check("candidate's own suite passes and adds tests", proc.returncode == 0 and ran and ran[-1] > BASELINE_TEST_COUNT, out[-300:])
    passed = all(c["passed"] for c in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
