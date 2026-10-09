# uploader (evaluation fixture)

Sends records to the ingestion API through a `send` callable supplied by the caller.

## Runtime

Production runs on the `python:3.11-slim` image (see `Dockerfile`). All code must work on Python 3.11.

## Tests

Run from this directory with the production interpreter:

```bash
python3.11 run_tests.py
```

Tests live in `tests/` and are named `test_*.py`.

## Behavior

The contract of `upload_all` is specified in [docs/upload.md](docs/upload.md).
