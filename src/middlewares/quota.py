from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.handler import current_handler, CancelHandler

from config import QUOTED_CHATS
from alchemy.models import Quota


class QuotaMiddleware(BaseMiddleware):
    def __init__(self, db_handler):
        BaseMiddleware.__init__(self)
        self.db = db_handler

    async def on_process_message(self, message, data):
        handler = current_handler.get()
        chat_id = message.chat.id

        if not getattr(handler, 'quoted', False):
            return

        if str(chat_id) not in QUOTED_CHATS.keys():
            return

        quota = self.db.get_quota(chat_id)

        if not quota:
            self.db.create_quoted_chat(chat_id,
                                       QUOTED_CHATS[str(chat_id)] - 1)
            return

        if quota.remaining > 0:
            self.db.change_quota(chat_id, quota.remaining - 1)
            return

        await message.answer(f'Бот устал.. возвращайся завтра!\nКвота: '
                             f'({quota.remaining}/{QUOTED_CHATS[str(chat_id)]})')
        raise CancelHandler


def quoted(func):
    setattr(func, 'quoted', True)
    return func
