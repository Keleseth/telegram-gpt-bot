from aiogram import F, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.bot.constants import (
    GREETING,
    HELP,
    HELP_BUTTON,
    RESET_DIALOG_BUTTON
)
from src.bot.keyboards.main_keyboards import main_kb
from src.ports.dialog_context import DialogContextProtocol

router = Router()


@router.message(CommandStart())
@router.message(F.text == RESET_DIALOG_BUTTON)
async def cmd_start(
    message: Message,
    dialog_storage: DialogContextProtocol
):
    """
    Обработчик команды /start: Приветствует пользователя, стирает текущий
    диалог пользователя с ботом и отправляет главную клавиатуру.
    """
    user_name = message.from_user.first_name or 'путник'
    await dialog_storage.reset_dialog(user_id=message.from_user.id)
    await message.answer(
        text=GREETING.format(name=user_name),
        reply_markup=main_kb(),
    )


@router.message(F.text == HELP_BUTTON)
async def cmd_help(
    message: Message,
):
    """
    Обработчик команды помощи: отправляет информацию о боте.
    Обновляет главную клавиатуру для пользователя(если была затерта).
    """
    await message.answer(
        text=HELP,
        reply_markup=main_kb(),
    )
