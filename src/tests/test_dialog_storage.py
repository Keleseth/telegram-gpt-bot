from src.adapters.in_memory_storage import InMemoryDialogStorage
from src.bot.core.constants import (
	ASSISTANT_ROLE,
	CONTENT,
	GPT_SYSTEM_PROMPT,
	ROLE,
	SYSTEM,
	USER_ROLE,
)
from src.tests.constants import (
    ASSISTANT_RESPONSE_1,
    FIRST_USER_FIRST_MESSAGE,
	FIRST_USER_SECOND_MESSAGE,
    SECOND_USER_FIRST_MESSAGE,
)


async def test_first_user_starts_with_prompt(
	storage: InMemoryDialogStorage,
	user_id: int
):
	dialog = await storage.update_and_get_dialog(
		user_id,
		USER_ROLE,
		FIRST_USER_FIRST_MESSAGE
    )
	assert len(dialog) == 2
	assert dialog[0] == GPT_SYSTEM_PROMPT
	assert dialog[1][ROLE] == USER_ROLE
	assert dialog[1][CONTENT] == FIRST_USER_FIRST_MESSAGE


async def test_storage_dialog_preserver_order(
		storage: InMemoryDialogStorage,
		user_id: int
):
	await storage.update_and_get_dialog(
		user_id,
		USER_ROLE,
		FIRST_USER_FIRST_MESSAGE
    )
	dialog = await storage.update_and_get_dialog(
		user_id,
		ASSISTANT_ROLE,
		ASSISTANT_RESPONSE_1
    )
	dialog = await storage.update_and_get_dialog(
		user_id,
		USER_ROLE,
		FIRST_USER_SECOND_MESSAGE
    )
	roles_sequence = [message[ROLE] for message in dialog]
	assert roles_sequence == [SYSTEM, USER_ROLE, ASSISTANT_ROLE, USER_ROLE]
	assert dialog[-1][CONTENT] == FIRST_USER_SECOND_MESSAGE

async def test_reset_dialog_leaves_only_system_prompt(
	storage_with_one_message: InMemoryDialogStorage, user_id: int
):
	await storage_with_one_message.reset_dialog(user_id)
	assert user_id in storage_with_one_message.dialogs
	dialog = storage_with_one_message.dialogs[user_id]
	assert len(dialog) == 1
	assert dialog == [GPT_SYSTEM_PROMPT]


async def test_system_prompt_not_duplicated(
	storage: InMemoryDialogStorage,
    user_id: int
):
	await storage.update_and_get_dialog(
		user_id,
		USER_ROLE,
		FIRST_USER_FIRST_MESSAGE
    )
	await storage.update_and_get_dialog(
		user_id,
        ASSISTANT_ROLE,
        ASSISTANT_RESPONSE_1
    )
	await storage.update_and_get_dialog(
		user_id,
		USER_ROLE,
		FIRST_USER_SECOND_MESSAGE
    )
	dialog = storage.dialogs[user_id]
	system_prompts = [
		message for message in dialog if message == GPT_SYSTEM_PROMPT
    ]
	assert len(system_prompts) == 1


async def test_dialogs_are_separted_between_users(
    storage_with_one_message: InMemoryDialogStorage,
    user_id: int,
    second_user_id: int
):
    await storage_with_one_message.update_and_get_dialog(
        second_user_id,
        USER_ROLE,
        SECOND_USER_FIRST_MESSAGE
    )
    dialog_user_1 = storage_with_one_message.dialogs[user_id]
    dialog_user_2 = storage_with_one_message.dialogs[second_user_id]
    assert len(dialog_user_1) == 2
    assert len(dialog_user_2) == 2
    assert (
		FIRST_USER_FIRST_MESSAGE in dialog_user_1[1][CONTENT]
		and SECOND_USER_FIRST_MESSAGE not in dialog_user_1[1][CONTENT]
    )
    assert (
		SECOND_USER_FIRST_MESSAGE in dialog_user_2[1][CONTENT]
        and FIRST_USER_FIRST_MESSAGE not in dialog_user_2[1][CONTENT]
    )


async def test_reset_dialog_not_affects_other_user(
    storage_with_one_message: InMemoryDialogStorage,
    user_id: int,
    second_user_id: int
):
    await storage_with_one_message.update_and_get_dialog(
        second_user_id,
        USER_ROLE,
        SECOND_USER_FIRST_MESSAGE
    )
    await storage_with_one_message.reset_dialog(user_id)
    dialog_user_1 = storage_with_one_message.dialogs[user_id]
    dialog_user_2 = storage_with_one_message.dialogs[second_user_id]
    assert len(dialog_user_1) == 1
    assert len(dialog_user_2) == 2
    assert (
        SECOND_USER_FIRST_MESSAGE in dialog_user_2[1][CONTENT]
        and FIRST_USER_FIRST_MESSAGE not in dialog_user_2[1][CONTENT]
    )
