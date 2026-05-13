import asyncio
import logging
import os
import redis
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ParseMode, Message, CallbackQuery
from aiogram.utils import executor

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
            log.info(f"Redis connected using {url}")
            return r
        except Exception as e:
            log.warning(f"Redis {url} failed: {e}")
    log.warning("Redis not available - continuing without memory")
    return None

r = init_redis()

# ---------- Bot setup ----------
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    log.error("TELEGRAM_TOKEN not set")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# ---------- Helper: check if bot mentioned ----------
async def is_mentioned(message: Message) -> bool:
    try:
        bot_user = await bot.get_me()
        mentioned = f'@{bot_user.username}'.lower() in message.text.lower()
        return mentioned
    except:
        return False

# ---------- Commands ----------
@dp.message_handler(commands=['start', 'menu'])
async def cmd_menu(message: Message):
    await message.answer("🔥 SLH Master Bot v3.14\n\nבחר קטגוריה:\n/menu")

@dp.message_handler(commands=['status'])
async def cmd_status(message: Message):
    await message.answer("🟢 SLH Ecosystem v3.14 — Online")

@dp.message_handler(commands=['health'])
async def cmd_health(message: Message):
    await message.answer("✅ Bot healthy")

@dp.message_handler(commands=['remember'])
async def cmd_remember(message: Message):
    if not r:
        await message.answer("❌ Redis not available. Can't remember.")
        return
    fact = message.get_args()
    if fact:
        r.sadd(f"user:{message.from_user.id}:facts", fact)
        await message.answer("🧠 Remembered!")
    else:
        await message.answer("Usage: /remember <fact>")

@dp.message_handler(commands=['facts'])
async def cmd_facts(message: Message):
    if not r:
        await message.answer("❌ Redis not available. No facts.")
        return
    facts = r.smembers(f"user:{message.from_user.id}:facts")
    if facts:
        await message.answer("\n".join(facts), parse_mode=ParseMode.HTML)
    else:
        await message.answer("No facts found.")

# ---------- Handle text (check mention) ----------
@dp.message_handler()
async def on_text(message: Message):
    if await is_mentioned(message):
        await message.reply("I'm here! Use /menu for commands.")

# ---------- Main ----------
if __name__ == '__main__':
    log.info("🚀 SLH Master Bot v3.14 FINAL")
    log.info("Start polling")
    executor.start_polling(dp, skip_updates=True)
