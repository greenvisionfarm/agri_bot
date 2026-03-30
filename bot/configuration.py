import os
import logging
from logging.handlers import RotatingFileHandler

from telebot import TeleBot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/bot.log', maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

""" Токен Telegram бота """
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logger.critical("TOKEN environment variable is not set")
    raise ValueError("TOKEN environment variable is not set")

logger.info("Токен бота успешно загружен")
bot = TeleBot(TOKEN)
logger.info("Экземпляр TeleBot создан")
