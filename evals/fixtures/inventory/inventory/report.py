def stock_value_cents(items):
    return sum(item.qty * item.price_cents for item in items)


def low_stock(items, threshold):
    return sorted((item for item in items if item.qty < threshold), key=lambda item: item.sku)
