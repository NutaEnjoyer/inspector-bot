from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import pd, bot
from utils.service import WdEditService
from utils.filters import OR_STATE, Button
from utils.filters import OnlyUser
from misc.wd import WdState
from misc.ct import CtState
from misc.ct_edit import CtEditState

from .ct import main as main_handler

import templates
import re
router = Router(name="ct_edit")


@router.message(OR_STATE(
	CtEditState.name,
	CtEditState.message,
	CtEditState.url), OnlyUser(pd))
async def setter(ctx: Message, state: FSMContext):
	"""
	* Setter for editing a name group/a message group
	"""

	current_state = await state.get_state()
	current_data = await state.get_data()
	table = pd.get_table("city")

	work_group = current_data["current_edit_group_index"]

	# * If user want to go back
	if await Button(templates.ct_edit.Button.cancel).__call__(ctx):
		...

	# * If user want to edit a name of group
	elif current_state == CtEditState.name.state:
		# * If name of group has existed already
		if ctx.text in table.index:
			return await ctx.answer(text=templates.ct_edit.edit_name_err)

		await ctx.answer(text=templates.ct_edit.edit_name_success.format(
			last=work_group, new=ctx.text
		))

		work_group, _ = ctx.text.capitalize(), \
						pd.inplace_index("city", work_group, ctx.text.capitalize())

	elif current_state == CtEditState.url.state:
		def rewrite_url(url):
			if url == 'Пропустить':
				return None
			if url[0] == '-' and url[1:].isdigit() or url.isdigit():
				return url
			# Remove "http://" or "https://"
			url = re.sub(r'(http://|https://)', '', url)

			# Remove "t.me/" if present
			url = re.sub(r't.me/', '', url)

			# Remove "@" if present
			url = re.sub(r'@', '', url)

			return '@' + url

		url = rewrite_url(ctx.text)
		if url:
			try:
				chat = await bot.get_chat(url)
			except Exception as e:
				print(e)
				await ctx.answer(
					"Произошла ошибка при добавлении ссылки проверьте правильность набора и наличие прав бота в чате")
				return
		else:
			chat = None
		await ctx.answer(templates.ct_edit.edit_url_success.format(
			name=work_group
		))
		print('edit_chat')
		pd.inplace_value("city", work_group, "channel_url", chat.id if chat else 0)
	else:
		await ctx.answer(templates.ct_edit.edit_message_success.format(
			name=work_group, new=ctx.text
		))

		pd.inplace_value("city", work_group, "message", ctx.text)

	await main(ctx, state, work_group)


@router.message(CtEditState.main, OnlyUser(pd))
async def manager(ctx: Message, state: FSMContext):
	switched_state = templates.ct_edit.state_by_button.get(ctx.text)
	message = templates.ct_edit.text_by_button.get(ctx.text)

	if await Button(templates.ct_edit.Button.cancel).__call__(ctx):
		return await main_handler(ctx, state)

	if await Button(templates.ct_edit.Button.remove).__call__(ctx):
		data = await state.get_data()
		print(data)
		pd.delete("city", data['current_edit_group_index'])
		return await main_handler(ctx, state)


	elif not (state and message):
		return await ctx.answer(text=templates.ct_edit.command_err)

	await state.set_state(switched_state)
	if switched_state == CtEditState.url:
		await ctx.answer(text=message, reply_markup=templates.ct_edit.edit_url_kb)
	else:
		await ctx.answer(text=message, reply_markup=templates.ct_edit.edit_kb)



@router.message(CtState.main, OnlyUser(pd))
async def main(ctx: Message, state: FSMContext, forced_group_name: str = None):
	table = pd.get_table("city")
	work_name_group = forced_group_name if forced_group_name else ctx.text
	group = table.loc[work_name_group]

	if group.empty: return await ctx.answer(
		text=templates.ct_edit.group_dont_exist_err
	)
	chat = 'Отсутствует'
	if group.channel_url:
		try:
			chat = await bot.get_chat(group.channel_url)
			chat = f"<a href='{chat.invite_link}'>{chat.title}</a>"
		except Exception as e:
			print(e)
	response_text = templates.ct_edit.text.format(
		group_name=work_name_group,
		create_by=0,
		message=group.message,
		channel_url=chat
	)

	await state.set_state(CtEditState.main)
	await state.update_data(current_edit_group_index=work_name_group)

	await ctx.answer(
		text=response_text,
		reply_markup=templates.ct_edit.kb
	)



