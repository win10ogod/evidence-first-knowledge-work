# upload_all

```python
upload_all(records, send, batch_size=100) -> int
```

- `records` is any iterable of records, including a generator. It is consumed once, in order.
- Records are sent in order, in consecutive batches of at most `batch_size` records.
  Only the last batch may be smaller.
- `send` is called once per batch with a `list` of records (not a tuple or other sequence).
- Empty `records`: `send` is never called and the function returns `0`.
- `batch_size` smaller than 1 raises `ValueError` before `send` is called.
- Returns the number of batches sent.

The current implementation predates batching: it sends one record per call.
