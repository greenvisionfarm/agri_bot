from telebot import types

from bot import buttons
from bot.configuration import bot

from data_core.data import ApiData
from bot import constants
# from data_core.grafs import create_graf


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(buttons.wheat, buttons.maize, buttons.rapeseed)
    bot.send_message(message.chat.id, constants.start_message_text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def callback(message):
    api_data = ApiData()

    if message.chat.type == 'private':
        input_message_validation = api_data.validation_of_incoming_data(message.text)

        if input_message_validation:
            request_processing = len(input_message_validation)
            if request_processing == 1:
                result, data = api_data.data_processing(input_message_validation[0])
                bot.send_message(message.chat.id, constants.answer_message.format(result, data))
            # if request_processing == 2:
            #     product = input_message_validation[0]
            #     graf = create_graf(product)
            #
            #     bot.send_photo(message.chat.id, graf)
        else:
            bot.send_message(message.chat.id, constants.error_message)
