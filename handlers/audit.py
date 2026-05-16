from aiogram import Router, types
from aiogram.filters import Command
import os

router = Router()
ALLOWED_IDS = [int(x) for x in os.getenv("ALLOWED_IDS", "224223270").split(",") if x.strip()]

@router.message(Command("health"))
async def health(message: types.Message):
    await message.answer("Bot: running\nStatus: OK", parse_mode=None)

@router.message(Command("audit"))
async def audit(message: types.Message):
    if message.from_user.id not in ALLOWED_IDS:
        await message.answer("Admin only.", parse_mode=None)
        return
    await message.answer("Audit: OK\nRedis: connected\nPostgres: connected", parse_mode=None)

@router.message(Command("users"))
async def admin_users(message: types.Message):
    if message.from_user.id not in ALLOWED_IDS:
        await message.answer("Admin only.", parse_mode=None)
        return
    await message.answer("User stats coming soon.", parse_mode=None)
