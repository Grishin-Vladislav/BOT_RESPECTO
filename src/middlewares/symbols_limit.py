from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.handler import current_handler, CancelHandler

from config import MAX_SYMBOLS


class SymbolsCapMiddleware(BaseMiddleware):
    def __init__(self):
        BaseMiddleware.__init__(self)

    async def on_process_message(self, message, data):
        handler = current_handler.get()

        if not getattr(handler, 'symbols', False):
            return

        if len(message.text) <= MAX_SYMBOLS:
            return

        await message.answer(f'Покороче, {MAX_SYMBOLS} симв.')
        raise CancelHandler


def symbols_cap(func):
    setattr(func, 'symbols', True)
    return func