from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import pd
from misc.wd import WdState
from utils.filters import Button, OnlyUser

from .control import start as start_handler

import templates


router = Router(name="wd")


@router.message(Button(templates.control.Button.wd), OnlyUser(pd))
async def main(ctx : Message, state : FSMContext):

    await state.set_state(WdState.main)

    await ctx.answer(
        text=templates.wd.action_text,
        reply_markup=templates.wd.action_kb(pd.get_table("word").index)
    )

    


@router.message(Button(templates.wd.Button.cancel), WdState.main, OnlyUser(pd))
async def cancel(ctx : Message, state : FSMContext):
    await start_handler(ctx, state)


