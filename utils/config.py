from os import environ
from dotenv import load_dotenv


load_dotenv()

# * Load Token from .env
TOKEN = environ.get("TOKEN") or input("TOKEN = ")
MESSAGE_ARCHIVE_DURATION = int(environ.get("MESSAGE_ARCHIVE_DURATION")) or int(input("MESSAGE_ARCHIVE_DURATION = "))
USER_CITY_MESSAGE_DELAY = int(environ.get("USER_CITY_MESSAGE_DELAY")) or int(input("USER_CITY_MESSAGE_DELAY = "))
IGNORE_SPAM_CHAT = environ.get("IGNORE_SPAM_CHAT").split('|') or input("IGNORE_SPAM_CHAT = ").split('|')
