# Sessions

## Input

A CSV file with the columns `user,timestamp,event` (with a header row). Rows are **not** guaranteed to be
in time order; they arrive from several regional collectors.

`timestamp` is ISO 8601. It may carry `Z` or a UTC offset (`2026-03-01T10:00:00+02:00`). A timestamp
without an offset (`2026-03-01 08:00:00` or `2026-03-01T08:00:00`) is in **UTC**.

## Rules

1. A user's events are ordered by the instant they happened.
2. A new session starts when **30 minutes or more** have passed since the user's previous event.
3. A session's duration is the time from its first to its last event, in whole seconds.

## Output

A JSON object keyed by user id (keys sorted), each value
`{"sessions": <count>, "total_seconds": <sum of session durations>}`.
