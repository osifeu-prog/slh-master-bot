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
    level, xp_current, xp_next = get_level(xp)
    tasks_done = int(r.hget(f"user:{user_id}:stats", "tasks_done") or 0)
    work_min = int(r.hget(f"user:{user_id}:stats", "work_min") or 0)
    logs_count = int(r.hget(f"user:{user_id}:stats", "logs_count") or 0)
    await message.answer(
        f"👤 *Your SLH Profile*\n\n"
        f"🎚️ Level: {level}\n"
        f"⭐ XP: {xp} (next level: {xp_next - xp_current})\n"
        f"✅ Tasks done: {tasks_done}\n"
        f"📝 Logs: {logs_count}\n"
        f"⏱️ Work time: {work_min // 60}h {work_min % 60}m",
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message):
    from slh_master_bot import r
    all_users = []
    keys = r.keys("user:*:xp")
    for k in keys:
        uid = k.decode().split(":")[1]
        xp_val = int(r.hget(k, "xp") or 0)
        all_users.append((f"User_{uid[:4]}", xp_val))
    all_users.sort(key=lambda x: x[1], reverse=True)
    text = "🏆 *XP Leaderboard*\n"
    for i, (name, xp_val) in enumerate(all_users[:10], 1):
        text += f"{i}. {name} – {xp_val} XP\n"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

user_work_start = {}

@router.message(Command("startwork"))
async def cmd_startwork(message: types.Message):
    user_work_start[message.from_user.id] = datetime.now()
    await message.answer("⏱️ Work session started. Use /stopwork when done.")

@router.message(Command("stopwork"))
async def cmd_stopwork(message: types.Message):
    from slh_master_bot import r
    start = user_work_start.pop(message.from_user.id, None)
    if not start:
        await message.answer("No active work session. Use /startwork first.")
        return
    minutes = int((datetime.now() - start).total_seconds() / 60)
    if minutes < 1:
        await message.answer("Work session too short (less than 1 minute). No XP.")
        return
    xp_earned = minutes * XP_PER_WORK_MIN
    user_id = str(message.from_user.id)
    r.hincrby(f"user:{user_id}:xp", "xp", xp_earned)
    r.hincrby(f"user:{user_id}:stats", "work_min", minutes)
    await message.answer(f"✅ Work session ended. +{xp_earned} XP for {minutes} minutes.")
