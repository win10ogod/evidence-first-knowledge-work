from pricing.coupons import apply_coupon
from pricing.rates import load_rates


def quote(region, amount_cents, coupon=None):
    rates = apply_coupon(load_rates(region), coupon)
    net = amount_cents * (100 - rates.get("discount_pct", 0)) // 100
    return net + net * rates["vat_pct"] // 100
