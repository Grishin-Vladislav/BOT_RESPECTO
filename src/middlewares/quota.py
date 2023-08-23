from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.handler import current_handler, CancelHandler

from config import PREMIUM, REGULAR_DAILY_QUOTA
from alchemy.models import Quota
from utils.premium import is_premium


class QuotaMiddleware(BaseMiddleware):
    def __init__(self, db_handler):
        BaseMiddleware.__init__(self)
        self.db = db_handler

    async def on_process_message(self, message, data):
        handler = current_handler.get()

        if not getattr(handler, 'quoted', False):
            return

        premium = is_premium(message)
        user_id = message.from_user.id
        quota = self.db.get_quota(user_id)

        if premium:
            if not quota:
                self.db.create_quoted_chat(user_id,
                                           PREMIUM[str(user_id)] - 1)
                return

            if quota.remaining > 0:
                self.db.change_quota(user_id, quota.remaining - 1)
                return

            await message.answer(
                f'Бот устал.. возвращайся завтра!\nКвота: '
                f'({quota.remaining}/{PREMIUM[str(user_id)]})')
            raise CancelHandler

        else:
            if not quota:
                self.db.create_quoted_chat(user_id,
                                           REGULAR_DAILY_QUOTA - 1)
                return

            if quota.remaining > 0:
                self.db.change_quota(user_id, quota.remaining - 1)
                return

            await message.answer(
                f'Бот устал.. возвращайся завтра!\nКвота: '
                f'({quota.remaining}/{REGULAR_DAILY_QUOTA})')
            raise CancelHandler


def quoted(func):
    setattr(func, 'quoted', True)
    return func
