from aiogram_dialog import DialogManager

from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Start, Button, Row, Group, Select, Back, Next
from aiogram_dialog.widgets.input import TextInput

from src.presentation.bot.logic.transactions.add_ai.states import TransactionFromTextAI
from src.presentation.bot.logic.transactions.add_ai.getters import getter_response_ai
from src.presentation.bot.logic.transactions.add_ai.handlers import confirm_transaction_ai_handler, on_success_handler


add_transaction_ai_dialog = Dialog(
    Window(
        Const(
            "🧠 *Умный разбор транзакции*\n\n"
            "Введите сообщение, например:\n"
            "📌 _«Вчера получил зарплату 100000»_\n\n"
            "Нейросеть автоматически определит тип, категорию, сумму и комментарий. ✨"
        ),
        TextInput(
            id="text",
            type_factory=str,
            on_success=on_success_handler,
        ),
        state=TransactionFromTextAI.start,
    ),
    Window(
        Format(
            "🧾 *Проверьте правильность данных:*\n\n"
            "💰 *Тип:* {type_tr}\n"
            "🏷 *Категория:* {cat}\n"
            "💸 *Сумма:* {total_sum} \n"
            "📝 *Комментарий:* {comment}"
        ),
        Button(
            text=Const("✅"),
            id="confirm",
            on_click=confirm_transaction_ai_handler,
        ),
        Back(Const("⬅️ Назад")),
        state=TransactionFromTextAI.confirm,
        getter=getter_response_ai,
    )
)
