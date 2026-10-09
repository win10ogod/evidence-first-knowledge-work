import json
import tempfile
import unittest
from pathlib import Path

from inventory import store
from inventory.model import Item

DATA = Path(__file__).parent / "data"


class StoreTest(unittest.TestCase):
    def test_round_trip(self):
        items = [Item("A1", "Widget", 3, 1250)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inv.json"
            store.save(path, items)
            self.assertEqual(store.load(path), items)
            self.assertEqual(json.loads(path.read_text())["format"], store.CURRENT_FORMAT)

    def test_format1_still_loads(self):
        items = store.load(DATA / "format1.json")
        self.assertEqual([(i.sku, i.price_cents) for i in items], [("A1", 1250), ("D4", 29)])

    def test_newer_format_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inv.json"
            path.write_text(json.dumps({"format": store.CURRENT_FORMAT + 1, "items": []}))
            with self.assertRaisesRegex(ValueError, "unsupported format"):
                store.load(path)


if __name__ == "__main__":
    unittest.main()
