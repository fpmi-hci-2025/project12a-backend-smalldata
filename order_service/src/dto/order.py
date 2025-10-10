from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class OrderDTO:
    id: int
    product_id: UUID
    status: str
    amount: int
    price: float
    created_at: datetime
    paid_at: datetime | None
