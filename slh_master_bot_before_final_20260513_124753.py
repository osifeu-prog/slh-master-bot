import asyncio
import logging
import os
import redis
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)

# ---------- Redis connection with auto-discovery ----------
def init_redis():
    candidates = [
        os.getenv("REDIS_URL"),
        "redis://redis-volume:6379",
        "redis://redis.railway.internal:6379",
        "redis://localhost:6379"
    ]
    for url in candidates:
        if not url:
            continue
        try:
            r = redis.from_url(url, decode_responses=True, socket_timeout=5)
            r.ping()
            log.info(f"✅ Redis connected using {url}")
            return r
        except Exception as e:
            log.warning(f"Redis {url} failed: {e}")
    log.warning("⚠️ Redis not available - continuing without memory")
    return None

r = init_redis()

# ---------- Bot setup ----------
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    log.error("TELEGRAM_TOKEN not set")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ---------- Helper: check if bot mentioned ----------
async def is_mentioned(message: Message) -> bool:
    try:
        me = await bot.get_me()
        mentioned = f'@{me.username}'.lower() in message.text.lower()
        return mentioned
    except:
        return False

# ---------- Commands ----------
@dp.message(Command("start", "menu"))
async def cmd_menu(message: Message):
    await message.answer("🔥 SLH Master Bot v3.14\n\nבחר קטגוריה:\n/menu")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer("🟢 SLH Ecosystem v3.14 — Online")

@dp.message(Command("health"))
async def cmd_health(message: Message):
    await message.answer("✅ Bot healthy")

@dp.message(Command("remember"))
async def cmd_remember(message: Message):
    if not r:
        await message.answer("❌ Redis not available. Can't remember.")
        return
    fact = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if fact:
        r.sadd(f"user:{message.from_user.id}:facts", fact)
        await message.answer("🧠 Remembered!")
    else:
        await message.answer("Usage: /remember <fact>")

@dp.message(Command("facts"))
async def cmd_facts(message: Message):
    if not r:
        await message.answer("❌ Redis not available. No facts.")
        return
    facts = r.smembers(f"user:{message.from_user.id}:facts")
    if facts:
        await message.answer("\n".join(facts))
    else:
        await message.answer("No facts found.")

# ---------- Handle text (check mention) ----------
@dp.message()
async def on_text(message: Message):
    if await is_mentioned(message):
        await message.reply("I'm here! Use /menu for commands.")

# ---------- Main ----------
async def main():
    log.info("🚀 SLH Master Bot v3.14 FINAL")
    log.info("Start polling")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
