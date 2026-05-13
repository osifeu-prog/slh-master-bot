from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("balance"))
async def balance(message: types.Message):
    await message.answer("💰 Your balance: 0 SLH (demo). Use /deposit to add funds.")

@router.message(Command("deposit"))
async def deposit(message: types.Message):
    await message.answer("💳 Demo deposit. In production, integrate CryptoPay.")
