import logging

from dotenv import dotenv_values
from prometheus_client import Counter

CONFIGS = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


def setup_logging():
    logging.basicConfig(filename='scheduler.log', level=logging.INFO)


MESSAGE_SENT = Counter('message_sent', 'The number of messages sent to Telegram')