from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("menu"))
async def menu_handler(message: Message):
    text = """🔥 *SLH Master Bot v3.14*  Main Menu

📦 *Containers*  /containers
🧠 *Memory*  /remember, /facts
👥 *Users*  /id, /listusers
🪙 *OSIF*  /startwork, /mytime
🛠️ *System*  /status, /logs
🛡️ *Investment*  /invest
📊 *IDO*  /ido
📋 *Tasks*  /todo
"""
    await message.answer(text, parse_mode="Markdown")
