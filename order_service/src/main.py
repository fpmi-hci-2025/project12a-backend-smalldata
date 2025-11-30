import contextlib
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, Body, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from auth import authorize, authorize_admin
from config import config
from dependencies import get_message_broker
from db.session import get_session, Base, engine
from db.models import OrderStatus
from exceptions.order import OrderNotFoundError
from services.order import OrderService
from schemas.order import OrderStatusUpdateRequest


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    message_broker = RabbitBroker(
        f"amqp://{config.rabbitmq_user}:{config.rabbitmq_password}"
        f"@{config.rabbitmq_host}:{config.rabbitmq_port}/"
    )
    await message_broker.connect()
    app.dependency_overrides[get_message_broker] = lambda: message_broker
    yield
    await message_broker.close()


app = FastAPI(
    title="Order Service API",
    version="1.0",
    docs_url="/api/docs",
    openapi_url="/orders-openapi.json",
    lifespan=lifespan
)

# Security scheme for Swagger
security = HTTPBearer()

async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin token for Swagger UI"""
    if credentials.credentials != config.admin_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing admin API token"
        )
    return credentials


@app.get("/api/orders/{order_id}")
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    service = OrderService(session=session, broker=broker)
    try:
        order = await service.get_order_by_id(order_id)
        # Convert enum to string for JSON response
        return {
            "id": order.id,
            "product_id": str(order.product_id),
            "status": order.status.value,
            "amount": order.amount,
            "price": order.price,
            "created_at": order.created_at.isoformat(),
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None,
        }
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


@app.post("/api/orders")
async def create_order(
    product_id: UUID = Body(...),
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    service = OrderService(session=session, broker=broker)
    try:
        order = await service.create_order(product_id)
        # Convert enum to string for JSON response
        return {
            "id": order.id,
            "product_id": str(order.product_id),
            "status": order.status.value,
            "amount": order.amount,
            "price": order.price,
            "created_at": order.created_at.isoformat(),
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Admin endpoints
@app.get("/api/orders", dependencies=[Depends(verify_admin_token)])
async def get_all_orders(
    limit: int = Query(default=100, le=1000, description="Limit results"),
    offset: int = Query(default=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    """Get all orders (admin only)"""
    service = OrderService(session=session, broker=broker)
    orders = await service.get_all_orders(limit=limit, offset=offset)
    
    # Convert to dict format for JSON response
    orders_data = []
    for order in orders:
        orders_data.append({
            "id": order.id,
            "product_id": str(order.product_id),
            "status": order.status.value,
            "amount": order.amount,
            "price": order.price,
            "created_at": order.created_at.isoformat(),
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None,
        })
    
    return {
        "orders": orders_data,
        "total": len(orders_data),
        "limit": limit,
        "offset": offset
    }


@app.patch("/api/orders/{order_id}", dependencies=[Depends(verify_admin_token)])
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdateRequest,
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    """Update order status (admin only)"""
    service = OrderService(session=session, broker=broker)
    try:
        updated_order = await service.update_order_status(order_id, status_update.status)
        return {
            "id": updated_order.id,
            "product_id": str(updated_order.product_id),
            "status": updated_order.status.value,
            "amount": updated_order.amount,
            "price": updated_order.price,
            "created_at": updated_order.created_at.isoformat(),
            "paid_at": updated_order.paid_at.isoformat() if updated_order.paid_at else None,
            "shipped_at": updated_order.shipped_at.isoformat() if updated_order.shipped_at else None,
            "delivered_at": updated_order.delivered_at.isoformat() if updated_order.delivered_at else None,
        }
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/api/orders/{order_id}/confirm",
    # dependencies=[Depends(authorize)]
)
async def confirm_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    service = OrderService(session=session, broker=broker)
    try:
        return await service.confirm_order(order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
