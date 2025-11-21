from dataclasses import dataclass, field

from src.bot.core.constants import GPT_SYSTEM_PROMPT


@dataclass(slots=True)
class InMemoryDialogStorage:
    """
    Реализация хранилища диалогов in-memory.

    Хранит диалоги в оперативной памяти в виде словаря dialogs, где ключом
    является идентификатор пользователя(для телеграма это telegram_id),
    а значением - список сообщений диалога.
    """

    dialogs: dict[int, list[dict[str, str]]] = field(default_factory=dict)

    async def update_and_get_dialog(
        self,
        user_id: int,
        role: str,
        content: str
    ) -> list[dict[str, str]]:
        """
        Создает и/или обновляет диалог пользователя в памяти и возвращает
        обновленный список сообщений диалога.
        """
        user_dialog = self.dialogs.get(user_id, [GPT_SYSTEM_PROMPT])
        user_dialog.append(
            {
                'role': role,
                'content': content
            }
        )
        self.dialogs[user_id] = user_dialog
        return user_dialog

    async def reset_dialog(
        self,
        user_id: int
    ) -> None:
        """
        Стирает текущий диалог пользователя с ботом.
        """
        if user_id in self.dialogs:
            self.dialogs[user_id] = [GPT_SYSTEM_PROMPT]

    def __repr__(self):
        dialogs_count = len(self.dialogs)
        messages_total = sum(len(v) for v in self.dialogs.values())
        return f"InMemoryDialogStorage(dialogs={dialogs_count}, messages={messages_total})"