import logging

from telebot import types

from bot import buttons
from bot.configuration import bot
from bot.functions import create_message, validation_of_incoming_data

from data_core.data import ApiData
from bot import constants

logger = logging.getLogger(__name__)


def add_buttons():
    logger.debug("Creating keyboard buttons")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons.bot_buttons:
        markup.add(button)
    logger.debug(f"Keyboard created with {len(buttons.bot_buttons)} buttons")
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    logger.info(f"Received /start command from user {message.from_user.id} ({message.from_user.username})")
    try:
        markup = add_buttons()
        bot.send_message(message.chat.id, constants.start_message_text, reply_markup=markup)
        logger.info(f"Start message sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error sending start message to user {message.from_user.id}: {e}", exc_info=True)


@bot.message_handler(content_types=['text'])
def callback(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_text = message.text
    
    logger.info(f"Received message from user {user_id} ({username}): '{user_text}'")
    
    if message.chat.type != 'private':
        logger.warning(f"Message from non-private chat (chat_id: {message.chat.id}), ignoring")
        return

    logger.debug(f"Validating user input: '{user_text}'")
    input_message_validation = validation_of_incoming_data(message.text)
    
    if not input_message_validation:
        logger.warning(f"Validation failed for user {user_id}: '{user_text}'")
        try:
            bot.send_message(message.chat.id, constants.error_message)
            logger.info(f"Error message sent to user {user_id}")
        except Exception as e:
            logger.error(f"Error sending error message to user {user_id}: {e}", exc_info=True)
        return

    logger.debug(f"Validation successful: {input_message_validation}")
    api_data = ApiData()
    request_processing = len(input_message_validation)

    if request_processing == 1:
        product = input_message_validation[0]
        logger.info(f"Processing price request for product: {product}")
        try:
            result, data = api_data.data_processing(product)
            if result is False:
                logger.warning(f"Failed to get data for product {product}")
                bot.send_message(message.chat.id, "Не удалось получить данные")
                return
            
            bot_message = create_message(result, data)
            logger.info(f"Sending price response to user {user_id}: {bot_message}")
            bot.send_message(message.chat.id, bot_message)
            logger.info(f"Price response sent to user {user_id}")
        except Exception as e:
            logger.error(f"Error processing price request for {product}: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Произошла ошибка при обработке запроса")

    elif request_processing == 2:
        product = input_message_validation[0]
        logger.info(f"Processing graph request for product: {product}")
        try:
            graf = api_data.create_graf(product)
            if graf:
                logger.info(f"Sending graph to user {user_id} (size: {len(graf)} bytes)")
                bot.send_photo(message.chat.id, graf)
                logger.info(f"Graph sent to user {user_id}")
            else:
                logger.warning(f"Not enough data for graph: {product}")
                bot.send_message(message.chat.id, 'Na vykreslenie grafu nie je dostatok hodnôt')
        except Exception as e:
            logger.error(f"Error creating graph for {product}: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Произошла ошибка при создании графика")
    else:
        logger.warning(f"Unknown request type from user {user_id}: request_processing={request_processing}")
        bot.send_message(message.chat.id, constants.error_message)
