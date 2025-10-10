from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from faststream.rabbit import RabbitBroker

from config import config
from db.models import Order
from dto.order import OrderDTO
from exceptions.order import OrderNotFoundError
from clients.catalog_client import CatalogClient


class OrderService:

    def __init__(self, session: AsyncSession, broker: RabbitBroker):
        self.session = session
        self.broker = broker

    async def get_order_by_id(self, order_id: int) -> OrderDTO:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise OrderNotFoundError(order_id)

        return self._map_to_dto(order)

    async def create_order(self, product_id: UUID) -> OrderDTO:
        exists = await CatalogClient.check_product_exists(product_id)
        if not exists:
            raise ValueError("Product does not exist in catalog")

        new_order = Order(
            product_id=product_id,
            status="created",
            amount=1,
            price=0.0,
            created_at=datetime.utcnow(),
            paid_at=None,
        )
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)

        return self._map_to_dto(new_order)

    async def confirm_order(self, order_id: int) -> OrderDTO:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise OrderNotFoundError(order_id)
        if order.status == "paid":
            raise ValueError("Order already paid")

        order.status = "paid"
        order.paid_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(order)

        await self.broker.publish(
            queue=config.rabbitmq_notifications_queue,
            message=f"Order with id={order_id} was confirmed!"
        )

        return self._map_to_dto(order)

    def _map_to_dto(self, order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id,
            product_id=order.product_id,
            status=order.status,
            amount=order.amount,
            price=order.price,
            created_at=order.created_at,
            paid_at=order.paid_at,
        )
