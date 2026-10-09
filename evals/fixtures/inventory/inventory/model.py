from dataclasses import dataclass


@dataclass
class Item:
    sku: str
    name: str
    qty: int
    price_cents: int

    def to_dict(self):
        return {"sku": self.sku, "name": self.name, "qty": self.qty, "price_cents": self.price_cents}

    @classmethod
    def from_dict(cls, data):
        return cls(data["sku"], data["name"], data["qty"], data["price_cents"])
