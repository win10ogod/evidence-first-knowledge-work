# Configuration

Every option can be set in four places. Highest precedence first:

1. the command-line flag, e.g. `--retries 5`;
2. the environment variable `FETCHER_<NAME>`, e.g. `FETCHER_RETRIES=5`;
3. the `[fetcher]` table of `fetcher.toml` in the current directory, e.g. `retries = 5`;
4. the default.

All options are resolved in one place, `fetcher.config.resolve()`, so that every command
sees the same values. An invalid value from any source makes the program print
`error: <message>` to stderr and exit with status 2.

## Options

| Option | Type | Default | Rule | Applies to |
| --- | --- | --- | --- | --- |
| `retries` | integer | 2 | `retries must be >= 0` | `fetch`, `fetch-all` |
| `timeout` *(planned)* | number of **seconds**, may be fractional | 10 | `timeout must be > 0` | every request made by `fetch` and `fetch-all` |
