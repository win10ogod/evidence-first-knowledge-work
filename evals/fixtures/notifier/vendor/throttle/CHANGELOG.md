# Changelog

## 2.1.0
- `Throttle` accepts injectable `clock` and `sleep` callables for testing.

## 2.0.0
- **Breaking:** `period` is now given in **milliseconds** (it was seconds in 1.x), to allow
  sub-second windows without floats.
- Sliding-window algorithm replaces the fixed window.

## 1.2.0
- First vendored version.
