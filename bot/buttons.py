from telebot import types
from data_core import main_constants


# Creating keyboard buttons
wheat = types.KeyboardButton(main_constants.psenica)
maize = types.KeyboardButton(main_constants.kukurica)
rapeseed = types.KeyboardButton(main_constants.raps)
# wheat_price_chart = types.KeyboardButton('Pšenica graf')
# maize_price_chart = types.KeyboardButton('Kukurica graf')
# rapeseed_price_chart = types.KeyboardButton('Raps graf')
