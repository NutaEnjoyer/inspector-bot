from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from misc.ct_create import CtCreateState


class Button:
	rm = ReplyKeyboardRemove()
	cancel = KeyboardButton(text="◀️ Назад")
	skip = KeyboardButton(text="Пропустить")

name_text = """
<b>Как назвать новый город?</b>
"""

name_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
	[Button.cancel]
])

message_text = """
<b>Напишите сообщение, которое должно отправиться при активации этого города</b>
"""

words_text = """
<b>Отправьте слова для добавления в группу этого города</b>

<i>Пишите слова <b>через пробел</b>.</i>
"""

url_text = """
<b>Пришлите ссылку или айди чата. Если это открытый чат вы можете прислать ссылку в формате:
http://t.me/chat или t.me/chat или @chat</b>

Если чат закрытый пришлите id
"""
message_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
	[Button.cancel]
])

words_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
	[Button.cancel]
])

url_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
	[Button.skip],
	[Button.cancel]
])

text_by_state = {
	CtCreateState.name.state: name_text,
	CtCreateState.message.state: message_text,
	CtCreateState.words.state: words_text,
	CtCreateState.url.state: url_text,
}

kb_by_state = {
	CtCreateState.name.state: name_kb,
	CtCreateState.message.state: message_kb,
	CtCreateState.words.state: words_kb,
	CtCreateState.url.state: url_kb,
}