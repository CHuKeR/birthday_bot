from datetime import datetime
from pydantic import BaseSettings
from sqlalchemy import create_engine
from telebot import TeleBot
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker


class Config(BaseSettings):
    DB_URL: str
    BOT_KEY: str


Base = declarative_base()
config = Config()
db = create_engine(config.DB_URL)
Session = sessionmaker(bind=db)
session = Session()
bot = TeleBot(config.BOT_KEY)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    birthday = Column(DateTime, nullable=False)
    nickname = Column(String, nullable=False)
    chat_tg_id = Column(String)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, year=2020)
    query = session.query(User).filter(User.birthday == now).all()
    for user in query:
        bot.send_message(user.chat_tg_id, f'Happy B-DAY @{user.nickname}')
