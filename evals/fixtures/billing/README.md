# billing (evaluation fixture)

Computes invoice totals from a CSV of `quantity,unit_price[,discount_pct]` lines.

```bash
python -m billing invoice lines.csv
```

Rules are specified in [docs/billing.md](docs/billing.md).

## Tests

```bash
python run_tests.py
```
