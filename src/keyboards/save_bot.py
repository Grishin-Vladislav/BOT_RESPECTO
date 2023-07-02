from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_save_button(character_id):
    keyboard = InlineKeyboardMarkup()
    save_button = InlineKeyboardButton('Сохранить перса себе',
                                       callback_data=f'save_{character_id}')
    keyboard.add(save_button)
    return keyboard
