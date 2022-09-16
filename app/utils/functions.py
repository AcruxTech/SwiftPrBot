import time
import json
import hmac
import hashlib
import requests

from app.config.config import load_config


def generate_sign(token: str, data: dict) -> dict:
    data = dict(sorted(data.items()))
    sign = ''
    for key in data:
        sign += str(data[key]) + '|'
    sign = sign[:-1]

    byte_key = bytes(token, 'utf-8') 
    data['signature'] = hmac.new(byte_key, sign.encode(), hashlib.sha256).hexdigest()

    return data


def get_status(order_id: int) -> str:
    data = {
        'shopId': 21154,
        'nonce': int(time.time()*1000),
        'orderId': order_id
    }
    res = requests.post(
        'https://api.freekassa.ru/v1/orders', 
        json=generate_sign(load_config().fkassa.token, data))
    res = json.loads(res.text)
    return res['orders'][0]['status']