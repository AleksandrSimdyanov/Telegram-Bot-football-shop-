from aiogram import Bot, Dispatcher
import asyncio
from app.database.models import async_main
from app.handlers.user_handlers import user_router
from app.states.add_order import add_order_router
from app.handlers.admin_hadlers import admin_router
from app.states.do_appeal import do_appeal_router
from app.states.response import response_router
from app.states.mail import mail_router

TOKEN = "7965411958:AAHsv2w2lEkO_gM2j6u046b1-pdFsHMM9lQ"
bot = Bot(TOKEN)
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_routers(user_router, add_order_router, admin_router, do_appeal_router, response_router, mail_router)
    await dp.start_polling(bot)
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")