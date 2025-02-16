import asyncio
from aiogram import Bot, Dispatcher
import config as cfg
from handlers import start

async def main():

    bot = Bot(token=cfg.TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
   
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    asyncio.run(main())