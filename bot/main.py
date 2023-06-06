from telebot import types

from configuration import bot

from data_core.data import ApiData
from data_core.grafs import create_graf



@bot.message_handler(commands=['start'])
def start_message(message):

    # Creating keyboard buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wheat = types.KeyboardButton('Pšenica')
    maize = types.KeyboardButton('Kukurica')
    rapeseed = types.KeyboardButton('Raps')
    # wheat_price_chart = types.KeyboardButton('Pšenica graf')
    # maize_price_chart = types.KeyboardButton('Kukurica graf')
    # rapeseed_price_chart = types.KeyboardButton('Raps graf')

    markup.add(wheat, maize, rapeseed)

    # Start message
    bot.send_message(message.chat.id, 'Údaje prevzaté z web-page Central European Commission', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def callback(message):
    if message.chat.type == 'private':
        input_message_validation = ApiData().validation_of_incoming_data(message.text)

        if input_message_validation:
            request_processing = len(input_message_validation)
            if request_processing == 1:
                result = ApiData().data_processing(input_message_validation[0])
                price = result

                bot.send_message(message.chat.id, f'Cena: {price} €\n')
            # if request_processing == 2:
            #     product = input_message_validation[0]
            #     graf = create_graf(product)
            #
            #     bot.send_photo(message.chat.id, graf)
        else:
            bot.send_message(message.chat.id, 'Nerozumiem. Použite tlačidlá')

