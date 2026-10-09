def parse_amount(text):
    """Parse a decimal string from the input file."""
    return float(text)


def round_cents(value):
    """Round an amount to the cent."""
    return round(value, 2)


def format_amount(value):
    return f"{value:.2f}"
