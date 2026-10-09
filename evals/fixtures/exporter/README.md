# exporter (evaluation fixture)

Converts a JSON array of records read from stdin into an output format.

```bash
echo '[{"b": 1, "a": 2}]' | python -m exporter.cli --format json
```

## Tests

Run from this directory:

```bash
python run_tests.py
```

Tests live in `tests/` and must be named `*_test.py`; other names are not collected.

## Formats

Supported and planned formats are specified in [docs/formats.md](docs/formats.md).
