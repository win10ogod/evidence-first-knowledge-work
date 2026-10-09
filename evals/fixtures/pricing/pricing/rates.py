import functools
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def _read_rates_file(region):
    with open(DATA / f"rates_{region}.json", encoding="utf-8") as handle:
        return json.load(handle)


@functools.lru_cache(maxsize=None)
def load_rates(region):
    """Rate tables are large: read each region's file once per process."""
    return _read_rates_file(region)
