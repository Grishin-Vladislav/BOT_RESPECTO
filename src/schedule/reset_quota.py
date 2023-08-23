import asyncio
from datetime import datetime

from aiogram import dispatcher
from aiogram.utils.exceptions import BotKicked, BotBlocked


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

        kicked = []

        for chat_id in db.get_all_chats():
            try:
                await dp.bot.send_message(chat_id=chat_id,
                                          text=f'Квота восстановлена.')
            except BotBlocked:
                kicked.append(chat_id)
                continue

        if kicked:
            db.remove_inactive_chats(kicked)
