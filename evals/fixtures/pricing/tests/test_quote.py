import unittest

from pricing.quote import quote


class QuoteTest(unittest.TestCase):
    def test_coupon_eu(self):
        self.assertEqual(quote("eu", 10_000, "WELCOME10"), 10_800)

    def test_plain_eu(self):
        self.assertEqual(quote("eu", 10_000), 12_000)

    def test_plain_us(self):
        self.assertEqual(quote("us", 10_000), 10_000)


if __name__ == "__main__":
    unittest.main()
