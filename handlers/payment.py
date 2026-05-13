from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()
ADMIN_ID = 8789977826

@router.message(Command("buy", "premium"))
async def cmd_buy(message: types.Message):
    await message.answer_invoice(
        title="SLH Premium - 1 month",
        description="Double XP + live alerts + portfolio + priority",
        payload="premium_1month",
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium Monthly", amount=50)],
        start_parameter="slh_premium",
        provider_token=""
    )

@router.pre_checkout_query()
async def pre_checkout_query(query: types.PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    from slh_master_bot import r, bot
    user_id = str(message.from_user.id)
    r.set(f"user:{user_id}:premium", "true", ex=30*24*3600)
    r.hset(f"user:{user_id}:stats", "premium_since", str(datetime.now()))
    await message.answer("✅ **Premium activated!** Enjoy double XP, alerts and portfolio.", parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(
        ADMIN_ID,
        f"💰 *New Premium Purchase*\nUser: {message.from_user.full_name} (ID: {message.from_user.id})\nAmount: 50 Stars",
        parse_mode=ParseMode.MARKDOWN
    )
