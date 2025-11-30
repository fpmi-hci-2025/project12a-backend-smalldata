import asyncio
import httpx
from config import config


class NotifictionManager:

    async def send_message(self, message: str) -> None:
        # Print to console for debugging
        print(f"[NOTIFICATION] {message}")
        
        # Send to Telegram
        try:
            await self._send_telegram_message(message)
        except Exception as e:
            print(f"[ERROR] Failed to send Telegram message: {e}")

    async def _send_telegram_message(self, message: str) -> None:
        """Send message to Telegram chat"""
        url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
        
        payload = {
            "chat_id": config.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            print(f"[TELEGRAM] Message sent successfully: {response.status_code}")
