# Inventory file format

The inventory is one JSON document: `{"format": <int>, "items": [...]}`. `inventory/store.py` reads and
writes it.

## Changing the item schema

Inventory files live on shop machines for years and are never upgraded by hand, so:

1. Any change to what an item stores (a new field, a renamed field, a changed unit) **bumps
   `CURRENT_FORMAT`** by one.
2. Add a migration to `MIGRATIONS` that turns a document of the previous format into the new one,
   filling new fields with their documented default. Never edit an existing migration.
3. Every older format must keep loading. `tests/data/` holds one sample file per past format; add a
   sample of the format you are replacing when you bump.
4. Files are always **saved** in the current format.
5. A file whose `format` is newer than `CURRENT_FORMAT` is rejected with `unsupported format N`.

## History

| Format | Change |
| --- | --- |
| 1 | `price` as a float number of dollars |
| 2 | `price` replaced by integer `price_cents` |
