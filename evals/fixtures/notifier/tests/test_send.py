import unittest

from notifier.send import send_all


class SendAllTest(unittest.TestCase):
    def test_sends_every_message_in_order(self):
        sent = []
        self.assertEqual(send_all(["a", "b", "c"], sent.append), 3)
        self.assertEqual(sent, ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
