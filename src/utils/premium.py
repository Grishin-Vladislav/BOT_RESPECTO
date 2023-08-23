from aiogram.types import Message

from config import PREMIUM


def is_premium(message: Message):
    return PREMIUM.get(str(message.from_user.id))
