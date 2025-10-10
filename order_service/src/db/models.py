from datetime import datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True,
    )
    product_id: Mapped[UUID]
    status: Mapped[str] = mapped_column(String(50))
    amount: Mapped[int]
    price: Mapped[float]
    created_at: Mapped[datetime]
    paid_at: Mapped[datetime | None]
