from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from psycopg2 import OperationalError
import time
from dotenv import dotenv_values
import psycopg2

config = dotenv_values(".env")
PG_URL = 'postgresql+psycopg2://' + config['PG'].split('://')[1]

engine = create_engine(PG_URL)
Base = declarative_base()


# Define Word model
class Word(Base):
    __tablename__ = 'words'

    word = Column(String, primary_key=True)
    updated_at = Column(DateTime)


# Create session factory
Session = sessionmaker(bind=engine)


def get_words_today():
    with Session() as session:
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        words = session.query(Word.word).filter(Word.updated_at >= twenty_four_hours_ago).all()
        return [word[0] for word in words]


if __name__ == '__main__':
    print(get_words_today())
