from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.ports.dialog_context import DialogContextProtocol


class DialogStorageMiddleware(BaseMiddleware):
    """
    Прокидывает в обработчики событий хранилище диалога пользователя.
    """

    def __init__(self, storage: DialogContextProtocol) -> None:
        super().__init__()
        self._storage = storage

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: dict,
    ):
        data['dialog_storage'] = self._storage
        return await handler(event, data)
