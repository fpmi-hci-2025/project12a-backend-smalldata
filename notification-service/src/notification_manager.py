import asyncio


class NotifictionManager:

    async def send_message(self, message: str) -> None:
        await asyncio.sleep(0.15)
        print(message)
