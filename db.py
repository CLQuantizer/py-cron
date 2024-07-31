from psycopg2 import OperationalError
import time
from dotenv import dotenv_values
import psycopg2

config = dotenv_values(".env")
PG_URL = config['PG']

connection = psycopg2.connect(PG_URL)


def get_words_today():
    retries = 3
    while retries > 0:
        try:
            connection = psycopg2.connect(PG_URL)
            cursor = connection.cursor()
            cursor.execute("SELECT word FROM words WHERE updated_at >= NOW() - INTERVAL '24 hours'")
            words = cursor.fetchall()
            cursor.close()
            connection.close()
            return [word[0] for word in words]
        except OperationalError as e:
            print(f"OperationalError: {e}")
            retries -= 1
            if retries > 0:
                print(f"Retrying... {retries} attempts left.")
                time.sleep(5)
            else:
                raise Exception("Failed to connect to the database after several attempts")
            
if __name__ == '__main__':
    print(get_words_today())