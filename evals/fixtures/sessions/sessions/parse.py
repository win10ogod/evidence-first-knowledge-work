import csv
from datetime import datetime


def parse_timestamp(text):
    """Parse an event timestamp (see docs/sessions.md)."""
    return datetime.fromisoformat(text.strip()[:19])


def read_events(path):
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            yield row["user"], row["timestamp"], row["event"]
