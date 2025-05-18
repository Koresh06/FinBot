from aiogram.fsm.state import State, StatesGroup


class AddTransaction(StatesGroup):
    start = State()


class TransactionDefault(StatesGroup):
    start = State()
    cat = State()


class TransactionFromTextAI(StatesGroup):
    start = State()