from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

@router.message(Command("ido"))
async def cmd_ido(message: types.Message):
    await message.answer("🪙 SLH IDO Summary - see full details in /ido", parse_mode=ParseMode.MARKDOWN)

@router.message(Command("risks"))
async def cmd_risks(message: types.Message):
    await message.answer("⚠️ 10 Risks - see /risks", parse_mode=ParseMode.MARKDOWN)

@router.message(Command("vesting"))
async def cmd_vesting(message: types.Message):
    await message.answer("📅 Vesting Schedule - see /vesting", parse_mode=ParseMode.MARKDOWN)

@router.message(Command("invest"))
async def cmd_invest(message: types.Message):
    await message.answer("🛡️ Investment Questionnaire started. Answer the questions.", parse_mode=ParseMode.MARKDOWN)

@router.message(Command("journal", "myday"))
async def cmd_journal(message: types.Message):
    await message.answer("📓 Journal & MyDay - use /log to add entries", parse_mode=ParseMode.MARKDOWN)

@router.message(Command("price"))
async def cmd_price(message: types.Message):
    await message.answer("📈 SLH Price coming soon (live from CoinGecko)", parse_mode=ParseMode.MARKDOWN)

@router.message(Command("faq", "verify", "osifrate"))
async def cmd_faq(message: types.Message):
    await message.answer("ℹ️ Use /help for full list of commands", parse_mode=ParseMode.MARKDOWN)
