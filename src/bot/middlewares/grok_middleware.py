from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from groq import AsyncGroq


class GrokAsyncClientMiddleware(BaseMiddleware):
    """
    Прокидывает в обработчики событий асинхронный клиент Grok.
    """
    def __init__(self, client: AsyncGroq):
        super().__init__()
        self.client = client

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: dict,
    ):
        data['grok_async_client'] = self.client
        return await handler(event, data)
