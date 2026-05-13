from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

router = Router()

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🩺 Status Check", callback_data="run_doctor"),
        types.InlineKeyboardButton(text="📝 View TODO", callback_data="run_todo")
    )
    builder.row(
        types.InlineKeyboardButton(text="🎓 SLH Academia", url="https://slhisrael.com"),
        types.InlineKeyboardButton(text="📊 SSoT Snapshot", callback_data="run_snapshot")
    )
    builder.row(
        types.InlineKeyboardButton(text="💡 Help & Commands", callback_data="run_help")
    )
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"🚀 **SLH MISSION CONTROL v8**\n"
        f"──────────────────\n"
        f"Owner: `OSIF`\n"
        f"Status: `Connected`\n\n"
        f"ברוך הבא למערכת הניהול המרכזית. "
        f"מכאן ניתן לנהל את המשימות, לבדוק את בריאות השרתים ולתעד פעולות ב-SSoT."
    )
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

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

@router.callback_query(F.data == "run_snapshot")
async def call_snapshot(callback: types.CallbackQuery):
    await callback.message.answer("📸 Snapshot triggered (via Telegram). Check your PowerShell console for details.")
    # Note: actual snapshot requires local script  here just a placeholder.
    await callback.answer()

@router.callback_query(F.data == "run_help")
async def call_help(callback: types.CallbackQuery):
    help_text = (
        "📜 **Command List:**\n"
        "`/log <text>` - תיעוד פעולה ל-SSoT\n"
        "`/doctor` - בדיקת מערכות\n"
        "`/todo` - רשימת משימות\n"
        "`/start` - פתיחת תפריט זה"
    )
    await callback.message.answer(help_text, parse_mode="Markdown")
    await callback.answer()
