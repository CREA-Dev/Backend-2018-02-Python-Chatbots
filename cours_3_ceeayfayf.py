import sys
import time
import math
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Récupération du token
bot_token = sys.argv[1]


# Raccourci pour récupérer les données sur OpenData
def get_from_opendata(path):
    url = "http://transport.opendata.ch/v1/" + path
    response = requests.get(url)
    return response.json()


# Message d'accueil
def welcome(bot, update):
    update.message.reply_text(
        "Bonjour {}! Bienvenue sur le bot plus mieux que Tipigee.".format(update.message.from_user.first_name)
    )


# Rechercher par query
def search_by_text(bot, update):
    result = get_from_opendata('locations?query=' + update.message.text)
    send_stations_around(bot, update, result)


# Rechercher par location
def search_by_location(bot, update):
    user_location = update.message.location
    result = get_from_opendata('locations?x={}&y={}'.format(user_location.latitude, user_location.longitude))
    send_stations_around(bot, update, result)


# Envoyer les résultats des stations autour
def send_stations_around(bot, update, result):
    text = "Voici les arrêts correspondant:\n"
    for station in result['stations']:
        if station['id'] is not None:
            text += "\n"
            text += "/st" + station['id']
            text += " {}".format(station['name'])

    update.message.reply_text(text)


# Détails de la station
def station_details(bot, update):

    station_id = update.message.text[3:]
    result = get_from_opendata('stationboard?id={}&limit=10'.format(station_id))

    text = "Prochains départs:\n"
    for departure in result['stationboard']:
        text += "\n"
        text += "{} {} dest. {} {}\n".format(
            departure['category'],
            departure['number'],
            departure['to'],
            when_is_next(departure['stop']['departureTimestamp'])
        )

    text += "\n\nRefresh results: /st" + station_id

    coordinate = result['station']['coordinate']

    update.message.reply_location(coordinate['x'], coordinate['y'])
    update.message.reply_text(text)


def when_is_next(timestamp):
    seconds = timestamp-time.time()
    minutes = math.floor(seconds/60)
    if minutes < 1:
        return "RUN!"
    if minutes > 60:
        return "> {} h.".format(math.floor(minutes/60))
    return "Dans {} min.".format(minutes)


# Création de l'updater
updater = Updater(bot_token)


# Commande start --> afficher welcome
updater.dispatcher.add_handler(CommandHandler("start", welcome))

# Texte --> rechercher par "query"
updater.dispatcher.add_handler(MessageHandler(Filters.text, search_by_text))

# Coordinates --> rechercher par x et y
updater.dispatcher.add_handler(MessageHandler(Filters.location, search_by_location))

# Un arrêt --> afficher les prochains départs
updater.dispatcher.add_handler(MessageHandler(Filters.command, station_details))


# Déclencher la recherche des messages
updater.start_polling(timeout=2)
updater.idle()
