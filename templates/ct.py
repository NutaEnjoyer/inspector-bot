from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
import numpy as np

class Button:

    create = KeyboardButton(text="🆕 Создать")
    cancel = KeyboardButton(text="◀️ Назад")

    group = lambda name : KeyboardButton(text=name)


action_text = """
<b>Выберите город с которым хотите работать или создайте новый</b>
"""

action_kb = lambda group_list : ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.create, Button.cancel],
    *[[Button.group(name) for name in group_list][i:i + 3] for i in range(0, len([Button.group(name) for name in group_list]), 3)]
])
