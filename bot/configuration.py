import os

from telebot import TeleBot

""" Telegram Token """
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN environment variable is not set")

bot = TeleBot(TOKEN)
