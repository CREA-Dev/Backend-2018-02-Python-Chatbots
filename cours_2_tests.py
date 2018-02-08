import sys
"""
from telegram.ext import Updater  # pour récupérer les messages sur le serveur
from telegram.ext import CommandHandler  # pour détecter les commandes
from telegram.ext import MessageHandler  # pour ajouter des filtres
from telegram.ext import Filters  # pour différencier les message
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot_token = sys.argv[1]


def dire_bonjour(bot, update):
    update.message.reply_text(
        "Bonjour {}, comment ça va?".format(update.message.from_user.first_name)
    )

def dire_bonjour2(bot, update):
    update.message.reply_text(
        "Bonjour2 {}, comment ça va?".format(update.message.from_user.first_name)
    )

def echo_text(bot, update):
    update.message.reply_text(
        "Vous avez dit '{}'".format(update.message.text)
    )

def extract_coordinates(bot, update):
    user_location = update.message.location
    update.message.reply_text(
        "Vous êtes à {};{}...".format(user_location.latitude, user_location.longitude)
    )


# Créer une instance de la classe Updater
# pour aller chercher les messages sur Telegram
updater = Updater(bot_token)

# associer le handler à notre updater
updater.dispatcher.add_handler(CommandHandler("start", dire_bonjour))
updater.dispatcher.add_handler(CommandHandler("bonjour", dire_bonjour2))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo_text))
updater.dispatcher.add_handler(MessageHandler(Filters.location, extract_coordinates))

# Déclencher la recherche des messages
updater.start_polling(timeout=2)
updater.idle()
