from aiogram.fsm.state import StatesGroup, State


class EditText(StatesGroup):
    message = State()


class RefLinkStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_token = State()


class ChangePriceState(StatesGroup):
    waiting_for_tariff = State()
    waiting_for_new_price = State()
