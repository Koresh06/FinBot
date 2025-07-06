from typing import Any, cast
from logging import getLogger

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from src.application.containers.container import Container
from src.application.use_cases.intarface import (
    UseCaseMultipleEntities,
    UseCaseOneEntity,
)
from src.domain.entities.category import CategoryEntity
from src.domain.entities.transaction import TransactionEntity
from src.presentation.bot.logic.transactions.add_ai.query import InvalidTransactionTextError, parse_text_with_ai
from src.presentation.bot.logic.transactions.add_ai.states import TransactionFromTextAI
from src.presentation.bot.logic.transactions.add_default.states import (
    AddTransaction,
)


logger = getLogger(__name__)


async def on_success_handler(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    text: str = dialog_manager.find("text").get_value()
    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    use_case: UseCaseMultipleEntities[CategoryEntity] = container.get_all_categories_uc()

    categories: list[CategoryEntity] = await use_case.execute()
    lst_names_categories: list[str] = [cat.name for cat in categories]

    try:
        result: dict = await parse_text_with_ai(text=text, categories=lst_names_categories)
    except InvalidTransactionTextError as e:
        await message.answer(
            "⚠️ *Не удалось распознать транзакцию.*\n\n"
            "Пожалуйста, попробуйте сформулировать сообщение иначе, "
            "например: «Вчера получил зарплату 100000».\n\n"
            "Если ошибка повторится, попробуйте уточнить детали."
        )
        return
    except Exception as e:
        logger.error(f"Ошибка при обращении к AI API: {e}")
        await message.answer("❌ Ошибка сервера. Попробуйте ещё раз позже.")
        return

    dialog_manager.dialog_data["result_ai"] = result
    await dialog_manager.next()




async def confirm_transaction_ai_handler(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    data: dict = dialog_manager.dialog_data["result_ai"]

    container: Container = cast(Container, dialog_manager.middleware_data["container"])
    use_case: UseCaseOneEntity[TransactionEntity] = container.add_transaction_uc()

    await use_case.execute(tg_id=callback.from_user.id, data=data)

    await callback.answer("✅ Транзакция успешно добавлена")
    logger.info(
        f"Пользователь: {callback.from_user.id} добавил AI транзакцию : тип - {data['type']}, категория - {data['category']}, сумма - {data['total_sum']}"
    )

    await dialog_manager.start(
        state=AddTransaction.start,
        show_mode=ShowMode.EDIT,
    )
