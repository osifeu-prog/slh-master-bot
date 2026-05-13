from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("ps"))
async def ps_legacy(message: types.Message):
    await message.answer("Use /status for container list.")

@router.message(Command("proj"))
async def proj_legacy(message: types.Message):
    await message.answer("Use /proj (alias for /containers).")
