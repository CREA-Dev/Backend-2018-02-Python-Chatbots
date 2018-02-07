# File bot.py

"""
Launch script with a command like
   python bot.py "123456:ThisIsYourChatBotToken"
"""

import sys, logging, requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


# Method to get all the data from open data
def get_data_from_opendata(path):
    url = "http://transport.opendata.ch/v1" + path
    r = requests.get(url)
    return r.json()



# We put some identifiers in variables
STATE_INSTRUCTIONS = 1
STATE_LOCATION = 2
STATE_STATIONS = 3


def start(bot, update):
    update.message.reply_text(
        'Hello {} !'.format(update.message.from_user.first_name)
    )

    return show_instructions(bot, update) # Show two states in a row

def show_instructions(bot, update):
    update.message.reply_text(
        "Veuillez envoyer une localisation"
    )
    return STATE_LOCATION

# Collecting user location
def collect_stops_from_text(bot, update):
    stops = get_data_from_opendata("/locations?query=" + update.message.text)
    return show_stops(bot, update, stops)

def collect_stops_from_location(bot, update):
    user_location = update.message.location
    stops = get_data_from_opendata("/locations?x={}&y={}".format(user_location.latitude,user_location.longitude))
    return show_stops(bot, update, stops)

def show_stops(bot, update, stops):
    text = "Please select a stop:\n"
    for station in stops['stations']:
        if 'id' in station and station[
            'id'] is not None:  # We also get the address of the current point, so we need to check
            text += "\n"  # new line
            text += "/stop" + station['id'] + " - " + station['name']  # showing the name and a command

    update.message.reply_text(
        text
    )

    return STATE_STATIONS

# Show results
def show_results(bot, update):
    id = update.message.text[5:] # remove the 5 first characters

    station = get_data_from_opendata("/stationboard?id={}".format(id))

    # Sending coordinates
    coordinate = station['station']['coordinate']
    update.message.reply_location(coordinate['x'], coordinate['y'])

    # Sending next departures
    text = "Prochains départs:\n"
    for departure in station['stationboard']:
        text += "\n"
        if 'category' in departure and departure['category']:
            text += departure['category'] + " "
        if 'number' in departure and departure['number']:
            text += departure['number'] + " "
        if 'to' in departure and departure['to']:
            text += "-> {} ".format(departure['to'])

    update.message.reply_text(
        text
    )

# Showing debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


# Creation of a conversation handler
conv_handler = ConversationHandler(
        entry_points = [
            CommandHandler('start', start)
        ],

        states = {
            STATE_INSTRUCTIONS: [], # Not necessary, as we don't move to it (substate)

            STATE_LOCATION: [
                CommandHandler('help', show_instructions),
                MessageHandler(Filters.location, collect_stops_from_location),
                MessageHandler(Filters.text, collect_stops_from_text)
            ],

            STATE_STATIONS: [
                CommandHandler('restart', start),
                MessageHandler(Filters.command, show_results) # Any command, to collect the stop id
            ],
        },
        fallbacks = []
    )

updater = Updater(sys.argv[1]) # Avec notre token en argument

updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
