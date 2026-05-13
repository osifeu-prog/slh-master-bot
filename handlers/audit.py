import os
import requests
import redis
from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()
ADMIN_ID = 8789977826

def run_audit():
    status = []
    # Redis
    try:
        r = redis.from_url(os.getenv("REDIS_URL"))
        r.ping()
        status.append("✅ Redis: Connected")
    except Exception as e:
        status.append(f"❌ Redis: {str(e)[:50]}")
    # FastAPI (if exists)
    try:
        res = requests.get("https://slh-fastapi-production.up.railway.app/health", timeout=5)
        status.append(f"✅ FastAPI: {res.status_code}")
    except:
        status.append("❌ FastAPI: Unreachable")
    return "\n".join(status)

@router.message(Command("audit"))
async def cmd_audit(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Unauthorized.")
        return
    report = run_audit()
    await message.answer(
        f"📋 *SLH System Audit*  {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{report}",
        parse_mode=ParseMode.MARKDOWN
    )
