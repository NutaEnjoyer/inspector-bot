from asyncio import run, get_event_loop
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core import bot, pd
from handlers import routers
from utils.service import DeleterService


async def main():
    """
    * Run bot
    """    

    loop = get_event_loop()

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(routers)
    
    loop.create_task(DeleterService.start_deleter(pd, bot))


    await dp.start_polling(bot)


if __name__ == "__main__":
    
    run(main())
