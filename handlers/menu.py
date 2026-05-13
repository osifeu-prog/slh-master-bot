from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.enums import ParseMode

router = Router()

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛒 קנה Premium (50 Stars)", callback_data="buy_premium"))
    builder.row(types.InlineKeyboardButton(text="📊 My Stats", callback_data="run_mystats"))
    builder.row(types.InlineKeyboardButton(text="🩺 Status", callback_data="run_doctor"))
    builder.row(types.InlineKeyboardButton(text="💡 Help", callback_data="run_help"))
    return builder.as_markup()

@router.message(Command("start", "menu"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 <b>ברוך הבא ל-SLH Master Control</b>\n\n"
        "✅ חינם: XP, TODO, זיכרון\n"
        "🔥 <b>Premium</b>  50 Stars לחודש:\n"
        "• XP ×2\n"
        "• התראות מחיר חיות\n"
        "• ניהול תיק\n"
        "• עדיפות + קבוצת ייעוץ\n\n"
        "<b>הצעה מוגבלת:</b> 3 הראשונים מקבלים 50% הנחה!",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "buy_premium")
async def buy_callback(callback: types.CallbackQuery):
    await callback.message.answer_invoice(
        title="SLH Premium - 1 חודש",
        description="XP ×2 + התראות + ניהול תיק + עדיפות",
        payload="premium_1month",
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium Monthly", amount=50)],
        start_parameter="slh_premium",
        provider_token=""
    )
    await callback.answer()
