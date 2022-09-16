from aiogram import types


def get_start_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Оплатить💳', callback_data='pay'),
        types.InlineKeyboardButton(text='Отменить', callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_link_info_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Как получить ссылку на сообщение?', callback_data='how_get_link')) 
    return keyboard


def get_payment_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Карта', callback_data='method_card'),
        types.InlineKeyboardButton(text='Yoomoney', callback_data='method_yoomoney')
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_pay_button_keyboard(link: str) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Страница оплаты', url=link),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard