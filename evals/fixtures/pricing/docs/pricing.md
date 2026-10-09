# Pricing

- `quote(region, amount_cents, coupon=None)` returns the gross price in cents:
  apply the coupon's percentage discount (if any) to the amount, then add the region's VAT.
  Integer cents, rounding down at each step.
- Rate tables (`data/rates_<region>.json`) are large in production. Each region's file is read
  **once per process** and reused for every later quote; this caching is required for performance.
- Quotes are independent: one quote must never change the result of another.
