# Per-item discounts

Each item can carry a discount: `discount_pct`, a whole number of percent from 0 to 100. Items without
one have `discount_pct` 0.

## Setting it

`python -m inventory add ... --discount 15`. The option is optional (default 0). A value that is not a
whole number from 0 to 100 is rejected with exit status 2 and this message on standard error:

```
error: discount must be a whole number from 0 to 100
```

## Money

An item's line total is `qty x price_cents x (100 - discount_pct) / 100`, rounded **half up** to a whole
cent, per line (totals of several items are sums of rounded lines). Every figure that reports an item's
money uses the discounted line total.

## Output

- `export` (CSV): a `discount` column between `price` and `total`, holding the integer percent
  (`0` when there is none). `price` stays the undiscounted unit price.
- `list`: when the discount is not 0, append ` (-15%)` after the price, for example
  `A1  Widget  qty=3  price=12.50 (-15%)`.

## Storage

The field is part of the stored item; see [storage.md](storage.md).
