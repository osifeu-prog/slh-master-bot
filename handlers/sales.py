from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("offers"))
async def offers(message: types.Message):
    await message.answer("🎁 Special offers: None at the moment.")
