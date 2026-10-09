# fetcher (evaluation fixture)

Downloads URLs and prints their size.

```bash
python -m fetcher fetch https://example.com/a
python -m fetcher fetch-all urls.txt        # one URL per line
```

Options and how they are configured are described in [docs/config.md](docs/config.md).

## Tests

```bash
python run_tests.py
```

Tests replace the network with a fake transport (`fetcher.client.TRANSPORT`).
