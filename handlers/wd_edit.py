from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core import pd
from utils.service import WdEditService
from utils.filters import OR_STATE, Button
from utils.filters import OnlyUser
from misc.wd import WdState
from misc.wd_edit import WdEditState


from .wd import main as main_handler

import templates


router = Router(name="wd_edit")


@router.message(OR_STATE(
    WdEditState.name, 
    WdEditState.message, 
    WdEditState.words_add,
    WdEditState.words_remove), OnlyUser(pd))
async def setter(ctx : Message, state : FSMContext):
    """
    * Setter for editing a name group/a message group
    """

    current_state = await state.get_state()
    current_data = await state.get_data()
    table = pd.get_table("word")

    work_group = current_data["current_edit_group_index"]

    # * If user want to go back 
    if await Button(templates.wd_edit.Button.cancel).__call__(ctx):
        ...

    # * If user want to edit a name of group
    elif current_state == WdEditState.name.state:
        # * If name of group has existed already
        if ctx.text in table.index:

            return await ctx.answer(text=templates.wd_edit.edit_name_err)

        await ctx.answer(text=templates.wd_edit.edit_name_success.format(
            last=work_group, new=ctx.text
        ))

        work_group, _ = ctx.text.capitalize(),\
            pd.inplace_index("word",work_group, ctx.text.capitalize())
        
    # ! almost the same code        
    # * If user want to edit a word of group (ADD)
    elif current_state == WdEditState.words_add.state:
        
        new_words = list(set(ctx.text.lower().split()))
        last_worlds = table.at[work_group, "word"]
        all_words = WdEditService.series_words_list(table.get("word"))
        ignore_words = WdEditService.remove_exist(new_words, all_words)
        WdEditService.remove_items(new_words, ignore_words)

        # * If ignore_words is not empty
        await ctx.answer(templates.wd_edit.edit_word_add_ignore.format(
            words=", ".join(ignore_words)
        )) if len(ignore_words) else ...

        # * If new_words is not empty
        await ctx.answer(templates.wd_edit.edit_word_add_success.format(
            name=work_group, words=", ".join(new_words)
        )) if len(new_words) else ...

        pd.inplace_value("word", work_group, "word", last_worlds + new_words)

    # * If user want to edit a word of group (ADD)
    elif current_state == WdEditState.words_remove.state:
        
        new_words = set(ctx.text.lower().split())
        last_words = table.at[work_group, "word"]
        ignore_words = WdEditService.remove_non_exist(new_words, last_words)
        WdEditService.remove_items(new_words, ignore_words)

        # * If ignore_words is not empty
        await ctx.answer(templates.wd_edit.edit_word_remove_ignore.format(
            words=", ".join(ignore_words)
        )) if len(ignore_words) else ...
        
        # * If new_words is not empty
        await ctx.answer(templates.wd_edit.edit_word_remove_success.format(
            name=work_group, words=", ".join(new_words)
        )) if len(new_words) else ...

        pd.inplace_value("word", work_group, "word", last_words)

    else:
        await ctx.answer(templates.wd_edit.edit_message_success.format(
            name=work_group, new=ctx.text
        ))

        pd.inplace_value("word", work_group, "message", ctx.text)

    await main(ctx, state, work_group)

    
@router.message(WdEditState.main, OnlyUser(pd))
async def manager(ctx : Message, state : FSMContext):

    switched_state = templates.wd_edit.state_by_button.get(ctx.text)
    message = templates.wd_edit.text_by_button.get(ctx.text)

    if await Button(templates.wd_edit.Button.cancel).__call__(ctx):
        return await main_handler(ctx, state)
    
    elif not (state and message):
        return await ctx.answer(text=templates.wd_edit.command_err)
    
    await state.set_state(switched_state)
    await ctx.answer(text=message, reply_markup=templates.wd_edit.edit_kb)
    

@router.message(WdState.main, OnlyUser(pd))
async def main(ctx : Message, state : FSMContext, forced_group_name : str = None):
    
    table = pd.get_table("word")
    work_name_group = forced_group_name if forced_group_name else ctx.text
    group = table.loc[work_name_group]

    if group.empty: return await ctx.answer(
        text=templates.wd_edit.group_dont_exist_err
    )


    response_text = templates.wd_edit.text.format(
        group_name=work_name_group,
        group_len=len(group.word),
        create_by=0,
        message=group.message,
        words='\n'.join(sorted(group.word))
    )

    await state.set_state(WdEditState.main)
    await state.update_data(current_edit_group_index=work_name_group)

    await ctx.answer(
        text=response_text,
        reply_markup=templates.wd_edit.kb
    )



