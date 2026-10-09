import unittest

from versions import satisfies


class SatisfiesTest(unittest.TestCase):
    def test_caret_major(self):
        self.assertTrue(satisfies("1.9.0", "^1.2.3"))
        self.assertFalse(satisfies("2.0.0", "^1.2.3"))

    def test_union(self):
        self.assertTrue(satisfies("3.1.0", "^1.0.0 || ^3.0.0"))

    def test_caret_zero_major_stays_in_minor(self):
        self.assertTrue(satisfies("0.2.9", "^0.2.3"))
        self.assertFalse(satisfies("0.3.0", "^0.2.3"))


if __name__ == "__main__":
    unittest.main()
