from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from core import pd
from utils.filters import OnlyUser
import templates


router = Router(name="control")


@router.message(CommandStart(deep_link=False), OnlyUser(pd))
async def start(ctx : Message, state : FSMContext):
    """
    * Called the command /start
    """
    
    await state.set_state()

    await ctx.answer(
        text=templates.control.start_text,
        reply_markup=templates.control.start_kb
    )