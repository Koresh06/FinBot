from aiogram.fsm.state import State, StatesGroup


class AddTransaction(StatesGroup):
    start = State()


class TransactionDefault(StatesGroup):
    start = State()
    cat = State()
    total_sum = State()
    comment = State()
    confirm = State()


class TransactionFromTextAI(StatesGroup):
    start = State()