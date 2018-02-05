# File bot.py

"""
Launch script with a command like
   python bot.py "123456:ThisIsYourChatBotToken"
"""

import sys
from telegram.ext import Updater, CommandHandler

def hello(bot, update):
   update.message.reply_text(
       'Hello {} !'.format(update.message.from_user.first_name)
   )

updater = Updater(sys.argv[1]) # Avec notre token en argument

updater.dispatcher.add_handler(CommandHandler('hello', hello)) # On accepte la commande "Hello"

updater.start_polling()
updater.idle()
