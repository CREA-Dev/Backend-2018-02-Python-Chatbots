# File bot.py

"""
Launch script with a command like
   python bot.py "123456:ThisIsYourChatBotToken"
"""

import sys, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


# We put some identifiers in variables
STATE_HELLO = "state hello"
STATE_INTRO = "state intro"


def hello(bot, update):
    update.message.reply_text(
        'Hello {} !'.format(update.message.from_user.first_name)
    )
    return STATE_INTRO  # Change state

def show_intro(bot, update):
    update.message.reply_text(
        "Après ce message, on repasse en mode hello"
    )
    return STATE_HELLO # Change state

def where_is(bot, update):
    user_location = update.message.location
    update.message.reply_text(
        'Vous avez envoyé les coordonnées {};{}.'.format(user_location.latitude, user_location.longitude)
    )


# Showing debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


# Creation of a conversation handler
conv_handler = ConversationHandler(
        entry_points = [CommandHandler('hello', hello)],
        states = {
            STATE_HELLO: [
                CommandHandler('hello', hello),
                MessageHandler(Filters.location, where_is)
            ],

            STATE_INTRO: [
                CommandHandler('hello', show_intro)
            ],
        },
        fallbacks = []
    )

updater = Updater(sys.argv[1]) # Avec notre token en argument

updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
