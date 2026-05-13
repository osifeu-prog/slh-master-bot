import asyncio
import logging
import os
import redis
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger(__name__)

def init_redis():
    url = os.getenv("REDIS_URL")
    if not url:
        log.warning("REDIS_URL not set")
        return None
    try:
        r = redis.from_url(url, decode_responses=True, socket_timeout=5)
        r.ping()
        log.info("✅ Redis connected")
        return r
    except Exception as e:
        log.warning(f"Redis not available: {e}")
        return None

r = init_redis()

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    log.error("TELEGRAM_TOKEN not set")
    sys.exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start", "menu"))
async def cmd_menu(message: Message):
    await message.answer("🔥 *SLH Master Bot v3.14*\n\n"
                         "Available commands:\n"
                         "/status  Bot health\n"
                         "/remember <fact>  Store a fact\n"
                         "/facts  Show your facts\n"
                         "/todo  Show task list\n"
                         "/task_add <task>  Add a task\n"
                         "/task_done <line>  Mark task as done",
                         parse_mode="Markdown")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer("🟢 SLH Ecosystem v3.14 — Online\nEnvironment: DILIGENT-RADIANCE")

@dp.message(Command("health"))
async def cmd_health(message: Message):
    await message.answer("✅ Bot healthy")

@dp.message(Command("remember"))
async def cmd_remember(message: Message):
    if not r:
        await message.answer("❌ Redis not available. Can't remember.")
        return
    fact = message.text.replace("/remember", "").strip()
    if not fact:
        await message.answer("Usage: /remember <fact>")
        return
    r.sadd(f"user:{message.from_user.id}:facts", fact)
    await message.answer("🧠 Remembered!")

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

@dp.message(Command("todo"))
async def cmd_todo(message: Message):
    try:
        with open("TODO.md", "r") as f:
            content = f.read()[:4000]
        await message.answer(f"📋 *Current TODO list:*\n{content}", parse_mode="Markdown")
    except:
        await message.answer("TODO.md not found. Ask admin to create it.")

@dp.message(Command("task_add"))
async def cmd_task_add(message: Message):
    task = message.text.replace("/task_add", "").strip()
    if not task:
        await message.answer("Usage: /task_add <description>")
        return
    try:
        with open("TODO.md", "a") as f:
            f.write(f"\n- [ ] {task}")
        await message.answer("Task added to TODO.md. Admin will sync to GitHub.")
    except:
        await message.answer("Could not write to TODO.md.")

@dp.message(Command("task_done"))
async def cmd_task_done(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /task_done <line_number>")
        return
    try:
        line_num = int(parts[1])
        with open("TODO.md", "r") as f:
            lines = f.readlines()
        if line_num < 1 or line_num > len(lines):
            await message.answer("Line number out of range.")
            return
        if not lines[line_num-1].strip().startswith("- [ ]"):
            await message.answer("That line is not an open task.")
            return
        lines[line_num-1] = lines[line_num-1].replace("- [ ]", "- [x]")
        with open("TODO.md", "w") as f:
            f.writelines(lines)
        await message.answer(f"Task on line {line_num} marked as done.")
    except:
        await message.answer("Invalid line number.")

async def main():
    log.info("🚀 Starting Bot Polling...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
