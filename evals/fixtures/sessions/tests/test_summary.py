import unittest

from sessions.summary import summarise


def events(*rows):
    return [(user, ts, "click") for user, ts in rows]


class SummaryTest(unittest.TestCase):
    def test_single_session(self):
        got = summarise(events(("u1", "2026-03-01T10:00:00Z"), ("u1", "2026-03-01T10:10:00Z")))
        self.assertEqual(got, {"u1": {"sessions": 1, "total_seconds": 600}})

    def test_long_gap_starts_new_session(self):
        got = summarise(events(("u1", "2026-03-01T10:00:00Z"), ("u1", "2026-03-01T11:00:00Z")))
        self.assertEqual(got, {"u1": {"sessions": 2, "total_seconds": 0}})

    def test_gap_of_exactly_30_minutes_starts_new_session(self):
        got = summarise(events(("u1", "2026-03-01T10:00:00Z"), ("u1", "2026-03-01T10:30:00Z")))
        self.assertEqual(got, {"u1": {"sessions": 2, "total_seconds": 0}})


if __name__ == "__main__":
    unittest.main()
