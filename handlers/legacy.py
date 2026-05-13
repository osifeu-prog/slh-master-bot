from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

@router.message(Command("ido"))
async def cmd_ido(message: types.Message):
    await message.answer(
        "🪙 *SLH IDO Summary*\n"
        "• Token: SLH (BSC)\n"
        "• Contract: `0xACb0A09414CEA1C879c67bB7A877E4e19480f022`\n"
        "• Price: 0.000004 BNB (~$0.05)\n"
        "• Listing: 0.000005 BNB (~$0.066)\n"
        "• Soft/Hard: 20/150 BNB\n"
        "• Vesting: 20% TGE + 20% monthly (4 months)\n"
        "• Liquidity lock: 365 days",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("risks"))
async def cmd_risks(message: types.Message):
    await message.answer(
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
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("vesting"))
async def cmd_vesting(message: types.Message):
    await message.answer(
        "📅 *Vesting schedule*\n"
        "Per 1 BNB invested → 250,000 SLH\n"
        "• TGE (day 14): 50,000 SLH (20%)\n"
        "• +30 days: 50,000 SLH (40%)\n"
        "• +60 days: 50,000 SLH (60%)\n"
        "• +90 days: 50,000 SLH (80%)\n"
        "• +120 days: 50,000 SLH (100% unlocked)",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("invest"))
async def cmd_invest(message: types.Message):
    await message.answer(
        "🛡️ *Investment Questionnaire*\n\n"
        "1. How much do you want to invest? (amount)\n"
        "2. What % of your portfolio is this?\n"
        "3. How long do you plan to invest?\n"
        "4. Expected return from this index?\n"
        "5. What similar offers have you seen?\n"
        "6. What attracted you to them?\n\n"
        "🎯 Analysis: I'll review your answers and suggest a better alternative.",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("faq"))
async def cmd_faq(message: types.Message):
    await message.answer(
        "❓ *Frequently Asked Questions*\n"
        "• What is SLH?  SLH Ecosystem token.\n"
        "• Which wallet?  MetaMask (BSC).\n"
        "• How to buy BNB?  Bit2C / Binance.\n"
        "• Tax in Israel?  25% capital gains tax on sale.\n"
        "• KYC required?  No at protocol level. Exchanges may require.\n"
        "• If Soft Cap not reached  automatic refund.\n"
        "• How to sell SLH?  PancakeSwap after TGE.\n"
        "• How to see my SLH?  Import token in MetaMask.",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("verify"))
async def cmd_verify(message: types.Message):
    await message.answer(
        "🔍 *Self‑audit steps*\n"
        "1. Check token address on BscScan\n"
        "2. Check holders  no single wallet >50%\n"
        "3. Check Treasury Safe  ≥2/3 signers\n"
        "4. Check Audit  SolidProof (to be released)\n"
        "5. Check LP Lock  PinkLock, duration ≥365 days\n"
        "6. Check MIDAO Certificate  status Active\n"
        "7. Check PinkSale Profile  KYC badge\n"
        "8. Check contract code  must be Verified",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("journal"))
async def cmd_journal(message: types.Message):
    await message.answer("📓 Work journal. Use /myday to summarize.")

@router.message(Command("myday"))
async def cmd_myday(message: types.Message):
    await message.answer(
        "📅 *Today's summary*\n"
        "• No entries yet.\n"
        "Use /log to record actions and /remember to store facts.",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("osifrate"))
async def cmd_osifrate(message: types.Message):
    await message.answer("🪙 1 OSIF = 1 minute of focused work. Earn with /startwork.")

@router.message(Command("price"))
async def cmd_price(message: types.Message):
    await message.answer("📈 *SLH Price*\nComing soon  live data from CoinGecko.", parse_mode=ParseMode.MARKDOWN)
