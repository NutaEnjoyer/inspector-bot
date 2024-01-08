from asyncio import sleep
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramMigrateToChat

from ..pd import PandasDatabase


async def check_message(pd : PandasDatabase, bot : Bot) -> timedelta.seconds:

    table = pd.get_table("gmsg")

    if table.empty:
        return 1
    
    all_message = table.where(table["time"].apply(lambda x : datetime.fromtimestamp(x) < datetime.now()))
    first_index = all_message.first_valid_index()
    delta = datetime.now() - datetime.fromtimestamp(all_message.at[first_index, "time"])
    delta_max = timedelta(minutes=1)

    if delta < delta_max:
        return (delta_max - delta).total_seconds()
    
    try:
        await bot.delete_message(
            chat_id=all_message.at[first_index, "chat_id"], 
            message_id=first_index
        )
    
    except TelegramBadRequest:
        print("message don't exist")
    except TelegramMigrateToChat:
        print("Migrate")

    table = table.drop([first_index], inplace=True)
    pd._write()
    
    return 3


    


async def start_deleter(pd : PandasDatabase, bot : Bot):

    while True:
        delay = await check_message(pd, bot)
        await sleep(delay)




