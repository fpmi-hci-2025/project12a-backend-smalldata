from datetime import datetime
from uuid import UUID
from enum import Enum

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True,
    )
    product_id: Mapped[UUID]
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.CREATED)
    amount: Mapped[int]
    price: Mapped[float]
    created_at: Mapped[datetime]
    paid_at: Mapped[datetime | None]
    shipped_at: Mapped[datetime | None]
    delivered_at: Mapped[datetime | None]
