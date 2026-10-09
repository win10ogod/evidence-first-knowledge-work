# scheduler (evaluation fixture)

Computes when daily jobs run next. Jobs are defined by a local wall-clock time and an IANA time zone.

```python
from scheduler.core import next_run
next_run({"at": "02:30", "tz": "Europe/Berlin"}, after)   # after: timezone-aware datetime
```

The scheduling rules, including what happens around daylight-saving changes, are in
[docs/schedule.md](docs/schedule.md).

## Tests

```bash
python run_tests.py
```
