import argparse
import sys

from fetcher import batch
from fetcher.client import Client
from fetcher.config import ConfigError, resolve


def build_parser():
    parser = argparse.ArgumentParser(prog="fetcher")
    parser.add_argument("--retries")
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("url")
    fetch_all = sub.add_parser("fetch-all")
    fetch_all.add_argument("path")
    return parser


def main(argv=None, out=None):
    out = out or sys.stdout
    args = build_parser().parse_args(argv)
    try:
        options = resolve({"retries": args.retries})
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.command == "fetch":
        client = Client(retries=options["retries"])
        out.write(f"{args.url} {len(client.get(args.url))}\n")
    else:
        batch.run(args.path, options, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
