import schedule
import time
import requests
from dotenv import dotenv_values

from db import get_words_today
from llm import generate_encouragement

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Your Telegram bot token
BOT_TOKEN = config['BOT_TOKEN']
# The chat ID of the recipient
CHAT_ID = config['CHAT_ID']


def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response.json()


def message_at_7():
    message = "早上好！今天要學法語了！"
    send_telegram_message(message)


def message_at_19():
    words = get_words_today()
    cnt = len(words)
    encouragement = generate_encouragement(cnt, words)
    # if it is less than 10, send a reminder
    send_telegram_message(f"{encouragement}")


# Schedule the job to run every day at 7:00 AM
schedule.every().day.at("06:00").do(message_at_7)

# Schedule the job to run every day at 19:00 PM
schedule.every().day.at("18:00").do(message_at_19)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
