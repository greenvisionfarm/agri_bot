import os

from telebot import TeleBot

""" Telegram Token """
bot = TeleBot(os.environ.get('TOKEN'))
