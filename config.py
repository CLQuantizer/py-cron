import logging
from dotenv import dotenv_values

CONFIGS = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


def setup_logging():
    logging.basicConfig(filename='scheduler.log', level=logging.INFO)
