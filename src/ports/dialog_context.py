from typing import Protocol


class DialogContextProtocol(Protocol):
    """
    Протокол для управления контекстом диалога пользователя.

    Методы:
    - update_and_get_dialog: добавляет подписанное новое сообщение в контекст
      указанного пользователя и возвращает список словарей с обновленным
      контекстом, где каждый словарь содержит 1 сообщение из диалога.
      Подпись определяется параметром role ('user' или 'assistant').
    - reset_dialog: сбрасывает контекст диалога для указанного пользователя.
    Метод хранения диалога определяется реализацией протокола.
    """

    async def update_and_get_dialog(
        self,
        user_id: int,
        role: str,
        content: str
    ) -> list[dict[str, str]]:
        pass

    async def reset_dialog(
        self,
        user_id: int
    ) -> None:
        pass
