# uploader (evaluation fixture)

Sends records to the ingestion API through a `send` callable supplied by the caller.

## Tests

```bash
python run_tests.py
```

Tests live in `tests/` and are named `test_*.py`. CI runs the same command (see `.github/workflows/ci.yml`).

## Behavior

The contract of `upload_all` is specified in [docs/upload.md](docs/upload.md).
