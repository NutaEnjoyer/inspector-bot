from os import environ
from dotenv import load_dotenv


load_dotenv()

# * Load Token from .env
TOKEN = environ.get("TOKEN") or input("TOKEN = ")
MESSAGE_ARCHIVE_DURATION = environ.get("MESSAGE_ARCHIVE_DURATION") or input("MESSAGE_ARCHIVE_DURATION = ")
USER_CITY_MESSAGE_DELAY = environ.get("USER_CITY_MESSAGE_DELAY") or input("USER_CITY_MESSAGE_DELAY = ")
IGNORE_SPAM_CHAT = environ.get("IGNORE_SPAM_CHAT") or input("IGNORE_SPAM_CHAT = ")
