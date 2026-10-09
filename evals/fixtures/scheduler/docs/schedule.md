# Scheduling rules

A job is `{"at": "HH:MM", "tz": "<IANA zone>"}` and runs once per **local calendar day** of its zone.

`next_run(job, after)` takes a timezone-aware `after` (in any zone) and returns the earliest scheduled
run that is **strictly later than `after` as an instant** (compare absolute time, not wall-clock time).
The result is a timezone-aware datetime expressed in the job's zone, with the correct UTC offset.

For each local calendar day, the run instant is:

1. **Normal days:** the instant at which the local wall clock shows `at`.
2. **Clocks set back (the wall time occurs twice):** only the **first** occurrence. The job does not
   run again at the repeated wall time.
   Example: `02:30` in `Europe/Berlin` on 2026-10-25 runs at `2026-10-25T02:30:00+02:00` only.
3. **Clocks set forward (the wall time does not exist):** the instant the clocks jump, i.e. the first
   wall time that exists after the skipped interval.
   Example: `02:30` in `Europe/Berlin` on 2026-03-29 runs at `2026-03-29T03:00:00+02:00`.

Every zone in the IANA database must work, including zones whose DST shift is not one hour and zones
that change their clocks at midnight.
