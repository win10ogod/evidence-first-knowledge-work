import io
import os
import tempfile
import unittest
from unittest import mock

from fetcher import __main__ as cli
from fetcher import client


class FakeTransport:
    def __init__(self):
        self.calls = []

    def __call__(self, url, timeout_ms):
        self.calls.append((url, timeout_ms))
        return b"hello"


class CliTest(unittest.TestCase):
    def setUp(self):
        self.fake = FakeTransport()
        patcher = mock.patch.object(client, "TRANSPORT", self.fake)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.cwd = tempfile.TemporaryDirectory()
        self.addCleanup(self.cwd.cleanup)
        old = os.getcwd()
        os.chdir(self.cwd.name)
        self.addCleanup(os.chdir, old)

    def run_cli(self, *argv):
        out = io.StringIO()
        code = cli.main(list(argv), out=out)
        return code, out.getvalue()

    def test_fetch_prints_size(self):
        code, out = self.run_cli("fetch", "https://example.test/a")
        self.assertEqual((code, out), (0, "https://example.test/a 5\n"))

    def test_retries_from_env(self):
        with mock.patch.dict(os.environ, {"FETCHER_RETRIES": "0"}):
            self.assertEqual(self.run_cli("fetch", "https://example.test/a")[0], 0)

    def test_invalid_retries(self):
        with mock.patch("sys.stderr", new_callable=io.StringIO) as err:
            code, _ = self.run_cli("--retries", "-1", "fetch", "https://example.test/a")
        self.assertEqual(code, 2)
        self.assertIn("error: retries must be >= 0", err.getvalue())

    def test_fetch_all(self):
        with open("urls.txt", "w", encoding="utf-8") as handle:
            handle.write("https://example.test/a\nhttps://example.test/b\n")
        code, out = self.run_cli("fetch-all", "urls.txt")
        self.assertEqual(code, 0)
        self.assertEqual(len(self.fake.calls), 2)


if __name__ == "__main__":
    unittest.main()
