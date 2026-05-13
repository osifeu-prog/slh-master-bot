import asyncio, logging, os, sys
sys.path.append(os.getcwd())

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import redis as redis_lib
from handlers import menu
from handlers import agent

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
            log.warning(f"Redis {url} failed: {e}")
    return None

r = init_redis()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    log.error("TELEGRAM_TOKEN not set"); sys.exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(menu.router)`ndp.include_router(agent.router)

@dp.message(Command("start", "status"))
async def cmd_status(message: Message):
    await message.answer("🟢 SLH Master Bot v3.14 - Online\nEcosystem: DILIGENT-RADIANCE")

async def main():
    log.info("🚀 Starting Bot Polling...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
