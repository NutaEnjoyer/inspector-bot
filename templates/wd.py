from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


class Button:

    create = KeyboardButton(text="🆕 Создать")
    cancel = KeyboardButton(text="◀️ Назад")

    group = lambda name : KeyboardButton(text=name)


action_text = """
<b>Выберите группу с которой хотите работать или создайте новую</b>
"""

action_kb = lambda group_list : ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.create, Button.cancel],
    *[[Button.group(name)] for name in group_list]
])