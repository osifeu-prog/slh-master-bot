import asyncio, logging, os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers import menu, agent, xp, legacy, audit, payment

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("MASTER_BOT_TOKEN")
if not TOKEN: raise SystemExit("MASTER_BOT_TOKEN not set")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(menu.router)
dp.include_router(agent.router)
dp.include_router(xp.router)
dp.include_router(legacy.router)
dp.include_router(audit.router)
dp.include_router(payment.router)

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
