import logging

import requests

from config import CONFIGS, MESSAGE_SENT

BOT_TOKEN = CONFIGS['BOT_TOKEN']
CHAT_ID = CONFIGS['CHAT_ID']


def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, json=payload)
    MESSAGE_SENT.inc()
    logging.info(f"Message sent: {message}")
    return response.json()
