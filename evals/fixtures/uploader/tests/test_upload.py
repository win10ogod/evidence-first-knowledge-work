import unittest

from uploader.upload import upload_all


class UploadAllTest(unittest.TestCase):
    def test_delivers_every_record_in_order(self):
        sent = []
        calls = upload_all(["a", "b", "c"], sent.append)
        delivered = [record for batch in sent for record in batch]
        self.assertEqual(delivered, ["a", "b", "c"])
        self.assertEqual(calls, len(sent))


if __name__ == "__main__":
    unittest.main()
