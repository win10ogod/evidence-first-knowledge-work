import csv
import io

from .pricing import format_cents, line_total_cents

COLUMNS = ["sku", "name", "qty", "price", "total"]


def to_csv(items):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(COLUMNS)
    for item in items:
        writer.writerow([item.sku, item.name, item.qty, format_cents(item.price_cents),
                         format_cents(line_total_cents(item))])
    return buffer.getvalue()
