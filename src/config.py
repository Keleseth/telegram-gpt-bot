from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from src.bot.core.constants import DEFAULT_GROK_MODEL


class Settings(BaseSettings):
    """
    Настройки приложения.

    Атрибуты:
        bot_token: Токен Telegram бота.
        grok_api_key: API ключ для доступа к Grok.
        grok_model: Модель Grok с опцией по умолчанию.
        grok_request_timeout: Таймаут запросов к Grok в секундах.
        bot_request_timeout: Таймаут запросов бота в секундах.
        redis_url: URL для подключения к Redis (если используется).
        logs_format: Формат логов приложения.    
    """

    bot_token: SecretStr
    grok_api_key: SecretStr
    grok_model: str = DEFAULT_GROK_MODEL
    grok_request_timeout: int = 180
    bot_request_timeout: int = 30
    redis_url: str | None = None
    logs_format: str = '%(asctime)s %(levelname)s %(name)s: %(message)s'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
