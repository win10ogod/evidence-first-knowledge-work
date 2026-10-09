# Billing rules

Input is a CSV with one invoice line per row: `quantity,unit_price[,discount_pct]`.
`unit_price` is a decimal string such as `19.99` and may be negative (credit notes).
`quantity` is an integer. `discount_pct` is an optional decimal percentage (default 0).

1. **Line amount** = quantity × unit_price × (1 − discount_pct / 100), computed exactly.
2. **Line total** = the line amount rounded to the cent, **half-up**: exact halves round away
   from zero (`0.125` → `0.13`, `-0.125` → `-0.13`, `1.005` → `1.01`).
3. **Invoice total** = the sum of the rounded line totals (round each line first, then add).
4. Output is the invoice total with exactly two decimal places, e.g. `12.30`, `-0.13`, `0.00`.

All arithmetic must be exact decimal arithmetic. Binary floating point cannot represent
values such as `1.005` exactly and must not be used for amounts.
