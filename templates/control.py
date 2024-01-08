from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


class Button:


    wd = KeyboardButton(text="📕 Словарь")
    ct = KeyboardButton(text="🏙 Город")


start_text = """
Управление
""" 

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.wd],
    [Button.ct]
])