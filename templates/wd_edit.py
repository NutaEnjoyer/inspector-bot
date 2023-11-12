from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from misc.wd_edit import WdEditState


class Button:

    name = KeyboardButton(text="📧 Изменить имя группы")
    message = KeyboardButton(text="💬 Изменить сообщение")
    remove = KeyboardButton(text="🗑 Удалить слова")
    add = KeyboardButton(text="🆕 Добавить слова")
    cancel = KeyboardButton(text="◀️ Назад")


group_dont_exist_err = """
⚠️ <b>Такой группы не существует!</b>
"""

command_err = """
⚠️ <b>Такой команды не существует!</b>
"""

text = """
<b>Название группы:</b> <i>{group_name}</i>
<b>Количество слов в группе:</b> <i>{group_len}</i>
<b>Группа создана:</b> <i>{create_by}</i>

<b>Сообщение группы:</b>
{message}

<b>Слова группы:</b>
{words}
"""

edit_word_add = """
Отправьте слова <b>через проблем</b>, чтобы <b>добавить</b> из в группу
"""

edit_word_add_success = """
✅ <b>Новое слова:</b> <i>{words}</i> <b>были успешно добавлены в группу</b> <i>{name}</i>
"""

edit_word_add_ignore = """
🆗 <b>Слова:</b> <i>{words}</i> <b>были игнорированы!</b>

ℹ️ <i>Эти слова уже существуют в другой группе!</i>
"""

edit_word_remove = """
Отправьте слова <b>через проблем</b>, чтобы <b>удалить></b> из в группу
"""

edit_word_remove_success = """
✅ <b>Слова:</b> <i>{words}</i> <b>были успешно удалены из группы</b> <i>{name}</i>
"""

edit_word_remove_ignore = """
🆗 <b>Слова:</b> <i>{words}</i> <b>были игнорированы!</b>
"""

edit_name = """
<b>Отправьте новое имя группы</b>
"""

edit_name_success = """
✅ <b>Новое имя для группы</b> <i>{last}</i> <b>было успешно установлено как</b> <i>{new}</i>
"""

edit_name_err = """
⚠️ <b>Нельзя использовать это имя, потому что такая группа уже существует!</b>
"""

edit_message = """
Отправьте новое сообщение для группы
"""

edit_message_success = """
✅ <b>Новое сообщение для группы</b> <i>{name}</i> <b>было успешно установлено как</b> 

<i>{new}</i>

"""

edit_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.cancel]
])

kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [Button.add, Button.remove],
    [Button.message],
    [Button.name],
    [Button.cancel]
])


state_by_button = {
    Button.name.text : WdEditState.name,
    Button.message.text : WdEditState.message,
    Button.add.text : WdEditState.words_add,
    Button.remove.text : WdEditState.words_remove
}

text_by_button = {
    Button.name.text : edit_name,
    Button.message.text : edit_message,
    Button.add.text : edit_word_add,
    Button.remove.text : edit_word_remove
}