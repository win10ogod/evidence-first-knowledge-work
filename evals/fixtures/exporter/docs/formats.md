# Output formats

Every format reads a JSON array of objects from stdin and writes UTF-8 text to stdout.
A format becomes available on the command line when its writer is added to
`REGISTRY` in `exporter/registry.py`; `cli.py` offers exactly the registered names.

## json (supported)

The whole array serialized with `json.dumps(records, indent=2, sort_keys=True)`,
followed by a single newline.

## lines (planned)

One record per line: each record serialized with
`json.dumps(record, sort_keys=True, ensure_ascii=False)` followed by `\n`.
Non-ASCII characters are written as-is. Empty input (`[]`) produces empty output:
no characters at all, not even a newline.
