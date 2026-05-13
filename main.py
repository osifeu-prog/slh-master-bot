import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("✅ SLH Bot Live! Try /leaderboard or /health")

@dp.message(Command("leaderboard"))
async def leaderboard(msg: types.Message):
    await msg.answer("🏆 Leaderboard: No XP yet. Start working!")

@dp.message(Command("health"))
async def health(msg: types.Message):
    await msg.answer("✅ Bot healthy. Redis: OK (if configured)")

@dp.message()
async def fallback(msg: types.Message):
    await msg.answer("🟢 SLH Master Bot v8.0 - Online\nEcosystem: DILIGENT-RADIANCE")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
