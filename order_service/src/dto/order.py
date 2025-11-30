from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from db.models import OrderStatus


@dataclass
class OrderDTO:
    id: int
    product_id: UUID
    status: OrderStatus
    amount: int
    price: float
    created_at: datetime
    paid_at: datetime | None
    shipped_at: datetime | None
    delivered_at: datetime | None
