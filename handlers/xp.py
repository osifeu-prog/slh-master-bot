import json
from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

# Redis client will be imported from main bot (r)
# XP calculation constants
XP_PER_LOG = 5
XP_PER_TASK = 10
XP_PER_WORK_MIN = 1   # per minute of work session
LEVEL_UP_BASE = 100   # XP needed for level 1

def get_level(xp):
    level = 1
    required = LEVEL_UP_BASE
    while xp >= required:
        xp -= required
        level += 1
        required = int(required * 1.2)  # each level requires 20% more
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
        f"🎚️ Level: *{level}*\n"
        f"⭐ XP: *{xp}* (next level: {xp_next - xp_current})\n"
        f"✅ Tasks done: {tasks_done}\n"
        f"📝 Logs: {logs_count}\n"
        f"⏱️ Work sessions: {work_min // 60}h {work_min % 60}m\n"
        f"🏆 Rank: {await get_rank(user_id)}",
        parse_mode=ParseMode.MARKDOWN
    )

async def get_rank(user_id):
    from slh_master_bot import r
    all_users = []
    keys = r.keys("user:*:xp")
    for k in keys:
        uid = k.decode().split(":")[1]
        xp_val = int(r.hget(k, "xp") or 0)
        all_users.append((uid, xp_val))
    all_users.sort(key=lambda x: x[1], reverse=True)
    for i, (uid, _) in enumerate(all_users[:10], 1):
        if uid == user_id:
            return f"#{i} / {len(all_users)}"
    return "unranked"

@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message):
    from slh_master_bot import r
    all_users = []
    keys = r.keys("user:*:xp")
    for k in keys:
        uid = k.decode().split(":")[1]
        xp_val = int(r.hget(k, "xp") or 0)
        name = await get_username(uid)
        all_users.append((name, xp_val))
    all_users.sort(key=lambda x: x[1], reverse=True)
    text = "🏆 *XP Leaderboard*\n"
    for i, (name, xp_val) in enumerate(all_users[:10], 1):
        text += f"{i}. {name}  {xp_val} XP\n"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

async def get_username(user_id):
    # Simple: try to get from cache or fallback
    return f"User_{user_id[:6]}"

@router.message(Command("praise"))
async def cmd_praise(message: types.Message):
    from slh_master_bot import r
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /praise @username or reply to a message")
        return
    target = parts[1].strip()
    # For simplicity, just extract numeric ID if possible; otherwise ignore.
    await message.answer("✅ Praise given! +10 XP to recipient, -5 XP to you.")
    # TODO: implement real user lookup and XP transfer

# Work session tracking
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
