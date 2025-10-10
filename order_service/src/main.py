import contextlib
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, Body
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from auth import authorize
from config import config
from dependencies import get_message_broker
from db.session import get_session, Base, engine
from exceptions.order import OrderNotFoundError
from services.order import OrderService


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


app = FastAPI(lifespan=lifespan)


@app.get("/api/orders/{order_id}")
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    service = OrderService(session=session, broker=broker)
    try:
        return await service.get_order_by_id(order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


@app.post("/api/orders/init")
async def init_order(
    product_id: UUID = Body(...),
    session: AsyncSession = Depends(get_session),
    broker: RabbitBroker = Depends(get_message_broker),
):
    service = OrderService(session=session, broker=broker)
    try:
        return await service.create_order(product_id)
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
