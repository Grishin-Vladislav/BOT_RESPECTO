from aiogram.dispatcher.filters.state import StatesGroup, State


class BroadcastState(StatesGroup):
    START = State()
    MESSAGE_RECEIVED = State()
    GROUP_SELECTED = State()
    CONFIRMED = State()
