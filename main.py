from telebot import types

from configuration import bot
from data_core.grafs import Wheat_graf, Corn_graf, Rapeseed_graf
from data_core.post_data import post_ebm, post_ema, post_eco


@bot.message_handler(commands=['start'])
def start_message(message):

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ebm = types.KeyboardButton('Pšenica')
    ema = types.KeyboardButton('Kukurica')
    eco = types.KeyboardButton('Raps')
    ebm_price_chart = types.KeyboardButton('Pšenica graf')
    ema_price_chart = types.KeyboardButton('Kukurica graf')
    eco_price_chart = types.KeyboardButton('Raps graf')

    markup.add(ebm, ema, eco, ebm_price_chart, ema_price_chart, eco_price_chart)

    # Message
    bot.send_message(
        message.chat.id, 'Údaje prevzaté z www.agritel.com',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def callback(message):
    if message.chat.type == 'private':
        if message.text == 'Pšenica':
            ebm = post_ebm()
            bot.send_message(message.chat.id, f'Cena: {ebm[0]} \n\n'
                                              f'Cas: {ebm[1]}')
        elif message.text == 'Kukurica':
            ema = post_ema()
            bot.send_message(message.chat.id, f'Cena: {ema[0]} \n\n'
                                              f'Cas: {ema[1]}')
        elif message.text == 'Raps':
            eco = post_eco()
            bot.send_message(message.chat.id, f'Cena: {eco[0]} \n\n'
                                              f'Cas {eco[1]}')

        elif message.text == 'Pšenica graf':
            Wheat_graf()
            graf = open('png/wheat_graf.png', 'rb')
            bot.send_photo(message.chat.id, graf)
        elif message.text == 'Kukurica graf':
            Corn_graf()
            graf = open('png/corn_graf.png', 'rb')
            bot.send_photo(message.chat.id, graf)
        elif message.text == 'Raps graf':
            Rapeseed_graf()
            graf = open('png/rape_graf.png', 'rb')
            bot.send_photo(message.chat.id, graf)

        else:
            bot.send_message(message.chat.id, 'Nerozumiem. Použite tlačidlá')


bot.polling()
