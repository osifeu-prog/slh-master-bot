import asyncio
import logging
import os
import sys

sys.path.append(os.getcwd())

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import redis as redis_lib

from handlers import menu
from handlers import agent
from handlers import xp
from handlers import legacy
from handlers import audit
from handlers import payment

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)

def init_redis():
    for url in [os.getenv("REDIS_URL"), "redis://slh-redis-v3:6379", "redis://localhost:6379"]:
        if not url: continue
        try:
            r = redis_lib.from_url(url, decode_responses=True, socket_timeout=5)
            r.ping()
            log.info(f"✅ Redis connected: {url}")
            return r
        except Exception as e:
            log.warning(f"Redis failed: {e}")
    log.warning("⚠️ Redis not available")
    return None

r = init_redis()

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    log.error("❌ TELEGRAM_TOKEN not set")
    sys.exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(menu.router)
dp.include_router(agent.router)
dp.include_router(xp.router)
dp.include_router(legacy.router)
dp.include_router(audit.router)
dp.include_router(payment.router)

@dp.message(Command("start", "status", "menu"))
async def cmd_status(message: Message):
    await message.answer("🟢 <b>SLH Master Bot v8.0</b> - Online\nEcosystem: DILIGENT-RADIANCE", parse_mode=ParseMode.HTML)

async def main():
    log.info("🚀 Starting Bot Polling...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())





