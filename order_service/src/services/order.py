from datetime import datetime
from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from faststream.rabbit import RabbitBroker

from config import config
from db.models import Order, OrderStatus
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
            status=OrderStatus.CREATED,
            amount=1,
            price=0.0,
            created_at=datetime.utcnow(),
            paid_at=None,
            shipped_at=None,
            delivered_at=None,
        )
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)

        # Send notification about new order
        await self.broker.publish(
            queue=config.rabbitmq_notifications_queue,
            message=f"Новый заказ создан! ID: {new_order.id}, Товар: {product_id}"
        )

        return self._map_to_dto(new_order)

    async def confirm_order(self, order_id: int) -> OrderDTO:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise OrderNotFoundError(order_id)
        if order.status == OrderStatus.PAID:
            raise ValueError("Order already paid")

        order.status = OrderStatus.PAID
        order.paid_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(order)

        await self.broker.publish(
            queue=config.rabbitmq_notifications_queue,
            message=f"Заказ #{order_id} оплачен!"
        )

        return self._map_to_dto(order)

    async def get_all_orders(self, limit: int = 100, offset: int = 0) -> List[OrderDTO]:
        """Get all orders with pagination (admin only)"""
        result = await self.session.execute(
            select(Order)
            .order_by(Order.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        orders = result.scalars().all()
        return [self._map_to_dto(order) for order in orders]

    async def update_order_status(self, order_id: int, new_status: OrderStatus) -> OrderDTO:
        """Update order status (admin only)"""
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            raise OrderNotFoundError(order_id)

        # Update status and corresponding timestamp
        old_status = order.status
        order.status = new_status
        current_time = datetime.utcnow()

        if new_status == OrderStatus.PAID and old_status != OrderStatus.PAID:
            order.paid_at = current_time
        elif new_status == OrderStatus.SHIPPED and old_status != OrderStatus.SHIPPED:
            order.shipped_at = current_time
        elif new_status == OrderStatus.DELIVERED and old_status != OrderStatus.DELIVERED:
            order.delivered_at = current_time

        await self.session.commit()
        await self.session.refresh(order)

        # Send notification about status change
        status_messages = {
            OrderStatus.PAID: f"Заказ #{order_id} оплачен!",
            OrderStatus.SHIPPED: f"Заказ #{order_id} отправлен!",
            OrderStatus.IN_TRANSIT: f"Заказ #{order_id} в пути!",
            OrderStatus.DELIVERED: f"Заказ #{order_id} доставлен!",
            OrderStatus.CANCELLED: f"Заказ #{order_id} отменен!"
        }
        
        if new_status in status_messages:
            await self.broker.publish(
                queue=config.rabbitmq_notifications_queue,
                message=status_messages[new_status]
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
            shipped_at=order.shipped_at,
            delivered_at=order.delivered_at,
        )
