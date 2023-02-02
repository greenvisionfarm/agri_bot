import os
from datetime import datetime, timedelta

from telebot import TeleBot

""" Telegram Token """
bot = TeleBot(os.environ.get('TOKEN'))

""" Requests """
main_url = 'https://ec.europa.eu/agrifood/api'
end_date = datetime.now().strftime("%d/%m/%Y")
begin_date = (datetime.now() - timedelta(days=60)).strftime("%d/%m/%Y")



