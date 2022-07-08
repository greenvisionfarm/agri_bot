import os
from telebot import types, TeleBot
from get_data import get_ebm, get_ema, get_eco

bot = TeleBot(os.environ.get('TOKEN'))


@bot.message_handler(commands=['start'])
def start_message(message):

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ebm = types.KeyboardButton('pšenica')
    ema = types.KeyboardButton('kukurica')
    eco = types.KeyboardButton('raps')
    markup.add(ebm, ema, eco)

    # Message
    bot.send_message(
        message.chat.id, 'Údaje prevzaté z www.agritel.com',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def callback(message):
    if message.chat.type == 'private':
        if message.text == 'pšenica':
            bot.send_message(message.chat.id, f'Cena: {get_ebm()[0]} \n\n'
                                              f'Cas: {get_ebm()[1]}')
        elif message.text == 'kukurica':
            bot.send_message(message.chat.id, f'Cena: {get_ema()[0]} \n\n'
                                              f'Cas: {get_ema()[1]}')
        elif message.text == 'raps':
            bot.send_message(message.chat.id, f'Cena: {get_eco()[0]} \n\n'
                                              f'Cas {get_eco()[1]}')
        else:
            bot.send_message(message.chat.id, 'Nerozumiem. Použite tlačidlá')


bot.polling()
