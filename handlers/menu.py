from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.enums import ParseMode

router = Router()

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🩺 Status", callback_data="run_doctor"),
        types.InlineKeyboardButton(text="📋 TODO", callback_data="run_todo")
    )
    builder.row(
        types.InlineKeyboardButton(text="💰 IDO", callback_data="run_ido"),
        types.InlineKeyboardButton(text="⚠️ Risks", callback_data="run_risks")
    )
    builder.row(
        types.InlineKeyboardButton(text="👤 My Stats", callback_data="run_mystats"),
        types.InlineKeyboardButton(text="🏆 Leaderboard", callback_data="run_leaderboard")
    )
    builder.row(
        types.InlineKeyboardButton(text="💡 Help", callback_data="run_help")
    )
    return builder.as_markup()

@router.message(Command("start", "menu"))
async def cmd_start(message: types.Message):
    text = "🚀 *SLH MISSION CONTROL v8.0*\nOwner: `OSIF`\nStatus: `Connected`"
    await message.answer(text, reply_markup=main_menu_keyboard(), parse_mode=ParseMode.MARKDOWN)

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

@router.callback_query(F.data == "run_mystats")
async def call_mystats(callback: types.CallbackQuery):
    from handlers.xp import cmd_mystats
    await cmd_mystats(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_leaderboard")
async def call_leaderboard(callback: types.CallbackQuery):
    from handlers.xp import cmd_leaderboard
    await cmd_leaderboard(callback.message)
    await callback.answer()

@router.callback_query(F.data == "run_ido")
async def call_ido(callback: types.CallbackQuery):
    await callback.message.answer("🪙 SLH IDO info...", parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@router.callback_query(F.data == "run_risks")
async def call_risks(callback: types.CallbackQuery):
    await callback.message.answer("⚠️ Risks list...", parse_mode=ParseMode.MARKDOWN)
    await callback.answer()

@router.callback_query(F.data == "run_help")
async def call_help(callback: types.CallbackQuery):
    await callback.message.answer("📜 Use /menu, /doctor, /mystats etc.", parse_mode=ParseMode.MARKDOWN)
    await callback.answer()
