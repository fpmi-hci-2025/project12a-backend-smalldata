from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ProductDTO:
    id: UUID
    title: str
    category_id: int
    description: str
    characteristics: dict
    created_at: datetime
    amount: int
    price: float
