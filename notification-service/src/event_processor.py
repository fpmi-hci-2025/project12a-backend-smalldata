from faststream import FastStream
from faststream.rabbit import RabbitBroker

from config import Settings
from notification_manager import NotifictionManager


config = Settings()

broker = RabbitBroker(
    f"amqp://{config.rabbitmq_user}:{config.rabbitmq_password}"
    f"@{config.rabbitmq_host}:{config.rabbitmq_port}/"
)

app = FastStream(broker)


@broker.subscriber(queue="rabbitmq_notifications_queue")
async def notification_listener(message: str) -> None:
    notification_manager = NotifictionManager()
    await notification_manager.send_message(
        message=message,
    )
