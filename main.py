from telebot import types

from configuration import bot
from data_core.post_data import data_processing
from data_core.grafs import create_graf
from data_core.secondary_functions import validation_of_incoming_data


@bot.message_handler(commands=['start'])
def start_message(message):

    # Creating keyboard buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wheat = types.KeyboardButton('Pšenica')
    maize = types.KeyboardButton('Kukurica')
    rapeseed = types.KeyboardButton('Raps')
    wheat_price_chart = types.KeyboardButton('Pšenica graf')
    maize_price_chart = types.KeyboardButton('Kukurica graf')
    rapeseed_price_chart = types.KeyboardButton('Raps graf')

    markup.add(wheat, maize, rapeseed, wheat_price_chart, maize_price_chart, rapeseed_price_chart)

    # Start message
    bot.send_message(
        message.chat.id, 'Údaje prevzaté z web-page Central European Commission',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def callback(message):
    if message.chat.type == 'private':
        input_message_validation = validation_of_incoming_data(message.text)

        if input_message_validation:
            request_processing = len(input_message_validation)
            if request_processing == 1:
                result = data_processing(input_message_validation[0])
                price = result[0][0]
                date = result[0][1]

                bot.send_message(
                    message.chat.id,
                    f'Cena: {price} €\n'
                    f'Data : {date}'
                )
            if request_processing == 2:
                product = input_message_validation[0]
                graf = create_graf(product)

                bot.send_photo(message.chat.id, graf)
        else:
            bot.send_message(message.chat.id, 'Nerozumiem. Použite tlačidlá')


if __name__ == '__main__':
    print('App is working')
    bot.polling()
