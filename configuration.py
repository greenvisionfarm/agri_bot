import os
from sqlalchemy import create_engine
from telebot import TeleBot

# Telegram
bot = TeleBot(os.environ.get('TOKEN'))
# Data
KEY = os.environ.get('KEY')
URL = f'https://flux.agritel.com/agritelwebsite/QuotesAjax.aspx?key={KEY}'
engine = create_engine('sqlite:///./agri_bot.db')

