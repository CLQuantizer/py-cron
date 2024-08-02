from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base

from config import CONFIGS

PG_URL = CONFIGS['PG']

engine = create_engine(PG_URL)
Base = declarative_base()


# Define Word model
class Word(Base):
    __tablename__ = 'words'

    word = Column(String, primary_key=True)
    updated_at = Column(DateTime)


class SentimentRecord(Base):
    __tablename__ = 'symbols'

    symbol = Column(String, primary_key=True)
    # sentiment is a float between -1 and 1
    sentiment = Column(Float)
    text = Column(String)
    updated_at = Column(DateTime)


# Create session factory
Session = sessionmaker(bind=engine)


def get_words_today():
    with Session() as session:
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        words = session.query(Word.word).filter(Word.updated_at >= twenty_four_hours_ago).all()
        return [word[0] for word in words]


def select_recent_5_words():
    with Session() as session:
        words = session.query(Word.word).order_by(Word.updated_at.desc()).limit(5).all()
        return [word[0] for word in words]


if __name__ == '__main__':
    print(get_words_today())
