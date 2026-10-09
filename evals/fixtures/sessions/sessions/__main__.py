import json
import sys

from sessions.parse import read_events
from sessions.summary import summarise


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    print(json.dumps(summarise(read_events(argv[0])), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
