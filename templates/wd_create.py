from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from misc.wd_create import WdCreateState


class Button:
    
    rm = ReplyKeyboardRemove()
    cancel = KeyboardButton(text="◀️ Назад")
    ignore = KeyboardButton(text="⏪ Пропустить")

name_text = """
<b>Как назвать новую группу слов?</b>
"""

name_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.cancel]
])


message_text = """
<b>Напишите сообщение, которое должно отправиться при активации этой группы</b>
"""
message_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.cancel]
])


words_text = """
<b>Отправьте слова для добавления в эту группу</b>

<i>Пишите слова <b>через пробел</b>.</i>

"""

words_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.ignore],
    [Button.cancel]
])



text_by_state = {
    WdCreateState.name.state : name_text,
    WdCreateState.message.state : message_text,
    WdCreateState.words.state : words_text
}

kb_by_state = {
    WdCreateState.name.state : name_kb,
    WdCreateState.message.state : message_kb,
    WdCreateState.words.state : words_kb
}