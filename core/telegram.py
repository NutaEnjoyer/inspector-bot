from aiogram import Bot
from aiogram.enums import ParseMode

from utils import config


# * Init telegram bot
bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

