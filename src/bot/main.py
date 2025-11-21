import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from groq import AsyncGroq

from src.bot.core.logger_messages import (
    BOT_STARTED,
    BOT_STARTUP_ERROR,
    LOGGER_BOT_STARTED,
    LOGGER_BOT_STARTUP_ERROR
)
from src.bot.handlers import commands_router, messages_router
from src.bot.middlewares.dialog_storage_middleware import (
    DialogStorageMiddleware
)
from src.bot.middlewares.grok_middleware import (
    GrokAsyncClientMiddleware
)
from src.bot.utils import (
    create_dialog_storage,
    setup_logging
)
from src.config import settings


async def main():
    setup_logging()
    try:
        session = AiohttpSession(
            timeout=settings.bot_request_timeout
        )
        bot = Bot(
            token=settings.bot_token.get_secret_value(),
            session=session,
            default=DefaultBotProperties(
                parse_mode=None
            )
        )
        dp = Dispatcher()
        dialog_storage = create_dialog_storage(settings)
        dp.include_router(commands_router)
        dp.message.middleware(DialogStorageMiddleware(dialog_storage))
        grok_async_client = AsyncGroq(
            api_key=settings.grok_api_key.get_secret_value(),
            timeout=settings.grok_request_timeout,
        )
        messages_router.message.middleware(
            GrokAsyncClientMiddleware(grok_async_client)
        )
        dp.include_router(messages_router)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            skip_updates=True
        )
        logging.info(LOGGER_BOT_STARTED)
    except Exception:
        logging.error(LOGGER_BOT_STARTUP_ERROR, exc_info=True)
    finally:
        await bot.session.close()
        await grok_async_client.close()


if __name__ == '__main__':
    asyncio.run(main())
