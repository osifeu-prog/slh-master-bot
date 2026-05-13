import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# טעינת משתני סביבה
load_dotenv("D:\\SLH_ECOSYSTEM\\.env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")

# התחברות ל-Redis (לגיבוי, locking, state)
import redis.asyncio as redis
redis_client = None
if REDIS_URL:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# לוגים
logging.basicConfig(level=logging.INFO)

# יצירת הבוט
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# יבוא כל ה-handlers
from handlers import admin, agent, audit, legacy, menu, payment, sales, xp, osif

dp.include_router(admin.router)
dp.include_router(agent.router)
dp.include_router(audit.router)
dp.include_router(legacy.router)
dp.include_router(menu.router)
dp.include_router(payment.router)
dp.include_router(sales.router)
dp.include_router(xp.router)
dp.include_router(osif.router)

# פקודת start
@dp.message()
async def fallback(message):
    await message.answer("🟢 SLH Master Bot v8.0 - Online\nEcosystem: DILIGENT-RADIANCE")

async def main():
    # מנגנון Lock למניעת כפילויות (אם Redis זמין)
    if redis_client:
        lock = redis_client.lock("telegram_bot_lock", timeout=30)
        acquired = await lock.acquire(blocking=False)
        if not acquired:
            logging.error("Another bot instance is running. Exiting.")
            return
        logging.info("✅ Lock acquired")
    else:
        logging.warning("Redis not available  lock disabled")

    logging.info("🚀 Starting bot polling...")
    await dp.start_polling(bot)

    if redis_client:
        await lock.release()
        logging.info("🔓 Lock released")

if __name__ == "__main__":
    asyncio.run(main())
