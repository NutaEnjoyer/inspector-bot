from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import pd
from misc.ct import CtState
from utils.filters import Button, OnlyUser

from .control import start as start_handler

import templates

router = Router(name="ct")


@router.message(Button(templates.control.Button.ct), OnlyUser(pd))
async def main(ctx: Message, state: FSMContext):
	await state.set_state(CtState.main)

	await ctx.answer(
		text=templates.ct.action_text,
		reply_markup=templates.ct.action_kb(pd.get_table("city").index)
	)


@router.message(Button(templates.ct.Button.cancel), CtState.main, OnlyUser(pd))
async def cancel(ctx: Message, state: FSMContext):
	await start_handler(ctx, state)


