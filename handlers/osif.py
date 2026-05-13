# handlers/osif.py - פקודות זמן / מטבע
from aiogram import Router, types
from aiogram.filters import Command
import json, os
from datetime import datetime

router = Router()
DATA_FILE = "osif_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@router.message(Command("startwork"))
async def startwork(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    data[user_id] = {"start": datetime.now().isoformat(), "total_seconds": 0}
    save_data(data)
    await message.answer("🕒 Work started. Use /stopwork when done.")

@router.message(Command("stopwork"))
async def stopwork(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id in data and "start" in data[user_id]:
        start = datetime.fromisoformat(data[user_id]["start"])
        elapsed = (datetime.now() - start).total_seconds()
        data[user_id]["total_seconds"] = data[user_id].get("total_seconds", 0) + elapsed
        data[user_id]["start"] = None
        save_data(data)
        await message.answer(f"✅ Work stopped. Total seconds: {int(elapsed)}")
    else:
        await message.answer("No active work session.")

@router.message(Command("mytime"))
async def mytime(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    total = data.get(user_id, {}).get("total_seconds", 0)
    hours = total // 3600
    minutes = (total % 3600) // 60
    await message.answer(f"⏱️ Total OSIF time: {hours}h {minutes}m")

@router.message(Command("osifrate"))
async def osifrate(message: types.Message):
    await message.answer("💰 Current OSIF rate: 0.05 USD per hour (example)")
