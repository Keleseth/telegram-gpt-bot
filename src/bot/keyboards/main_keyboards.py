from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bot.constants import (
    HELP_BUTTON,
    RESET_DIALOG_BUTTON
)


def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=RESET_DIALOG_BUTTON))
    kb.row(KeyboardButton(text=HELP_BUTTON))
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
