from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.chat_permissions import ChatPermissions

from utils.table import User, UserStatus, GroupMessage
from utils.filters import OnlyGroup
from utils.service import InspectorService

from core import pd, bot


router = Router(name="inspector")


@router.message(OnlyGroup())
async def main(ctx : Message):
    
    # ! reedit user's message
    response_text = ctx.text.lower().split()
    all_word = pd.get_table("word")
    all_user = pd.get_table("user")

    #lenght_input_data  = len(response_text)
    #start_time_analyze = datetime.now()

    # ! analyze
    for word in response_text:

        messages = all_word["message"].\
            where(all_word["word"].apply(lambda x : word in x)).\
            dropna().\
            reset_index(drop=True)


        if messages.empty:
            continue
        
        # * If words exist
        await ctx.delete()

        message = await ctx.answer(text=messages[0].format(
            user=InspectorService.get_user(ctx)
        ))

        pd.insert("gmsg", GroupMessage(
            index=message.message_id,
            chat_id=message.chat.id,
            sender=message.from_user.id,
            time=datetime.now().timestamp()
        ))

    
        if all_user.at[ctx.from_user.id, "claim"] == 4:
            pd.update_value("user", ctx.from_user, "mute", True)

            try:
                return await bot.restrict_chat_member(
                    chat_id=ctx.chat.id, 
                    user_id=ctx.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=timedelta(days=30)
                )
            except TelegramBadRequest:
                print("Owner")

                return

        
        try:

            all_user.at[ctx.from_user.id, "claim"] += 1
            pd._write()

        except KeyError:
            pd.insert(
                tablename="user", 
                value=User(
                    index=ctx.from_user.id, 
                    registered=datetime.now(), 
                    status=UserStatus.DEFAULT.value,
                    claim=1,
                    mute=False
                ))

        break

    #finish_time_analyze = datetime.now()

    # * Analytics
    # await ctx.answer(text=f"Количество слов: {lenght_input_data}.\nВремя анализа: {(finish_time_analyze - start_time_analyze).total_seconds()} секунд")
            
            


