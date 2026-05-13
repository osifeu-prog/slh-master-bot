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
        f"• Last action: {last_action}",
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

import os, httpx
from aiogram.types import Message

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

async def ask_groq(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not set. Please add it to Railway environment."
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={"model": GROQ_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            else:
                return f"❌ Groq error: {resp.status_code}"
        except Exception as e:
            return f"❌ AI error: {str(e)[:100]}"

@router.message()
async def ai_chat(message: types.Message):
    # Don't respond to commands
    if message.text.startswith("/"):
        return
    # Don't respond if already handled elsewhere
    if message.text.lower().strip() in ["hi", "hello", "hey", "שלום"]:
        await message.answer("Hello! How can I help you with SLH today?")
        return
    # Long messages or general chat → AI
    if len(message.text) > 10 or any(word in message.text.lower() for word in ["what", "how", "why", "tell", "explain"]):
        thinking = await message.answer("🤔 Thinking...")
        answer = await ask_groq(message.text)
        await thinking.edit_text(answer)