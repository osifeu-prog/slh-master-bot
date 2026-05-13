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
        "🚀 <b>SLH Master Bot v8.0</b>\n\nWelcome! Choose a category:",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "buy_premium")
async def buy_premium(callback: types.CallbackQuery):
    await callback.message.answer_invoice(
        title="SLH Premium - 1 month",
        description="Double XP + live alerts + portfolio + priority",
        payload="premium_1month",
        currency="XTR",
        prices=[types.LabeledPrice(label="Premium Monthly", amount=50)],
        start_parameter="slh_premium",
        provider_token=""
    )
    await callback.answer()

@router.callback_query(F.data == "run_ido")
async def call_ido(callback: types.CallbackQuery):
    from handlers.legacy import cmd_ido
    await cmd_ido(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_risks")
async def call_risks(callback: types.CallbackQuery):
    from handlers.legacy import cmd_risks
    await cmd_risks(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_vesting")
async def call_vesting(callback: types.CallbackQuery):
    from handlers.legacy import cmd_vesting
    await cmd_vesting(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_mystats")
async def call_mystats(callback: types.CallbackQuery):
    from handlers.xp import cmd_mystats
    await cmd_mystats(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_doctor")
async def call_doctor(callback: types.CallbackQuery):
    from handlers.agent import cmd_doctor
    await cmd_doctor(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_todo")
async def call_todo(callback: types.CallbackQuery):
    from handlers.agent import cmd_todo
    await cmd_todo(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_help")
async def call_help(callback: types.CallbackQuery):
    await callback.message.answer(
        "📜 *Commands*\n"
        "/ido, /risks, /vesting, /invest, /faq, /verify, /journal, /myday, /osifrate, /price\n"
        "/start, /menu, /buy, /log, /doctor, /todo, /mystats, /leaderboard, /audit",
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()
