import os
import tempfile
import unittest

from billing.invoice import render_total


def total_for(csv_text):
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
        handle.write(csv_text)
    try:
        return render_total(handle.name)
    finally:
        os.unlink(handle.name)


class InvoiceTotalTest(unittest.TestCase):
    def test_simple_lines(self):
        self.assertEqual(total_for("2,19.99\n1,5.00\n"), "44.98")

    def test_discount(self):
        self.assertEqual(total_for("1,10.00,10\n"), "9.00")

    def test_empty_invoice(self):
        self.assertEqual(total_for("# no lines\n"), "0.00")

    def test_half_cent_rounds_up(self):
        self.assertEqual(total_for("1,0.125\n"), "0.13")


if __name__ == "__main__":
    unittest.main()
