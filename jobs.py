from apscheduler.schedulers.blocking import BlockingScheduler
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


if __name__ == '__main__':
    scheduler = BlockingScheduler()

    scheduler.add_job(message_at_7, 'cron', hour=6, minute=0)
    scheduler.add_job(message_at_19, 'cron', hour=18, minute=0)
    #  for test purpose add a job to log every 10 seconds
    # scheduler.add_job(lambda: print("Logging..."), 'interval', seconds=10)

    try:
        print("Starting the job scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
