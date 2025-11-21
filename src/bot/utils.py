from pydantic_settings import BaseSettings

from src.adapters.in_memory_storage import InMemoryDialogStorage


def create_dialog_storage(settings: BaseSettings):
    """
    Создает репозиторий для хранения контекста диалога в зависимости от
    настроек приложения.
    """
    if settings.redis_url:
        return InMemoryDialogStorage()
    return InMemoryDialogStorage()
