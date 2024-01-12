import random
from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.chat_permissions import ChatPermissions

from utils.models import MessageArchive
from utils.table import User, UserStatus, GroupMessage
from utils.filters import OnlyGroup, OnlyUser, OnlyDefaultUser
from utils.service import InspectorService

from core import pd, bot


router = Router(name="inspector")



@router.message(OnlyGroup(), OnlyUser(pd))
async def main(ctx: Message):

    if ctx.text:
        response_text = ctx.text.lower()
        txt = ctx.text
    elif ctx.caption:
        response_text = ctx.caption.lower()
        txt = ctx.caption
    else:
        return

    all_city = pd.get_table("city")

    all_user = pd.get_table("user")


    # ! analyze

    def city_analyze():
        indexes = list(all_city.index.values)
        msgs = list(all_city.message.values)
        chnl_urls = list(all_city.channel_url.values)
        cities = []
        for i in range(len(indexes)):
            if indexes[i].lower() in response_text:
                cities.append([msgs[i], chnl_urls[i]])
        return cities

    def analyze(x):
        if not x: return
        for word in x:

            if response_text.find(word) >= 0:
                return True

    cities = all_city["message"]. \
        where(all_city["word"].apply(analyze)). \
        dropna(). \
        reset_index(drop=True)
    cities2 = all_city["channel_url"]. \
        where(all_city["word"].apply(analyze)). \
        dropna(). \
        reset_index(drop=True)

    if cities is not None and len(cities) > 0:
           # help(cities["message"])
        message = await ctx.reply(text=cities[0].format(
                user=InspectorService.get_user(ctx)
            ))
        pd.insert("gmsg", GroupMessage(
                index=message.message_id,
                chat_id=message.chat.id,
                sender=message.from_user.id,
                time=datetime.now().timestamp()
            ))
        if cities2[0] is not None and cities2[0] != 0:
            print(cities2[0])
            chat = await bot.get_chat(cities2[0])
            try:
                user_text = f"""<a href="{ctx.from_user.url}">{ctx.from_user.first_name}</a>"""
                text = f"""{txt}\n\nUsername: @{ctx.from_user.username}\nАвтор: {user_text}"""
                await bot.send_message(chat.id, text)

            except Exception as e:
                print(f'Exception while forward message: {e}')
        else:
            return

    pd.insert("gmsg", GroupMessage(
        index=message.message_id,
        chat_id=message.chat.id,
        sender=message.from_user.id,
        time=datetime.now().timestamp()
    ))


@router.message(OnlyGroup())
async def main(ctx : Message):
    # ! reedit user's message

    if ctx.text:
        response_text = ctx.text.lower()
        txt = ctx.text
    elif ctx.caption:
        response_text = ctx.caption.lower()
        txt = ctx.caption
    else:
        return

    # pd.insert(
    #     tablename="user",
    #     value=User(
    #         index=2134081408,
    #         registered=datetime.now().timestamp(),
    #         status=UserStatus.ADMIN.value,
    #         claim=0,
    #         mute=False
    #     ))
    
    all_word = pd.get_table("word")
    all_city = pd.get_table("city")
    all_user = pd.get_table("user")

    # pd.delete("city", index=all_city.index[0])
    #lenght_input_data  = len(response_text)
    #start_time_analyze = datetime.now()

    # ! analyze

    def analyze(x):
        if not x: return
        for word in x:
            
            if response_text.find(word) >= 0:
                return True

    def city_analyze():
        indexes = list(all_city.index.values)
        msgs = list(all_city.message.values)
        chnl_urls = list(all_city.channel_url.values)
        cities = []
        for i in range(len(indexes)):
            if indexes[i].lower() in response_text:
                cities.append([msgs[i], chnl_urls[i]])
        return cities



    messages = all_word["message"].\
        where(all_word["word"].apply(analyze)).\
        dropna().\
        reset_index(drop=True)

    cities = all_city["message"]. \
        where(all_city["word"].apply(analyze)). \
        dropna(). \
        reset_index(drop=True)
    cities2 = all_city["channel_url"]. \
        where(all_city["word"].apply(analyze)). \
        dropna(). \
        reset_index(drop=True)

    if messages.empty:
        try:
            new_message = MessageArchive.create(text=response_text)
            new_message.save()
        except Exception as e:
            await ctx.delete()
            return

        if cities is not None and len(cities) > 0:
            # help(cities["message"])
            message = await ctx.reply(text=cities[0].format(
                user=InspectorService.get_user(ctx)
            ))
            pd.insert("gmsg", GroupMessage(
                index=message.message_id,
                chat_id=message.chat.id,
                sender=message.from_user.id,
                time=datetime.now().timestamp()
            ))
            if cities2[0] is not None and cities2[0] != 0:
                print(cities2[0])
                chat = await bot.get_chat(cities2[0])
                try:
                    user_text = f"""<a href="{ctx.from_user.url}">{ctx.from_user.first_name}</a>"""
                    text = f"""{txt}\n\nUsername: @{ctx.from_user.username}\nАвтор: {user_text}"""
                    # url = ctx.get_url()
                    # text = f"""{txt}\n\nАвтор: {ctx.from_user.first_name}\nПост: <a href="{url}">ссылка</a>"""
                    await bot.send_message(chat.id, text)

                except Exception as e:
                    print(f'Exception while forward message: {e}')
        else:
            return

        return

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

    try:
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
    except KeyError:
        pass

    try:

        all_user.at[ctx.from_user.id, "claim"] += 1
        pd._write()

    except KeyError:
        pd.insert(
            tablename="user", 
            value=User(
                index=ctx.from_user.id, 
                registered=datetime.now().timestamp(),
                status=UserStatus.DEFAULT.value,
                claim=1,
                mute=False
            ))


    #finish_time_analyze = datetime.now()

    # * Analytics
    # await ctx.answer(text=f"Количество слов: {lenght_input_data}.\nВремя анализа: {(finish_time_analyze - start_time_analyze).total_seconds()} секунд")




