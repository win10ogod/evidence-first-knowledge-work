import contextlib
import csv
import io
import shutil
import tempfile
import unittest
from pathlib import Path

from inventory.__main__ import main

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "inventory.json"


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(list(argv))
    return code, out.getvalue()


class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = str(Path(self.tmp.name) / "inv.json")
        shutil.copy(SAMPLE, self.file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_export(self):
        code, out = run("--file", self.file, "export")
        self.assertEqual(code, 0)
        row = next(csv.DictReader(io.StringIO(out)))
        self.assertEqual((row["sku"], row["price"], row["total"]), ("A1", "12.50", "37.50"))

    def test_value(self):
        self.assertEqual(run("--file", self.file, "value")[1], "stock value: 85.38\n")

    def test_add_then_list(self):
        run("--file", self.file, "add", "--sku", "C3", "--name", "Gear", "--qty", "4", "--price", "7.25")
        lines = run("--file", self.file, "list")[1].splitlines()
        self.assertEqual(lines[-1], "C3  Gear  qty=4  price=7.25")


if __name__ == "__main__":
    unittest.main()
