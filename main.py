import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# ????? ????? ?????
load_dotenv("D:\\SLH_ECOSYSTEM\\.env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")

# ??????? ?-Redis (??????, locking, state)
import redis.asyncio as redis
redis_client = None
if REDIS_URL:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# ?????
logging.basicConfig(level=logging.INFO)

# ????? ????
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ???? ?? ?-handlers
from handlers.admin import router as admin_router
from handlers.agent import router as agent_router
from handlers.audit import router as audit_router
from handlers.legacy import router as legacy_router
from handlers.menu import router as menu_router
from handlers.payment import router as payment_router
from handlers.sales import router as sales_router
from handlers.xp import router as xp_router
from handlers.osif import router as osif_router

print("? registering admin router"); dp.include_router(admin_router)
dp.include_router(agent_router)
print("? registering audit router"); dp.include_router(audit_router)
dp.include_router(legacy_router)
dp.include_router(menu_router)
dp.include_router(payment_router)
dp.include_router(sales_router)
print("? registering xp router"); dp.include_router(xp_router)
dp.include_router(osif_router)

# ????? start
@dp.message()
async def fallback(message):
    await message.answer("?? SLH Master Bot v8.0 - Online\nEcosystem: DILIGENT-RADIANCE")

async def main():
    # ?????? Lock ?????? ???????? (?? Redis ????)
    if redis_client:
        lock = redis_client.lock("telegram_bot_lock", timeout=30)
        acquired = await lock.acquire(blocking=False)
        if not acquired:
            logging.error("Another bot instance is running. Exiting.")
            return
        logging.info("? Lock acquired")
    else:
        logging.warning("Redis not available  lock disabled")

    logging.info("?? Starting bot polling...")
    await dp.start_polling(bot)

    if redis_client:
        await lock.release()
        logging.info("?? Lock released")

if __name__ == "__main__":
    asyncio.run(main())


