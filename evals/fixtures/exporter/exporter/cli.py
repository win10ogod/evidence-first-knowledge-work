import argparse
import json
import sys

from exporter.registry import REGISTRY


def main(argv=None):
    parser = argparse.ArgumentParser(prog="exporter")
    parser.add_argument("--format", required=True, choices=sorted(REGISTRY))
    args = parser.parse_args(argv)
    records = json.load(sys.stdin)
    sys.stdout.write(REGISTRY[args.format](records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
