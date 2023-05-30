import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv, find_dotenv

from config import START_MSG, WIN_MSG, LOSE_MSG
from chat import ChatHandler

load_dotenv(find_dotenv())

API_TOKEN = os.getenv('TELEGRAM_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
chat = ChatHandler(OPENAI_API_KEY)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(START_MSG)


@dp.message_handler(commands=['kill'])
async def kill_character(message: types.Message):
    if chat.get_character(message.chat.id):
        chat.remove_conversation(message.chat.id)
        await message.answer('Вы его убили... ffff')
    else:
        await message.answer('Убивать некого\n¯\_(ツ)_/¯')


@dp.message_handler(is_reply=True)
async def process_conversation(message: types.Message):
    chat.add_conversation(message.chat.id)
    character = chat.get_character(message.chat.id)

    res = character.generate_response(message.text)
    print(character.name)
    print(character.prompt)
    for mem in character.memory:
        print(mem)
    await message.reply(res)

    if chat.is_user_win(res):
        chat.remove_conversation(message.chat.id)
        await message.answer(WIN_MSG)

    if chat.is_user_lost(res):
        chat.remove_conversation(message.chat.id)
        await message.answer(LOSE_MSG)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
