import argparse

from billing.invoice import render_total


def main(argv=None):
    parser = argparse.ArgumentParser(prog="billing")
    sub = parser.add_subparsers(dest="command", required=True)
    invoice = sub.add_parser("invoice")
    invoice.add_argument("path")
    args = parser.parse_args(argv)
    print(render_total(args.path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
