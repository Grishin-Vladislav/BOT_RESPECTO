import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv, find_dotenv

from config import START_MSG, WIN_MSG, LOSE_MSG, WHITELIST
from conversation_handler import ConversationHandler
from alchemy.db_handler import DbHandler

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

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
chat = ConversationHandler(OPENAI_API_KEY)


@dp.message_handler(commands=['start'], chat_id=WHITELIST)
async def send_welcome(message: types.Message):
    await message.answer(START_MSG)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f'You are not in white list\n\n'
                         f'User_id: {message.from_user.id}\n'
                         f'Chat_id: {message.chat.id}')


@dp.message_handler(commands=['kill'], chat_id=WHITELIST)
async def kill_character(message: types.Message):
    if chat.get_character(message.chat.id):
        chat.remove_character(message.chat.id)
        await message.answer('Вы его убили... ffff')
    else:
        await message.answer('Убивать некого\n¯\_(ツ)_/¯')


@dp.message_handler(
    lambda msg: msg.reply_to_message.from_user.id == bot.id,
    chat_id=WHITELIST, is_reply=True)
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

    if chat.is_user_win(res):
        db.mark_conversation_win(True, character.conversation_id)
        chat.remove_character(message.chat.id)
        await message.answer(WIN_MSG)

    if chat.is_user_lost(res):
        db.mark_conversation_win(False, character.conversation_id)
        chat.remove_character(message.chat.id)
        await message.answer(LOSE_MSG)


if __name__ == '__main__':
    with DbHandler(DSN) as db:
        executor.start_polling(dp, skip_updates=True)
