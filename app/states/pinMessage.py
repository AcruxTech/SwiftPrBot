from aiogram.dispatcher.filters.state import State, StatesGroup

class PinMessage(StatesGroup):
    waiting_for_message = State()
    waiting_for_method = State()
    waiting_for_payment = State()