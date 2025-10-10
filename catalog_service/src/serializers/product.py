from datetime import datetime
from uuid import UUID

import ujson


def serialize_product(product: dict) -> str:
    # product["created_at"] = product["created_at"].isoformat()
    product["id"] = str(product["id"])
    return ujson.dumps(product)


def deserialize_product(json_str: str) -> dict:
    product = ujson.loads(json_str)
    # product["created_at"] = datetime.fromisoformat(product["created_at"])
    product["id"] = UUID(product["id"])
    return product
