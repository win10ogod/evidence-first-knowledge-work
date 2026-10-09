from collections import defaultdict
from datetime import timedelta

from sessions.parse import parse_timestamp

SESSION_GAP = timedelta(minutes=30)


def split_sessions(times):
    sessions = []
    for when in times:
        if sessions and when - sessions[-1][-1] <= SESSION_GAP:
            sessions[-1].append(when)
        else:
            sessions.append([when])
    return sessions


def summarise(events):
    by_user = defaultdict(list)
    for user, timestamp, _event in sorted(events, key=lambda e: (e[0], e[1])):
        by_user[user].append(parse_timestamp(timestamp))
    result = {}
    for user in sorted(by_user):
        sessions = split_sessions(by_user[user])
        total = sum(int((s[-1] - s[0]).total_seconds()) for s in sessions)
        result[user] = {"sessions": len(sessions), "total_seconds": total}
    return result
