"""Tests for the bundled hook and snapshot script. They do not run or evaluate a model."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hooks"))

from zero_tests_guard import build_context, zero_test_signals  # noqa: E402

FIXTURES = json.loads((ROOT / "evals" / "fixtures" / "runner_outputs.json").read_text(encoding="utf-8"))
HOOK = ROOT / "hooks" / "zero_tests_guard.py"
SNAPSHOT = ROOT / "scripts" / "env_snapshot.py"


class ZeroTestsGuardTests(unittest.TestCase):
    def test_real_runner_outputs_are_classified(self):
        for case in FIXTURES["cases"]:
            with self.subTest(case=case["name"]):
                signals = zero_test_signals(case["stdout"] + "\n" + case["stderr"])
                self.assertEqual(bool(signals), case["zero_tests"], signals)

    def test_exit_code_zero_cases_are_covered(self):
        # The dangerous cases: a zero-test run that still exits 0.
        silent = [c["name"] for c in FIXTURES["cases"] if c["zero_tests"] and c["exit_code"] == 0]
        self.assertGreaterEqual(len(silent), 4, silent)

    def run_hook(self, payload):
        return subprocess.run([sys.executable, "-I", str(HOOK)], input=payload, capture_output=True,
                              text=True, timeout=30)

    def test_hook_emits_additional_context(self):
        case = next(c for c in FIXTURES["cases"] if c["name"] == "cargo-zero")
        payload = {"hook_event_name": "PostToolUse", "tool_name": "Bash",
                   "tool_input": {"command": case["command"]},
                   "tool_response": {"stdout": case["stdout"], "stderr": case["stderr"],
                                     "interrupted": False, "isImage": False}}
        proc = self.run_hook(json.dumps(payload))
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("NOT RUN", out["hookSpecificOutput"]["additionalContext"])

    def test_hook_is_silent_on_passing_runs_and_bad_input(self):
        case = next(c for c in FIXTURES["cases"] if c["name"] == "pytest-pass")
        payload = {"tool_name": "Bash", "tool_input": {"command": case["command"]},
                   "tool_response": {"stdout": case["stdout"], "stderr": case["stderr"]}}
        for raw in (json.dumps(payload), "not json", "[]", json.dumps({"tool_name": "Edit"})):
            with self.subTest(raw=raw[:30]):
                proc = self.run_hook(raw)
                self.assertEqual(proc.returncode, 0)
                self.assertEqual(proc.stdout, "")

    def test_non_bash_tools_ignored(self):
        self.assertIsNone(build_context({"tool_name": "Read", "tool_response": {"stdout": "Ran 0 tests"}}))


class EnvSnapshotTests(unittest.TestCase):
    def test_reports_manifests_packages_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='x'\n")
            (root / "AGENTS.md").write_text("rules\n")
            pkg = root / "node_modules" / "left-pad"
            pkg.mkdir(parents=True)
            (pkg / "package.json").write_text(json.dumps({"version": "1.3.0", "types": "index.d.ts"}))
            before = sorted(str(p) for p in root.rglob("*"))
            proc = subprocess.run(
                [sys.executable, "-I", str(SNAPSHOT), "--root", str(root), "--json",
                 "--node", "left-pad", "--node", "absent-pkg", "--py", "surely-not-installed-dist"],
                capture_output=True, text=True, timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            snap = json.loads(proc.stdout)
            self.assertEqual(sorted(str(p) for p in root.rglob("*")), before)
        self.assertIn("pyproject.toml", snap["manifests"])
        self.assertIn("AGENTS.md", snap["instruction_files"])
        self.assertEqual(snap["node_packages"]["left-pad"]["version"], "1.3.0")
        self.assertIsNone(snap["node_packages"]["absent-pkg"]["version"])
        self.assertIsNone(snap["python"]["dists"]["surely-not-installed-dist"]["version"])

    def test_bad_root(self):
        proc = subprocess.run([sys.executable, "-I", str(SNAPSHOT), "--root", "/nonexistent/dir"],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
