import time
import json
import requests

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from urllib.parse import urlparse

from app.config.config import load_config
from app.utils.keyboards import get_link_info_keyboard, get_pay_button_keyboard, get_payment_keyboard
from app.utils.functions import generate_sign, get_status
from app.states.pinMessage import PinMessage


async def call_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Команда отменена')
    await state.finish()
    await call.answer()

    
async def how_get_link(call: types.CallbackQuery):
    await call.message.answer('Зайдите в группу -> найдите нужное сообщение -> нажмите на него один раз и во всплывающем меню выберите "Копировать ссылку" -> отправьте ее сюда боту🦸')
    await call.answer()


async def enter_link(call: types.CallbackQuery):
    await call.message.answer('Пожалуйста, отправьте ссылку на сообщение из <a href="t.me/dubai_profi">группы</a>', reply_markup=get_link_info_keyboard(), parse_mode='html')
    await PinMessage.waiting_for_message.set()
    await call.answer()


async def pin_message(message: types.Message, state: FSMContext):
    directories = urlparse(message.text).path.strip('/').split('/')
    if len(directories) < 2:
        await message.answer('Этого сообщения нет в группе! Пожалуйста, попробуйте еще раз')
        return
    if directories[-2] != 'dubai_profi':
        await message.answer('Этого сообщения нет в группе! Пожалуйста, попробуйте еще раз')
        return
    await message.answer('Хорошо! Сумма для оплаты: 300руб.\nВыберите один из способов оплаты ниже', reply_markup=get_payment_keyboard())
    await state.update_data(message_id=directories[-1])
    await PinMessage.next()


async def pin_method(call: types.CallbackQuery, state: FSMContext):
    data = {
        'shopId': 21154,
        'nonce': int(time.time()*1000),
        'email': 'email@mail.ru',
        'ip': '85.8.8.8',
        'amount': 300,
        'currency': 'RUB'
    }
    action = call.data.split('_')[1]
    data['i'] = 36 if action == 'card' else 6
    res = requests.post(
        'https://api.freekassa.ru/v1/orders/create', 
        json=generate_sign(load_config().fkassa.token, data)
    )
    res = json.loads(res.text)
    link = res['location']
    await call.message.answer(
        f'Оплатите по кнопке ниже', 
        parse_mode='html', 
        reply_markup=get_pay_button_keyboard(link)
    )
    
    get_status(res['orderId'])
    
    await call.answer()
    await state.finish()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(call_cancel, text='cancel', state='*')
    dp.register_callback_query_handler(how_get_link, text='how_get_link', state='*')
    dp.register_callback_query_handler(enter_link, text='pay', state='*')
    dp.register_message_handler(pin_message, state=PinMessage.waiting_for_message)
    dp.register_callback_query_handler(pin_method, Text(startswith='method_'), state=PinMessage.waiting_for_method)


# @dp.message_handler(state=PinMessage.waiting_for_payment)
# async def pin_payment(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer('Благодарим за использование нашего бота! Сообщение будет закреплено в группе в течение 24 часов')

