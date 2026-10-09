"""Reading and writing the inventory file. The format rules are in docs/storage.md."""

import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from .model import Item

CURRENT_FORMAT = 2


def _v1_to_v2(data):
    # Format 1 stored `price` as a float number of dollars.
    items = []
    for item in data["items"]:
        item = dict(item)
        dollars = Decimal(str(item.pop("price")))
        item["price_cents"] = int((dollars * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        items.append(item)
    return {"format": 2, "items": items}


# MIGRATIONS[n] turns a format-n document into a format-(n+1) document.
MIGRATIONS = {1: _v1_to_v2}


def load(path):
    path = Path(path)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    version = data.get("format", 1)
    if version > CURRENT_FORMAT:
        raise ValueError(f"unsupported format {version}")
    while version < CURRENT_FORMAT:
        data = MIGRATIONS[version](data)
        version += 1
    return [Item.from_dict(item) for item in data["items"]]


def save(path, items):
    document = {"format": CURRENT_FORMAT, "items": [item.to_dict() for item in items]}
    Path(path).write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
