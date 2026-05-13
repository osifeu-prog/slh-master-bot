from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

XP_PER_LOG = 5
XP_PER_TASK = 10
XP_PER_WORK_MIN = 1
LEVEL_UP_BASE = 100

def get_level(xp):
    level = 1
    required = LEVEL_UP_BASE
    while xp >= required:
        xp -= required
        level += 1
        required = int(required * 1.2)
    return level, xp, required

@router.message(Command("mystats"))
async def cmd_mystats(message: types.Message):
    from slh_master_bot import r
    user_id = str(message.from_user.id)
    xp = int(r.hget(f"user:{user_id}:xp", "xp") or 0)
    level, current, next_needed = get_level(xp)
    await message.answer(
        f"🏆 *Your SLH Profile*\n\n"
        f"Level: {level}\n"
        f"XP: {xp} (next: {next_needed - current})\n"
        f"Use /startwork and /log to earn more!",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message):
    from slh_master_bot import r
    text = "🏆 *XP Leaderboard*\n"
    # Simple version for now
    await message.answer(text + "Feature coming soon...", parse_mode=ParseMode.MARKDOWN)

user_work_start = {}

@router.message(Command("startwork"))
async def cmd_startwork(message: types.Message):
    user_work_start[message.from_user.id] = datetime.now()
    await message.answer("⏳ Work session started. Use /stopwork when done.")

@router.message(Command("stopwork"))
async def cmd_stopwork(message: types.Message):
    from slh_master_bot import r
    start = user_work_start.pop(message.from_user.id, None)
    if not start:
        await message.answer("No active session.")
        return
    minutes = int((datetime.now() - start).total_seconds() / 60)
    if minutes < 1:
        await message.answer("Session too short.")
        return
    xp_earned = minutes * XP_PER_WORK_MIN
    user_id = str(message.from_user.id)
    r.hincrby(f"user:{user_id}:xp", "xp", xp_earned)
    await message.answer(f"✅ +{xp_earned} XP for {minutes} minutes of work!")
