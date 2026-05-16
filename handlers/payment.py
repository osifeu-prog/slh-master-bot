from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("buy"))
async def buy(message: types.Message):
    await message.answer_invoice(
        title="SLH Premium - 1 Month",
        description="Double XP + live alerts + priority support",
        payload="premium_1month",
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium", amount=50)],
        start_parameter="slh_premium",
        provider_token=""
    )

@router.message(Command("balance"))
async def balance(message: types.Message):
    await message.answer("Balance: 0 SLH\nUse /buy to get Premium (50 Stars).", parse_mode=None)
