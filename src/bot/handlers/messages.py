import logging

from aiogram import Router, F
from aiogram.types import Message
from groq import AsyncGroq, APITimeoutError

from src.bot.core.constants import (
    ASSISTANT_ROLE,
    USER_ROLE
)
from src.bot.core.errors import (
    GROK_EMPTY_RESPONSE_ERROR,
    GROK_TIMEOUT_ERROR,
    REQUEST_PROCESSING_ERROR
)
from src.bot.core.logger_messages import (
    LOGGER_GROK_PROCESSING_ERROR,
    LOGGER_GROK_TIMEOUT_ERROR
)
from src.config import settings
from src.ports.dialog_context import DialogContextProtocol


router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text)
async def handle_user_message(
    message: Message,
    dialog_storage: DialogContextProtocol,
    grok_async_client: AsyncGroq
):
    dialog_context = await dialog_storage.update_and_get_dialog(
        user_id=message.from_user.id,
        role=USER_ROLE,
        content=message.text
    )
    try:
        response = await grok_async_client.chat.completions.create(
            model=settings.grok_model,
            messages=dialog_context
        )
        assistant_message = (
            response.choices[0].message.content
            if getattr(response, 'choices', None)
            and len(response.choices) > 0
            and getattr(response.choices[0], 'message', None)
            else None
        )
        if not assistant_message:
            await message.answer(
                text=GROK_EMPTY_RESPONSE_ERROR
            )
            return
    except APITimeoutError:
        logger.error(LOGGER_GROK_TIMEOUT_ERROR.format(
            user_id=message.from_user.id)
        )
        await message.answer(
            GROK_TIMEOUT_ERROR
        )
        return
    except Exception:
        logger.exception(LOGGER_GROK_PROCESSING_ERROR.format(
            user_id=message.from_user.id)
        )
        await message.answer(
            text=REQUEST_PROCESSING_ERROR
        )
        return
    await dialog_storage.update_and_get_dialog(
        user_id=message.from_user.id,
        role=ASSISTANT_ROLE,
        content=assistant_message
    )
    await message.answer(
        text=assistant_message
    )
