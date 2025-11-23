# Телеграм-бот с интеграцией Grok (Aiogram + Grok)

Лёгкий MVP‑бот для **Telegram**, который интегрируется с моделью **Grok** (через Groq API), ведёт контекст диалога и поддерживает его сброс. Архитектура модульная (ports/adapters/middlewares/handlers) с упором на расширяемость: для mvp in-memory - дефолтное хранение диалога, можно подменить на свою реализацию (в планах Redis).

## Стек технологий
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/aiogram-2F80ED?style=for-the-badge&logo=telegram&logoColor=white)
![Groq](https://img.shields.io/badge/groq-FF6B2B?style=for-the-badge&logo=openai&logoColor=white)
![Pydantic](https://img.shields.io/badge/pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Logging](https://img.shields.io/badge/logging-525252?style=for-the-badge&logo=python&logoColor=white)

---

## Описание проекта
MVP закрывает требования тестового задания:
- Команды `/start` и `/help` и удобные пользовательские кнопки для этих операций.
- Любое текстовое сообщение отправляется модели и получает ответ с учётом истории.
- История диалога хранится отдельно для каждого пользователя (in‑memory) и используется при генерации ответов.
- Сброс контекста через `/start` и кнопку "Начать новый диалог".
- Простое логирование ошибок (таймауты, исключения).

Пока без: Redis, тестов, CI/CD, тримминга истории, метрик. Эти улучшения запланированы.

## Архитектура и компоненты
### 1. Хранилище диалога (InMemory)
`src/adapters/in_memory_storage.py` — `InMemoryDialogStorage` хранит список сообщений формата `{role, content}`. Системный промпт добавляется при сбросе. Реализация соответствует протоколу `DialogContextProtocol`.

### 2. Протокол контекста
`src/ports/dialog_context.py` — определяет контракт для любых хранилищ (будущий Redis). Методы: `update_and_get_dialog`, `reset_dialog`.

### 3. Handlers
`commands.py`: `/start`, `/help`, кнопка сброса.  
`messages.py`: основной обработчик текста — обновляет контекст, обращается к Grok, добавляет ответ.

### 4. Middleware
`DialogStorageMiddleware` — прокидывает хранилище.  
`GrokAsyncClientMiddleware` — прокидывает асинхронный клиент Groq только в handler обработки сообщений.

### 5. Интеграция с Groq
Используется `AsyncGroq`. Ошибки таймаута и общие исключения логируются и возвращают пользователю fallback‑сообщение.

### 6. Клавиатура
`main_keyboards.py` — две кнопки: сброс диалога и помощь.

### 7. Логирование
Централизованное в `main.py` функцией setup_logging (файл `logs/app.log` + консоль). Логируются только ошибки (timeout, unexpected exception).

### 8. Конфигурация
`config.py` — pydantic settings: токены, модель, таймауты (минимальный набор). Секреты через `.env`.

### Переменные окружения (.env)
```
BOT_TOKEN — Ваш токен телеграм бота
GROK_API_KEY — Ваш токен API Grok
GROK_MODEL — Желаемая модель Grok, есть дефолтная.
GROK_REQUEST_TIMEOUT — Время ожидания ответа от Grok в секундах, есть дефолтное.
BOT_REQUEST_TIMEOUT — Время ожидания ответа от бота в секунлах, есть дефолтное.
# ДЛя Redis переменные будут добавлены позже.
```

## Быстрый старт (локально, без docker)
1. Клонировать репозиторий:
```bash
git clone https://github.com/Keleseth/telegram-gpt-bot
cd telegram-gpt-bot
```
2. Создать `.env` по примеру выше.
3. Установить зависимости из файла dev_requirements.txt если нужно выполнять Pytest тесты или requirements.txt для прод-версии:
```bash
pip install -r requirements.txt
```

4. Запустить:
```bash
python -m src.bot.main
```

## Запуск через Docker
1. Клонировать репозиторий:
```bash
git clone https://github.com/Keleseth/telegram-gpt-bot
cd telegram-gpt-bot
```
2. Создать `.env` по примеру выше.
Билд и запуск контейнера:
```bash
docker compose up -d --build
```
Логи будут писаться в консоль. По желанию можно добавить Volume для хранения логов

## Планы по улучшению
1. Redis хранилище (LPUSH + LTRIM для истории диалога).
2. Расширить базу тестов. Добавить к существующим Unit-тесты для handlers бота, а также интеграционные тесты.
3. CI/CD (GitHub Actions: lint, tests, build image).
4. Тримминг истории или.
5. Лимитированеи для пользователей.
7. Расширяемая конфигурация модели - ООП реализация модели.

---

Проект разработан Келесидисом Александром. GitHub: [Keleseth](https://github.com/Keleseth)