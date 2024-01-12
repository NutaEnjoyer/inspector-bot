from os import environ
from dotenv import load_dotenv


load_dotenv()

# * Load Token from .env
TOKEN = environ.get("TOKEN") or input("TOKEN = ")
MESSAGE_ARCHIVE_DURATION = environ.get("MESSAGE_ARCHIVE_DURATION") or input("MESSAGE_ARCHIVE_DURATION = ")
