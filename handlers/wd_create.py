from typing import List
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from core import pd
from utils.table import Word
from utils.service import WdEditService
from utils.filters import Button, OnlyUser
from misc.wd import WdState
from misc.wd_create import WdCreateState, state_by_state, args_by_state, cancel_by_state


from .wd import main as main_handler

import templates


router = Router(name="wd_create")


@router.message(WdCreateState(), Button(templates.wd_create.Button.cancel), OnlyUser(pd))
async def cancel(ctx : Message, state : FSMContext):
    """
    * The cancel handler of creating 
    """

    current_state = await state.get_state()
    switched_state = cancel_by_state.get(current_state)

    await state.set_state(switched_state)

    if switched_state is not None:

        await ctx.answer(
            text=templates.wd_create.text_by_state[switched_state.state],
            reply_markup=templates.wd_create.kb_by_state[switched_state.state]
        ) 

        return
    
    await main_handler(ctx, state)


@router.message(WdCreateState(), OnlyUser(pd))
async def creating(ctx : Message, state : FSMContext):
    """
    * The middle handler of creating 
    """


    current_state = await state.get_state()
    switched_state = state_by_state.get(current_state)
    all_words = WdEditService.series_words_list(pd.get_table("word").get(["word"]))
    
    ignore_is_pressed = await Button(templates.wd_create.Button.ignore).__call__(ctx)

    
    await state.update_data(**{args_by_state[current_state] : ctx.text if not ignore_is_pressed else ""})
    await state.set_state(switched_state)

    # * If state exists
    if switched_state is not None:

        await ctx.answer(
            text=templates.wd_create.text_by_state[switched_state.state],
            reply_markup=templates.wd_create.kb_by_state[switched_state.state]
        ) 

        return
    
    # * When state finished
    data, args = await state.get_data(), list(args_by_state.values())
    print(data, args)
    new_words : List[str] = data.get(args[2]).lower().split()
    all_words = WdEditService.series_words_list(pd.get_table("word").get("word"))
    ignore_words = WdEditService.remove_exist(new_words, all_words)
    WdEditService.remove_items(new_words, ignore_words)

    # * If ignore_words is not empty
    await ctx.answer(templates.wd_edit.edit_word_add_ignore.format(
        words=", ".join(ignore_words)
    )) if len(ignore_words) else ...

    # * Add a new group at database
    pd.insert("word", Word(
        index=data.get(args[0]),
        message=data.get(args[1]),
        word=new_words
    ))

    await main_handler(ctx, state)

    
    
@router.message(Button(templates.wd.Button.create), WdState.main, OnlyUser(pd))
async def main(ctx : Message, state : FSMContext):
    """
    * The start handler of creating 
    """
    await state.set_state(current_state:=WdCreateState.name)

    await ctx.answer(
        text=templates.wd_create.text_by_state[current_state.state],
        reply_markup=templates.wd_create.kb_by_state[current_state.state]
    )



