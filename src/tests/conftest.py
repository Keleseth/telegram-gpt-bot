import pytest

from src.adapters.in_memory_storage import InMemoryDialogStorage
from src.bot.core.constants import GPT_SYSTEM_PROMPT, USER_ROLE
from src.tests.constants import (
	FIRST_USER_ID,
	FIRST_USER_FIRST_MESSAGE,
	SECOND_USER_FIRST_MESSAGE,
	SECOND_USER_ID
)


@pytest.fixture()
def user_id() -> int:
	return FIRST_USER_ID

@pytest.fixture()
def second_user_id() -> int:
	return SECOND_USER_ID


@pytest.fixture()
def storage() -> InMemoryDialogStorage:
	return InMemoryDialogStorage()


@pytest.fixture()
async def storage_with_one_message(storage: InMemoryDialogStorage, user_id: int):
	await storage.update_and_get_dialog(
		user_id,
		USER_ROLE,
		FIRST_USER_FIRST_MESSAGE
    )
	return storage


@pytest.fixture()
async def storage_one_message_for_two_users(
	storage: InMemoryDialogStorage,
    user_id: int,
    second_user_id: int
):
    await storage.update_and_get_dialog(
        user_id,
        USER_ROLE,
        FIRST_USER_FIRST_MESSAGE
    )
    await storage.update_and_get_dialog(
        second_user_id,
        USER_ROLE,
        SECOND_USER_FIRST_MESSAGE
    )
    return storage
