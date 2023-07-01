import asyncio
from datetime import datetime

from aiogram import dispatcher

from config import QUOTED_CHATS


async def daily_quota_reset(dp: dispatcher, db):
    while True:

        current_time = datetime.now()
        target_time = datetime(year=current_time.year,
                               month=current_time.month,
                               day=current_time.day,
                               hour=00,
                               minute=00)

        delta = target_time - current_time

        await asyncio.sleep(delta.seconds + 1)

        db.reset_quota_for_all()

        for chat, quota in QUOTED_CHATS.items():
            await dp.bot.send_message(chat_id=chat,
                                      text=f'Квота восстановлена. '
                                           f'({quota})')
