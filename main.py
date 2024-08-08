from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging

from app.handlers import router
from app.database.models import async_main

storage = MemoryStorage()

async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    print("Working")
    print("_______")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
        print("_______")