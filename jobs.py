from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from dotenv import dotenv_values
import logging
from prometheus_client import start_http_server, Counter

from config import CONFIGS
from db import get_words_today, select_recent_5_words
from llm import summarize_day


logging.basicConfig(filename='scheduler.log', level=logging.INFO)

MESSAGE_SENT = Counter('message_sent', 'The number of messages sent to Telegram')
BOT_TOKEN = CONFIGS['BOT_TOKEN']
CHAT_ID = CONFIGS['CHAT_ID']


def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, json=payload)
    MESSAGE_SENT.inc()
    logging.info(f"Message sent: {message}")
    return response.json()


def message_at_19():
    words = get_words_today()
    cnt = len(words)
    if cnt < 10:
        cnt = 5
        words = select_recent_5_words()
    send_telegram_message(summarize_day(cnt, words))


if __name__ == '__main__':
    scheduler = BlockingScheduler()

    start_http_server(9090)
    scheduler.add_job(lambda: send_telegram_message("早上好！今天要學法語了！"), 'cron', hour=7, minute=0)
    scheduler.add_job(message_at_19, 'cron', hour=18, minute=0)

    try:
        print("Starting the job scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
