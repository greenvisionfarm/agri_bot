import os
from telebot import types

from configuration import bot
from data_core.requests_data import get_ebm, get_ema, get_eco


@bot.message_handler(commands=['start'])
def start_message(message):

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ebm = types.KeyboardButton('Pšenica')
    ema = types.KeyboardButton('Kukurica')
    eco = types.KeyboardButton('Raps')
    ebm_price_chart = types.KeyboardButton('Pšenica graf')
    ema_price_chart = types.KeyboardButton('Kukurica graf')
    eco_price_chart = types.KeyboardButton('Paps graf')

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
            ebm = get_ebm()
            bot.send_message(message.chat.id, f'Cena: {ebm[0]} \n\n'
                                              f'Cas: {ebm[1]}')
        elif message.text == 'Kukurica':
            ema = get_ema()
            bot.send_message(message.chat.id, f'Cena: {ema[0]} \n\n'
                                              f'Cas: {ema[1]}')
        elif message.text == 'Raps':
            eco = get_eco()
            bot.send_message(message.chat.id, f'Cena: {eco[0]} \n\n'
                                              f'Cas {eco[1]}')

        elif message.text == 'Pšenica graf':
            bot.send_message(message.chat.id, f'graf')
        elif message.text == 'Kukurica graf':
            bot.send_message(message.chat.id, f'graf')
        elif message.text == 'Raps graf':
            bot.send_message(message.chat.id, f'graf')

        else:
            bot.send_message(message.chat.id, 'Nerozumiem. Použite tlačidlá')


bot.polling()
