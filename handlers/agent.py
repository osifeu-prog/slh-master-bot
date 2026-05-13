import json
from pathlib import Path
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
BOT_ROOT = Path(__file__).parent.parent

@router.message(Command("log"))
async def cmd_log(message: Message):
    text = message.text.replace("/log", "").strip()
    if not text:
        await message.answer("📝 Usage: /log <message>")
        return
    log_file = BOT_ROOT / "session_log.json"
    try:
        if log_file.exists():
            data = json.loads(log_file.read_text(encoding="utf-8"))
        else:
            data = []
        if not data:
            data.append({"agent": "telegram", "actions": []})
        data[-1]["actions"].append({
            "time": str(__import__("datetime").datetime.now()),
            "action": f"[Telegram] {text}"
        })
        log_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        await message.answer(f"📝 Logged: {text}")
    except Exception as e:
        await message.answer(f"⚠️ Failed to write log: {e}")

@router.message(Command("doctor"))
async def cmd_doctor(message: Message):
    # Redis check via existing connection
    from slh_master_bot import r
    redis_status = "✅ Connected" if r and r.ping() else "❌ Not connected"
    
    # TODO.md status
    todo_path = BOT_ROOT / "TODO.md"
    todo_exists = todo_path.exists()
    todo_status = "✅ Exists" if todo_exists else "❌ Missing"
    todo_preview = ""
    if todo_exists:
        lines = todo_path.read_text(encoding="utf-8").splitlines()
        pending = [l for l in lines if "- [ ]" in l][:3]
        todo_preview = "\n".join(f"  • {l.split('- [ ]')[-1].strip()}" for l in pending)
    
    # Last action from session log
    log_file = BOT_ROOT / "session_log.json"
    last_action = "None"
    if log_file.exists():
        try:
            data = json.loads(log_file.read_text(encoding="utf-8"))
            if data and data[-1].get("actions"):
                last_action = data[-1]["actions"][-1].get("action", "?")
        except:
            last_action = "Error reading log"
    
    await message.answer(
        f"🩺 **SLH System Health**\n\n"
        f"• Redis: {redis_status}\n"
        f"• TODO.md: {todo_status}\n"
        f"• Pending tasks:\n{todo_preview if todo_preview else '  None'}\n"
        f"• Last action: {last_action}\n"
        f"• Bot version: v3.14\n"
        f"• Environment: DILIGENT-RADIANCE",
        parse_mode="Markdown"
    )
