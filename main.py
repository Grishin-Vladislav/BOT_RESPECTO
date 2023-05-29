import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv, find_dotenv

from config import start_message, win_message, lose_message, \
    win_triggers, lose_triggers
from character import Character

load_dotenv(find_dotenv())

API_TOKEN = os.getenv('TELEGRAM_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

conversations = {}


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(start_message)


@dp.message_handler(commands=['kill'])
async def kill_character(message: types.Message):
    if conversations.get(message.chat.id):
        del conversations[message.chat.id]
        await message.answer('Вы его убили... ffff')
    else:
        await message.answer('Убивать некого\n¯\_(ツ)_/¯')


@dp.message_handler(is_reply=True)
async def process_conversation(message: types.Message):
    if not conversations.get(message.chat.id):
        conversations[message.chat.id] = Character()

    character = conversations[message.chat.id]
    res = character.generate_response(message.text)
    print(character.name)
    print(character.prompt)
    for mem in character.memory:
        print(mem)
    await message.reply(res)

    if any(trigger in res.lower() for trigger in win_triggers):
        await message.answer(win_message)
        del conversations[message.chat.id]

    if any(trigger in res.lower() for trigger in lose_triggers):
        await message.answer(lose_message)
        del conversations[message.chat.id]


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
