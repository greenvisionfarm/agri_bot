import logging

from telebot import types

from bot import buttons
from bot.configuration import bot
from bot.functions import create_message, validation_of_incoming_data

from data_core.data import ApiData
from bot import constants

logger = logging.getLogger(__name__)


def add_buttons():
    logger.debug("Создание кнопок клавиатуры")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons.bot_buttons:
        markup.add(button)
    logger.debug(f"Клавиатура создана с {len(buttons.bot_buttons)} кнопками")
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id} ({message.from_user.username})")
    try:
        markup = add_buttons()
        bot.send_message(message.chat.id, constants.start_message_text, reply_markup=markup)
        logger.info(f"Приветственное сообщение отправлено пользователю {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка отправки приветственного сообщения пользователю {message.from_user.id}: {e}", exc_info=True)


@bot.message_handler(content_types=['text'])
def callback(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_text = message.text

    logger.info(f"Получено сообщение от пользователя {user_id} ({username}): '{user_text}'")

    if message.chat.type != 'private':
        logger.warning(f"Сообщение из непубличного чата (chat_id: {message.chat.id}), игнорирование")
        return

    logger.debug(f"Валидация пользовательского ввода: '{user_text}'")
    input_message_validation = validation_of_incoming_data(message.text)

    if not input_message_validation:
        logger.warning(f"Валидация не пройдена для пользователя {user_id}: '{user_text}'")
        try:
            bot.send_message(message.chat.id, constants.error_message)
            logger.info(f"Сообщение об ошибке отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения об ошибке пользователю {user_id}: {e}", exc_info=True)
        return

    logger.debug(f"Валидация пройдена: {input_message_validation}")
    api_data = ApiData()
    request_processing = len(input_message_validation)

    if request_processing == 1:
        product = input_message_validation[0]
        logger.info(f"Обработка запроса цены для продукта: {product}")
        try:
            result, data = api_data.data_processing(product)
            if result is False:
                logger.warning(f"Не удалось получить данные для продукта {product}")
                bot.send_message(message.chat.id, "Не удалось получить данные")
                return

            bot_message = create_message(result, data)
            logger.info(f"Отправка ответа с ценой пользователю {user_id}: {bot_message}")
            bot.send_message(message.chat.id, bot_message)
            logger.info(f"Ответ с ценой отправлен пользователю {user_id}")
        except Exception as e:
            logger.error(f"Ошибка обработки запроса цены для {product}: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Произошла ошибка при обработке запроса")

    elif request_processing == 2:
        product = input_message_validation[0]
        logger.info(f"Обработка запроса графика для продукта: {product}")
        try:
            graf = api_data.create_graf(product)
            if graf:
                logger.info(f"Отправка графика пользователю {user_id} (размер: {len(graf)} байт)")
                bot.send_photo(message.chat.id, graf)
                logger.info(f"График отправлен пользователю {user_id}")
            else:
                logger.warning(f"Недостаточно данных для графика: {product}")
                bot.send_message(message.chat.id, 'Na vykreslenie grafu nie je dostatok hodnôt')
        except Exception as e:
            logger.error(f"Ошибка создания графика для {product}: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Произошла ошибка при создании графика")
    else:
        logger.warning(f"Неизвестный тип запроса от пользователя {user_id}: request_processing={request_processing}")
        bot.send_message(message.chat.id, constants.error_message)
