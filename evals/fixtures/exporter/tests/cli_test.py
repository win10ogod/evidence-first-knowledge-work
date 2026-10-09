import json
import subprocess
import sys
import unittest


def run_cli(fmt, records):
    return subprocess.run(
        [sys.executable, "-m", "exporter.cli", "--format", fmt],
        input=json.dumps(records), capture_output=True, text=True, encoding="utf-8",
    )


class JsonFormatTest(unittest.TestCase):
    def test_json_sorted_and_indented(self):
        proc = run_cli("json", [{"b": 1, "a": 2}])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, '[\n  {\n    "a": 2,\n    "b": 1\n  }\n]\n')

    def test_unknown_format_rejected(self):
        proc = run_cli("xml", [])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("invalid choice", proc.stderr)
