from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

@router.message(Command("start", "menu"))
async def aggressive_start(message: types.Message):
    await message.answer(
        "🚀 <b>ברוך הבא ל-SLH Ecosystem</b>\n\n"
        "כדי לקבל גישה מלאה + XP + התראות + ייעוץ:\n"
        "שלח <b>/buy</b> עכשיו (50 Stars לחודש)\n\n"
        "רוצה ייעוץ אישי? שלח <b>/consulting</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text="🛒 קנה Premium עכשיו", callback_data="buy_premium")
        ]])
    )

@router.callback_query(F.data == "buy_premium")
async def callback_buy(callback: types.CallbackQuery):
    await callback.message.answer_invoice(
        title="SLH Premium - 1 חודש",
        description="גישה מלאה + XP ×2 + התראות + עדיפות",
        payload="premium_1month",
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium Monthly", amount=50)],
        start_parameter="slh_premium",
        provider_token=""
    )
    await callback.answer()
