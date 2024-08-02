from apscheduler.schedulers.blocking import BlockingScheduler
import logging

from prometheus_client import start_http_server

from config import setup_logging
from db import get_words_today, select_recent_5_words
from llm import summarize_day
from tg import send_telegram_message

logging.basicConfig(filename='scheduler.log', level=logging.INFO)


def message_at_18():
    words = get_words_today()
    cnt = len(words)
    if cnt < 10:
        cnt = 5
        words = select_recent_5_words()
    send_telegram_message(summarize_day(cnt, words))


if __name__ == '__main__':
    setup_logging()
    scheduler = BlockingScheduler()
    start_http_server(9090)
    scheduler.add_job(lambda: send_telegram_message("早上好！今天要學法語了！"), 'cron', hour=7, minute=0)
    scheduler.add_job(message_at_18, 'cron', hour=17, minute=0)
    try:
        print("Starting the job scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
