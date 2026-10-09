import argparse
import sys
from decimal import Decimal, InvalidOperation

from . import store
from .export import to_csv
from .model import Item
from .pricing import format_cents
from .report import low_stock, stock_value_cents


def _price_cents(text):
    try:
        value = Decimal(text)
    except InvalidOperation:
        raise SystemExit("error: price must be a decimal amount") from None
    if value < 0 or value != value.quantize(Decimal("0.01")):
        raise SystemExit("error: price must be a decimal amount")
    return int(value * 100)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="inventory")
    parser.add_argument("--file", default="inventory.json")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("--sku", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--qty", type=int, required=True)
    add.add_argument("--price", required=True)
    commands.add_parser("list")
    commands.add_parser("export")
    commands.add_parser("value")
    low = commands.add_parser("low")
    low.add_argument("--below", type=int, default=5)
    args = parser.parse_args(argv)

    items = store.load(args.file)
    if args.command == "add":
        items = [item for item in items if item.sku != args.sku]
        items.append(Item(args.sku, args.name, args.qty, _price_cents(args.price)))
        items.sort(key=lambda item: item.sku)
        store.save(args.file, items)
    elif args.command == "list":
        for item in items:
            print(f"{item.sku}  {item.name}  qty={item.qty}  price={format_cents(item.price_cents)}")
    elif args.command == "export":
        sys.stdout.write(to_csv(items))
    elif args.command == "value":
        print(f"stock value: {format_cents(stock_value_cents(items))}")
    elif args.command == "low":
        for item in low_stock(items, args.below):
            print(f"{item.sku}  qty={item.qty}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
