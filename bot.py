# File bot.py

"""
Launch script with a command like
   python bot.py "123456:ThisIsYourChatBotToken"
"""

import sys, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def hello(bot, update):
   update.message.reply_text(
       'Hello {} !'.format(update.message.from_user.first_name)
   )

def where_is(bot, update):
    user_location = update.message.location
    update.message.reply_text(
        'Vous avez envoyé les coordonnées {};{}.'.format(user_location.latitude, user_location.longitude)
    )

updater = Updater(sys.argv[1]) # Avec notre token en argument

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.location, where_is)) # On accepte la commande "Hello"

updater.start_polling()
updater.idle()
