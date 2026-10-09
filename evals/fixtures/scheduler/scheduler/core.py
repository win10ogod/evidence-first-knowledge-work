from datetime import timedelta
from zoneinfo import ZoneInfo


def parse_at(text):
    hours, minutes = text.split(":")
    return int(hours), int(minutes)


def next_run(job, after):
    """Return the next run of `job` strictly after the aware datetime `after` (see docs/schedule.md)."""
    tz = ZoneInfo(job["tz"])
    hour, minute = parse_at(job["at"])
    local = after.astimezone(tz)
    candidate = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= local:
        candidate += timedelta(days=1)
    return candidate
