from aiogram import Router, types
from aiogram.filters import Command
import json, os
from datetime import datetime

router = Router()
DATA_FILE = "xp_data.json"

def load_xp():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@router.message(Command("leaderboard"))
print("Loading leaderboard handler"); async def leaderboard(message: types.Message):
    data = load_xp()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
    text = "?? **Top 10 XP**\n\n"
    for i, (uid, info) in enumerate(sorted_users, 1):
        text += f"{i}. ID {uid}  {info.get('xp', 0)} XP\n"
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("myxp"))
async def myxp(message: types.Message):
    uid = str(message.from_user.id)
    data = load_xp()
    xp = data.get(uid, {}).get("xp", 0)
    await message.answer(f"? Your XP: {xp}")

