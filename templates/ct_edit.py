from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from misc.ct_edit import CtEditState


class Button:

    name = KeyboardButton(text="📧 Изменить имя города")
    message = KeyboardButton(text="💬 Изменить сообщение")
    url = KeyboardButton(text="🔗 Изменить чат")
    remove = KeyboardButton(text="🗑 Удалить город")
    cancel = KeyboardButton(text="◀️ Назад")
    skip = KeyboardButton(text="Пропустить")


group_dont_exist_err = """
⚠️ <b>Такого города не существует!</b>
"""

command_err = """
⚠️ <b>Такой команды не существует!</b>
"""

text = """
<b>Название города:</b> <i>{group_name}</i>
<b>Город создан:</b> <i>{create_by}</i>

<b>Сообщение города:</b>
{message}

<b>Чат для перессылки сообщений:</b>
{channel_url}
"""


edit_name = """
<b>Отправьте новое имя города</b>
"""

edit_name_success = """
✅ <b>Новое имя для города</b> <i>{last}</i> <b>было успешно установлено как</b> <i>{new}</i>
"""

edit_name_err = """
⚠️ <b>Нельзя использовать это имя, потому что такой город уже существует!</b>
"""

edit_message = """
Отправьте новое сообщение для города
"""
remove_city = """
Город удален
"""

edit_url = """
<b>Пришлите ссылку или айди чата. Если это открытый чат вы можете прислать ссылку в формате:
http://t.me/chat или t.me/chat или @chat</b>

Если чат закрытый пришлите id
"""

edit_message_success = """
✅ <b>Новое сообщение для города</b> <i>{name}</i> <b>было успешно установлено как</b> 

<i>{new}</i>

"""

edit_url_success = """
✅ <b>Новый чат для города</b> <i>{name}</i> <b>был успешно установлен</b> 

"""

edit_url_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.skip],
    [Button.cancel]
])

edit_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.cancel]
])

kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.message, Button.name],
    [Button.url],
    [Button.remove],
    [Button.cancel]
])


state_by_button = {
    Button.name.text : CtEditState.name,
    Button.message.text : CtEditState.message,
    Button.url.text: CtEditState.url,
}

text_by_button = {
    Button.name.text : edit_name,
    Button.message.text : edit_message,
    Button.url.text : edit_url,
    Button.remove.text: remove_city,
}