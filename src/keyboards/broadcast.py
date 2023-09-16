from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_options():
    keyboard = InlineKeyboardMarkup()
    normal = InlineKeyboardButton('обычным пацанам',
                                     callback_data=f'broadcast_normal')

    registered = InlineKeyboardButton('зарегистрировавшимся педикам',
                                      callback_data='broadcast_promo')

    everybody = InlineKeyboardButton('ваще всем нахой',
                                     callback_data='broadcast_all')

    keyboard.add(normal, registered, everybody)
    return keyboard


def confirm():
    keyboard = InlineKeyboardMarkup()
    yes = InlineKeyboardButton('✅',
                               callback_data=f'send')
    no = InlineKeyboardButton('❎',
                              callback_data='discard')

    keyboard.add(yes, no)
    return keyboard
