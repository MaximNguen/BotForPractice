from config import TOKEN
from aiogram import Bot, Dispatcher
import asyncio
import logging
from app.handlers import router

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    print("Working")
    print("_______")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
        print("________")