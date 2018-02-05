# File bot.py

"""
Launch script with a command like
   python bot.py "123456:ThisIsYourChatBotToken"
"""

import sys

botToken = sys.argv[1]

print("Starting bot for token:", botToken)