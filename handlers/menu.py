from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.enums import ParseMode

router = Router()

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🛒 Premium (50 Stars)", callback_data="buy_premium"),
        types.InlineKeyboardButton(text="📊 My Stats", callback_data="run_mystats")
    )
    builder.row(
        types.InlineKeyboardButton(text="💰 IDO", callback_data="run_ido"),
        types.InlineKeyboardButton(text="⚠️ Risks", callback_data="run_risks")
    )
    builder.row(
        types.InlineKeyboardButton(text="📅 Vesting", callback_data="run_vesting"),
        types.InlineKeyboardButton(text="🩺 Status", callback_data="run_doctor")
    )
    builder.row(
        types.InlineKeyboardButton(text="📋 TODO", callback_data="run_todo"),
        types.InlineKeyboardButton(text="💡 Help", callback_data="run_help")
    )
    return builder.as_markup()

@router.message(Command("start", "menu"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 <b>SLH Master Bot v8.0</b>\n\n"
        "ברוך הבא! בחר קטגוריה:",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "buy_premium")
async def buy_premium(callback: types.CallbackQuery):
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
