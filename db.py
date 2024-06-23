from dotenv import dotenv_values
import psycopg2

config = dotenv_values(".env")
PG_URL = config['PG']

connection = psycopg2.connect(PG_URL)


def get_words_today():
    cursor = connection.cursor()
    cursor.execute("SELECT word FROM words WHERE updated_at::date = CURRENT_DATE")
    words = cursor.fetchall()
    return [word[0] for word in words]
