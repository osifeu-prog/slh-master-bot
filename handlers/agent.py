import json
from pathlib import Path
from aiogram import Router, types
from aiogram.filters import Command
import logging
import os
import httpx
from datetime import datetime

router = Router()
log = logging.getLogger(__name__)
BASE_DIR = Path(__file__).parent.parent

# ====================== /log ======================
@router.message(Command("log"))
async def cmd_log(message: types.Message):
    text = message.text.replace("/log", "").strip()
    if not text:
        await message.answer("📝 Usage: /log <message>", parse_mode=None)
        return
    
    try:
        log_file = BASE_DIR / "session_log.json"
        data = json.loads(log_file.read_text(encoding="utf-8")) if log_file.exists() else []
        if not data or not isinstance(data, list):
            data = [{"agent": "telegram", "actions": []}]
        
        data[-1]["actions"].append({
            "time": datetime.now().isoformat(),
            "action": text
        })
        
        log_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        await message.answer(f"✅ Logged: {text[:400]}...", parse_mode=None)
    except Exception as e:
        await message.answer(f"⚠️ Log error: {str(e)[:100]}", parse_mode=None)

# ====================== AI Chat ======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def ask_groq(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "AI is temporarily unavailable."
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            )
            return resp.json()["choices"][0]["message"]["content"] if resp.status_code == 200 else "AI is busy right now."
    except:
        return "AI connection error."

@router.message()
async def ai_chat(message: types.Message):
    if message.text.startswith("/"):
        return
    if len(message.text.strip()) < 4:
        return
    thinking = await message.answer("🤔 Thinking...")
    answer = await ask_groq(message.text)
    await thinking.edit_text(answer[:3500], parse_mode=None)
