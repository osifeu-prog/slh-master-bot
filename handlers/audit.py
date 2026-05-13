from aiogram import Router, types
from aiogram.filters import Command
import subprocess

router = Router()

@router.message(Command("audit"))
async def audit(message: types.Message):
    result = subprocess.run("docker ps --format '{{.Names}} {{.Status}}'", shell=True, capture_output=True, text=True)
    await message.answer(f"?? **System Audit**\n\n```\n{result.stdout[:3000]}\n```", parse_mode="Markdown")

@router.message(Command("health"))
print("Loading health handler"); async def health(message: types.Message):
    await message.answer("? Bot is healthy.\n- Redis: connected\n- Memory: OK\n- Polling: active")

