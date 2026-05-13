from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

router = Router()

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🩺 Status", callback_data="run_doctor"),
        types.InlineKeyboardButton(text="📋 TODO", callback_data="run_todo"),
        types.InlineKeyboardButton(text="🧠 Memory", callback_data="run_memory")
    )
    builder.row(
        types.InlineKeyboardButton(text="💰 IDO", callback_data="run_ido"),
        types.InlineKeyboardButton(text="⚠️ Risks", callback_data="run_risks"),
        types.InlineKeyboardButton(text="📅 Vesting", callback_data="run_vesting")
    )
    builder.row(
        types.InlineKeyboardButton(text="🪙 OSIF", callback_data="run_osif"),
        types.InlineKeyboardButton(text="💡 Help", callback_data="run_help")
    )
    return builder.as_markup()

@router.message(Command("start", "menu"))
async def cmd_start(message: types.Message):
    text = (
        "🚀 *SLH MISSION CONTROL v8*\n"
        "──────────────────\n"
        "Owner: `OSIF`\n"
        "Status: `Connected`\n\n"
        "Use the buttons below or type commands:\n"
        "`/ido`, `/invest`, `/risks`, `/vesting`,\n"
        "`/remember`, `/facts`, `/journal`, `/myday`,\n"
        "`/startwork`, `/mytime`, `/id`, `/status`, `/todo`, `/log`"
    )
    await message.answer(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# Callback handlers
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

@router.callback_query(F.data == "run_memory")
async def call_memory(callback: types.CallbackQuery):
    await callback.message.answer("🧠 *Memory commands*\n`/remember <fact>`  store\n`/facts`  show\n`/forget <fact>`  remove\n`/journal`  work log\n`/myday`  daily summary", parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "run_ido")
async def call_ido(callback: types.CallbackQuery):
    await callback.message.answer(
        "🪙 *SLH IDO Summary*\n"
        "• Token: SLH (BSC)\n"
        "• Contract: `0xACb0A09414CEA1C879c67bB7A877E4e19480f022`\n"
        "• Price: 0.000004 BNB (~$0.05)\n"
        "• Listing: 0.000005 BNB (~$0.066)\n"
        "• Soft/Hard: 20/150 BNB\n"
        "• Vesting: 20% TGE + 20% monthly (4 months)\n"
        "• Liquidity lock: 365 days",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "run_risks")
async def call_risks(callback: types.CallbackQuery):
    await callback.message.answer(
        "⚠️ *10 Risks to know*\n"
        "1. Total loss possible\n"
        "2. Smart contract risk\n"
        "3. Regulatory (Israel/global)\n"
        "4. Volatility >50% in a week\n"
        "5. 80% locked for 4 months\n"
        "6. Soft cap not reached → refund\n"
        "7. Phishing / fake tokens\n"
        "8. Wrong network (ERC20 instead of BEP20)\n"
        "9. Dependency on third parties\n"
        "10. No guaranteed profit",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "run_vesting")
async def call_vesting(callback: types.CallbackQuery):
    await callback.message.answer(
        "📅 *Vesting schedule*\n"
        "Per 1 BNB invested → 250,000 SLH\n"
        "• TGE (day 14): 50,000 SLH (20%)\n"
        "• +30 days: 50,000 SLH (40%)\n"
        "• +60 days: 50,000 SLH (60%)\n"
        "• +90 days: 50,000 SLH (80%)\n"
        "• +120 days: 50,000 SLH (100% unlocked)",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "run_osif")
async def call_osif(callback: types.CallbackQuery):
    await callback.message.answer(
        "🪙 *OSIF Time Coin*\n"
        "Commands: `/startwork`, `/stopwork`, `/mytime`, `/osifrate`\n"
        "Earn time credits for contributions.",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "run_help")
async def call_help(callback: types.CallbackQuery):
    await callback.message.answer(
        "📜 *All commands*\n"
        "`/menu`  this menu\n"
        "`/ido`, `/invest`, `/risks`, `/vesting`, `/faq`, `/verify`\n"
        "`/remember`, `/facts`, `/forget`, `/journal`, `/myday`, `/summary`\n"
        "`/startwork`, `/stopwork`, `/mytime`, `/osifrate`\n"
        "`/id`, `/status`, `/health`, `/todo`, `/log`, `/doctor`\n"
        "`/containers`, `/ps`, `/logs`, `/restart`, `/deploy` (admin)",
        parse_mode="Markdown"
    )
    await callback.answer()
