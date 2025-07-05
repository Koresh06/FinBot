from aiogram.fsm.state import State, StatesGroup


class TransactionFromTextAI(StatesGroup):
    start = State()
    confirm = State()