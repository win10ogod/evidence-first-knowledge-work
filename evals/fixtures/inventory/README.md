# inventory (evaluation fixture)

A small stock-keeping CLI.

```bash
python -m inventory --file data/inventory.json list
python -m inventory --file data/inventory.json add --sku C3 --name Gear --qty 4 --price 7.25
python -m inventory --file data/inventory.json export     # CSV on stdout
python -m inventory --file data/inventory.json value      # total stock value
python -m inventory --file data/inventory.json low --below 5
```

- File format and schema changes: [docs/storage.md](docs/storage.md)
- Discounts: [docs/discounts.md](docs/discounts.md)

## Tests

```bash
python run_tests.py
```
