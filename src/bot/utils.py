import logging
import os

from pydantic_settings import BaseSettings

from src.config import settings
from src.adapters.in_memory_storage import InMemoryDialogStorage
from src.ports.dialog_context import DialogContextProtocol


def setup_logging() -> None:
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format=settings.logs_format,
        handlers=[
            logging.FileHandler('logs/app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def create_dialog_storage(settings: BaseSettings) -> DialogContextProtocol:
    """
    Создает репозиторий для хранения контекста диалога в зависимости от
    настроек приложения.
    """
    if settings.redis_url:
        return InMemoryDialogStorage()
    return InMemoryDialogStorage()
