import logging
import os
import time
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv, find_dotenv

from config import START_MSG, WIN_MSG, LOSE_MSG, LOG_CHAT, \
    PREMIUM, REGULAR_DAILY_QUOTA
from conversation_handler import ConversationHandler
from alchemy.db_handler import DbHandler
from middlewares.quota import QuotaMiddleware, quoted
from middlewares.symbols_limit import SymbolsCapMiddleware, symbols_cap
from schedule.reset_quota import daily_quota_reset
from keyboards.save_bot import get_save_button
from utils.premium import is_premium

load_dotenv(find_dotenv())

# Getting tokens and stuff
API_TOKEN = os.getenv('TELEGRAM_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_ROLE = os.getenv('DB_ROLE')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DSN = f'postgresql://{DB_ROLE}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Setting system time
os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
chat = ConversationHandler(OPENAI_API_KEY)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(START_MSG, parse_mode="HTML")


@dp.message_handler(commands=['kill'])
async def kill_character(message: types.Message):
    if chat.get_character(message.chat.id):
        chat.remove_character(message.chat.id)
        await message.answer('Ты убил Олега... ffff')
    else:
        await message.answer('Убивать некого\n¯\_(ツ)_/¯')


@dp.message_handler(commands=['whereami'])
async def send_chat_id(message: types.Message):
    await message.answer(f'your chat id:\n<b>{message.chat.id}</b>',
                         parse_mode='HTML')


@dp.message_handler(commands=['quota'])
async def send_remaining_quota(message: types.Message):
    premium = is_premium(message)
    quota = db.get_quota(message.from_user.id)

    if not quota:
        await message.answer('you are not quoted yet, send something '
                             'to me to start the game')
        return

    if premium:
        total = PREMIUM[str(message.from_user.id)]
    else:
        total = REGULAR_DAILY_QUOTA

    await message.answer(f'Quota: {quota.remaining}/{total}')


@dp.message_handler(commands=['this'])
async def send_this(message: types.Message):
    await message.answer(message)


@dp.message_handler(
    lambda msg: msg.reply_to_message.from_user.id == bot.id, is_reply=True)
@quoted
@symbols_cap
async def process_conversation(message: types.Message):
    if not chat.is_character_exists(message.chat.id):
        conv_id = db.record_conversation(message.chat.id)
        character = chat.create_character(message.chat.id, conv_id)
        character.id = db.record_character(conv_id, character.name,
                                           character.prompt)

    character = chat.get_character(message.chat.id)
    db.record_message(character.id, character.conversation_id,
                      message.text, user=True)
    res = character.generate_response(message.text)
    db.record_message(character.id, character.conversation_id,
                      res, user=False)
    print(character.name)
    print(character.prompt)
    for mem in character.memory:
        print(mem)
    await message.reply(res)

    if chat.is_user_win(res, character):
        db.mark_conversation_win(True, character.conversation_id)
        chat.remove_character(message.chat.id)
        await message.answer(WIN_MSG,
                             reply_markup=get_save_button(character.id))

    if chat.is_user_lost(res):
        db.mark_conversation_win(False, character.conversation_id)
        chat.remove_character(message.chat.id)
        await message.answer(LOSE_MSG,
                             reply_markup=get_save_button(character.id))


@dp.callback_query_handler(lambda callback_query: True)
async def process_query(call: types.CallbackQuery):
    if call.data.startswith('save'):
        user = call.from_user.username

        chat = 'ЛС' if not call.message.chat.title else \
            call.message.chat.title

        char = call.data[5:]

        log = f'@{user} из чата {chat} сохранил бота с id {char}'

        await bot.send_message(LOG_CHAT, log)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=None)
        await call.answer('Бот успешно сохранён! (тест фича)')


if __name__ == '__main__':
    with DbHandler(DSN) as db:
        # db.sync_quoted_chats_with_config()
        dp.middleware.setup(QuotaMiddleware(db))
        dp.middleware.setup(SymbolsCapMiddleware())
        loop = asyncio.get_event_loop()
        loop.create_task(daily_quota_reset(dp, db))
        executor.start_polling(dp, loop=loop, skip_updates=True)
