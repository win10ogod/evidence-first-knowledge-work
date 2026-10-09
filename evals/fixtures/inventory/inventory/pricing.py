def format_cents(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def line_total_cents(item):
    return item.qty * item.price_cents
