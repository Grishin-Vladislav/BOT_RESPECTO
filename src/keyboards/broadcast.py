from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_options():
    keyboard = InlineKeyboardMarkup()
    everybody = InlineKeyboardButton('ваще всем нахой',
                                     callback_data=f'broadcast_all')
    registered = InlineKeyboardButton('зарегистрировавшимся педикам',
                                      callback_data='broadcast_promo')

    keyboard.add(everybody, registered)
    return keyboard


def confirm():
    keyboard = InlineKeyboardMarkup()
    yes = InlineKeyboardButton('✅',
                               callback_data=f'send')
    no = InlineKeyboardButton('❎',
                              callback_data='discard')

    keyboard.add(yes, no)
    return keyboard
