from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

@router.message(Command("buy", "premium"))
async def cmd_buy(message: types.Message):
    await message.answer_invoice(
        title="SLH Premium - 1 חודש",
        description="XP ×2 + התראות מחיר + פקודות פרימיום",
        payload="premium_1month",
        currency="XTR",
        prices=[types.LabeledPrice(label="SLH Premium Monthly", amount=50)],
        start_parameter="slh_premium",
        provider_token=""
    )

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    from slh_master_bot import r
    user_id = str(message.from_user.id)
    r.set(f"user:{user_id}:premium", "true", ex=30*24*3600)
    r.hset(f"user:{user_id}:stats", "premium_since", str(datetime.now()))
    await message.answer("✅ אתה עכשיו **Premium**!\nXP ×2 + פיצ'רים\n/mystats", parse_mode=ParseMode.MARKDOWN)
