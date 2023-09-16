from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import current_handler, CancelHandler

from config import ADMINS


class AdminMiddleware(BaseMiddleware):
    def __init__(self):
        BaseMiddleware.__init__(self)

    async def on_process_message(self, message, data):
        handler = current_handler.get()

        if not getattr(handler, 'admin_only', False):
            return

        if str(message.from_user.id) in ADMINS:
            return

        await message.answer('idi nahui')
        raise CancelHandler


def admin_only(func):
    setattr(func, 'admin_only', True)
    return func
