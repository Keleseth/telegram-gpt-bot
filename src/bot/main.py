import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from src.bot.handlers import commands_router
from src.bot.middlwares.dialog_storage_middleware import (
    DialogStorageMiddleware
)
from src.bot.utils import create_dialog_storage
from src.config import settings


async def main():

    session = AiohttpSession(
        timeout=30
    )

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()
    dialog_storage = create_dialog_storage(settings)
    dp['dialog_storage'] = dialog_storage
    dp.include_router(commands_router)
    dp.message.middleware(DialogStorageMiddleware(dialog_storage))
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            skip_updates=True
        )
    except Exception as e:
        print('Ошибка при запуске бота:', e)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
