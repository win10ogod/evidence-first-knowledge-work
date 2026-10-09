import unittest
from datetime import datetime

from scheduler.core import next_run

BERLIN_0230 = {"at": "02:30", "tz": "Europe/Berlin"}


class NextRunTest(unittest.TestCase):
    def test_later_same_day(self):
        after = datetime.fromisoformat("2026-06-01T01:00:00+02:00")
        self.assertEqual(next_run(BERLIN_0230, after).isoformat(), "2026-06-01T02:30:00+02:00")

    def test_rolls_to_next_day(self):
        after = datetime.fromisoformat("2026-06-01T12:00:00+02:00")
        self.assertEqual(next_run(BERLIN_0230, after).isoformat(), "2026-06-02T02:30:00+02:00")

    def test_spring_forward_runs_when_clocks_jump(self):
        after = datetime.fromisoformat("2026-03-28T12:00:00+01:00")
        self.assertEqual(next_run(BERLIN_0230, after).isoformat(), "2026-03-29T03:00:00+02:00")


if __name__ == "__main__":
    unittest.main()
