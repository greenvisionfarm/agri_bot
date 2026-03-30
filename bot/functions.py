import logging

from bot import constants
from data_core import main_constants

logger = logging.getLogger(__name__)


def create_message(result: str, data: str) -> str:
    """Форматирование ответного сообщения"""
    logger.debug(f"Создание сообщения: result={result}, data={data}")
    message = constants.answer_message.format(result, data)
    logger.debug(f"Отформатированное сообщение: {message}")
    return message


def validation_of_incoming_data(data: str):
    """Валидация пользовательского ввода"""
    logger.debug(f"Валидация ввода: '{data}'")
    data = data.split(' ')
    first_letter = data[0]

    if first_letter not in main_constants.products:
        logger.debug(f"Валидация не пройдена: продукт '{first_letter}' отсутствует в списке разрешённых")
        return False

    elif len(data) == 1 or (len(data) == 2 and data[1] == 'graf'):
        logger.debug(f"Валидация пройдена: {data}")
        return data

    logger.debug(f"Валидация не пройдена: неверный формат")
    return False
