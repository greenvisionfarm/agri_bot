from bot.main import *

if __name__ == '__main__':
    try:
        print('Bot is working')
        bot.polling()
    except KeyboardInterrupt:
        print('Bot is stop')
