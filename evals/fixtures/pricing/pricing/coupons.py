COUPONS = {"WELCOME10": 10, "VIP25": 25}


def apply_coupon(rates, coupon):
    """Return the rate table to use for a quote with `coupon`."""
    if coupon:
        rates["discount_pct"] = COUPONS[coupon]
    return rates
