from telebot import types

from bot import buttons
from bot.configuration import bot
from bot.functions import create_message, validation_of_incoming_data

from data_core.data import ApiData
from bot import constants


def add_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons.bot_buttons:
        markup.add(button)

    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = add_buttons()
    bot.send_message(message.chat.id, constants.start_message_text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def callback(message):
    if message.chat.type != 'private':
        return

    input_message_validation = validation_of_incoming_data(message.text)
    if not input_message_validation:
        return bot.send_message(message.chat.id, constants.error_message)

    api_data = ApiData()
    request_processing = len(input_message_validation)

    if request_processing == 1:
        result, data = api_data.data_processing(input_message_validation[0])
        bot_message = create_message(result, data)
        return bot.send_message(message.chat.id, bot_message)

    if request_processing == 2:
        product = input_message_validation[0]
        graf = api_data.create_graf(product)
        if graf:
            bot.send_photo(message.chat.id, graf)

        else:
            bot.send_message(message.chat.id, 'Na vykreslenie grafu nie je dostatok hodnôt')
