from telebot import types

from configuration import bot
from data_core.post_data import data_processing
from data_core.grafs import create_graf


@bot.message_handler(commands=['start'])
def start_message(message):

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wheat = types.KeyboardButton('Pšenica')
    maize = types.KeyboardButton('Kukurica')
    rapeseed = types.KeyboardButton('Raps')
    ebm_price_chart = types.KeyboardButton('Pšenica graf')
    ema_price_chart = types.KeyboardButton('Kukurica graf')
    eco_price_chart = types.KeyboardButton('Raps graf')

    markup.add(wheat, maize, rapeseed, ebm_price_chart, ema_price_chart, eco_price_chart)

    # Message
    bot.send_message(
        message.chat.id, 'Údaje prevzaté z web-page Central European Commission',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def callback(message):
    if message.chat.type == 'private':
        input_message = message.text.split(' ')
        if len(input_message) == 1:
            result = data_processing(input_message[0])
            price = result[0][0]
            date = result[0][1]
            bot.send_message(
                message.chat.id,
                f'Cena: {price} €\n'
                f'Data : {date}'
            )

        elif len(input_message) == 2:
            product = input_message[0]
            create_graf(product)

            graf = open(f'./data/{product}_graf.png', 'rb')
            bot.send_photo(message.chat.id, graf)

        else:
            bot.send_message(message.chat.id, 'Nerozumiem. Použite tlačidlá')


if __name__ == '__main__':
    print('App is working')
    bot.polling()
