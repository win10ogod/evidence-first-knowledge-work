import csv

from billing.money import format_amount, parse_amount, round_cents


def read_lines(path):
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            if not row or row[0].startswith("#"):
                continue
            quantity = int(row[0])
            unit_price = parse_amount(row[1])
            discount = parse_amount(row[2]) if len(row) > 2 and row[2] else 0
            yield quantity, unit_price, discount


def line_total(quantity, unit_price, discount_pct=0):
    return round_cents(quantity * unit_price * (1 - discount_pct / 100))


def invoice_total(lines):
    return round_cents(sum(line_total(*line) for line in lines))


def render_total(path):
    return format_amount(invoice_total(read_lines(path)))
