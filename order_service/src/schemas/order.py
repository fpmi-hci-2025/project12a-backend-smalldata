from pydantic import BaseModel
from db.models import OrderStatus


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus


class OrderListResponse(BaseModel):
    orders: list[dict]
    total: int
    limit: int
    offset: int