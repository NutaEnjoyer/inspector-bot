from typing import List
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import pd, bot
from utils.table import Word, City
from utils.service import WdEditService, CtEditService
from utils.filters import Button, OnlyUser
from misc.ct import CtState
from misc.ct_create import CtCreateState, state_by_state, args_by_state, cancel_by_state

from .ct import main as main_handler

import templates

import re

router = Router(name="ct_create")


@router.message(CtCreateState(), Button(templates.ct_create.Button.cancel), OnlyUser(pd))
async def cancel(ctx: Message, state: FSMContext):
	"""
	* The cancel handler of creating
	"""

	current_state = await state.get_state()
	switched_state = cancel_by_state.get(current_state)

	await state.set_state(switched_state)

	if switched_state is not None:
		await ctx.answer(
			text=templates.ct_create.text_by_state[switched_state.state],
			reply_markup=templates.ct_create.kb_by_state[switched_state.state]
		)

		return

	await main_handler(ctx, state)


@router.message(CtCreateState(), OnlyUser(pd))
async def creating(ctx: Message, state: FSMContext):
	"""
	* The middle handler of creating
	"""

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

		return '@'+url

	current_state = await state.get_state()

	if current_state == CtCreateState.url:
		print('state it')
		url = rewrite_url(ctx.text)
		print(url)
		if url:
			try:
				chat = await bot.get_chat(url)
			except Exception as e:
				print(e)
				await ctx.answer("Произошла ошибка при добавлении ссылки проверьте правильность набора и наличие прав бота в чате")
				return
		else:
			chat = None
	switched_state = state_by_state.get(current_state)
	# all_words = CtEditService.series_words_list(pd.get_table("city").get(["name"]))

	ignore_is_pressed = None

	await state.update_data(**{args_by_state[current_state]: ctx.text if not ignore_is_pressed else ""})
	await state.set_state(switched_state)

	# * If state exists

	if switched_state is not None:
		await ctx.answer(
			text=templates.ct_create.text_by_state[switched_state.state],
			reply_markup=templates.ct_create.kb_by_state[switched_state.state]
		)

		return

	# * When state finished
	data, args = await state.get_data(), list(args_by_state.values())



	# * Add a new group at database
	pd.insert("city", City(
		index=data.get(args[0]),
		message=data.get(args[1]),
		channel_url=chat.id if chat else 0
	))

	await main_handler(ctx, state)


@router.message(Button(templates.wd.Button.create), CtState.main, OnlyUser(pd))
async def main(ctx: Message, state: FSMContext):
	"""
	* The start handler of creating
	"""
	await state.set_state(current_state := CtCreateState.name)

	await ctx.answer(
		text=templates.ct_create.text_by_state[current_state.state],
		reply_markup=templates.ct_create.kb_by_state[current_state.state]
	)



