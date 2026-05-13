import json
from pathlib import Path
from aiogram import Router, types
from aiogram.filters import Command

router = Router()
BASE_DIR = Path(__file__).parent.parent

@router.message(Command("log"))
async def cmd_log(message: types.Message):
    text = message.text.replace("/log", "").strip()
    if not text:
        await message.answer("📝 Usage: /log <message>")
        return
    log_file = BASE_DIR / "session_log.json"
    try:
        data = json.loads(log_file.read_text(encoding="utf-8")) if log_file.exists() else []
        if not data:
            data.append({"agent": "telegram", "actions": []})
        data[-1]["actions"].append({
            "time": str(__import__("datetime").datetime.now()),
            "action": f"[Telegram] {text}"
        })
        log_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        await message.answer(f"📝 Logged: {text}")
    except Exception as e:
        await message.answer(f"⚠️ Failed: {e}")

@router.message(Command("doctor"))
async def cmd_doctor(message: types.Message):
    from slh_master_bot import r
    redis_status = "✅ Connected" if r and r.ping() else "❌ Not connected"
    todo_path = BASE_DIR / "TODO.md"
    todo_status = "✅ Exists" if todo_path.exists() else "❌ Missing"
    todo_preview = ""
    if todo_path.exists():
        lines = todo_path.read_text(encoding="utf-8").splitlines()
        pending = [l for l in lines if "- [ ]" in l][:3]
        todo_preview = "\n".join(f"  • {l.split('- [ ]')[-1].strip()}" for l in pending)
    log_file = BASE_DIR / "session_log.json"
    last_action = "None"
    if log_file.exists():
        try:
            data = json.loads(log_file.read_text(encoding="utf-8"))
            if data and data[-1].get("actions"):
                last_action = data[-1]["actions"][-1].get("action", "?")
        except:
            last_action = "Error"
    await message.answer(
        f"🩺 *SLH System Health*\n\n"
        f"• Redis: {redis_status}\n"
        f"• TODO.md: {todo_status}\n"
        f"• Pending tasks:\n{todo_preview if todo_preview else '  None'}\n"
        f"• Last action: {last_action}\n"
        f"• Bot version: v3.14\n"
        f"• Environment: DILIGENT-RADIANCE",
        parse_mode="Markdown"
    )

@router.message(Command("todo"))
async def cmd_todo(message: types.Message):
    todo_path = BASE_DIR / "TODO.md"
    if not todo_path.exists():
        await message.answer("❌ TODO.md not found.")
        return
    pending = [l for l in todo_path.read_text(encoding="utf-8").splitlines() if "- [ ]" in l][:10]
    text = "\n".join(f"→ {l.replace('- [ ]', '').strip()}" for l in pending) if pending else "All done!"
    await message.answer(f"📋 *Pending tasks*\n{text}", parse_mode="Markdown")

@router.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("🟢 SLH Master Bot v3.14 - Online\nEcosystem: DILIGENT-RADIANCE")
