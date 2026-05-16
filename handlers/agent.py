import json, os, logging, httpx
from pathlib import Path
from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime

router = Router()
log = logging.getLogger(name)
BASE_DIR = Path(file).parent.parent
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@router.message(Command("log"))
async def cmd_log(message: types.Message):
    text = message.text.replace("/log", "").strip()
    if not text:
        await message.answer("Usage: /log your message", parse_mode=None)
        return
    try:
        log_file = BASE_DIR / "session_log.json"
        data = json.loads(log_file.read_text(encoding="utf-8")) if log_file.exists() else [{"agent": "telegram", "actions": []}]
        data[-1]["actions"].append({"time": datetime.now().isoformat(), "action": text})
        log_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        await message.answer("Logged: " + text[:200], parse_mode=None)
    except Exception as e:
        await message.answer("Log error: " + str(e)[:100], parse_mode=None)

@router.message(Command("doctor"))
async def cmd_doctor(message: types.Message):
    url = os.getenv("RAILWAY_FASTAPI_URL", "https://slh-fastapi-production.up.railway.app")
    lines = ["System Status", ""]
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(url + "/health")
            lines.append("FastAPI: OK" if r.status_code == 200 else "FastAPI: ERROR")
    except:
        lines.append("FastAPI: unreachable")
    lines.append("Token: set" if os.getenv("MASTER_BOT_TOKEN") else "Token: MISSING")
    lines.append("Groq: set" if GROQ_API_KEY else "Groq: not configured")
    await message.answer("\n".join(lines), parse_mode=None)

@router.message(Command("todo"))
async def cmd_todo(message: types.Message):
    todo_file = BASE_DIR / "TODO.md"
    content = todo_file.read_text(encoding="utf-8")[:2000] if todo_file.exists() else "No TODO.md found."
    await message.answer(content, parse_mode=None)

async def ask_groq(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "AI not configured."
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": "Bearer " + GROQ_API_KEY},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            )
            return resp.json()["choices"][0]["message"]["content"] if resp.status_code == 200 else "AI busy."
    except:
        return "AI connection error."

@router.message()
async def ai_chat(message: types.Message):
    if not message.text or message.text.startswith("/") or len(message.text.strip()) < 4:
        return
    thinking = await message.answer("Thinking...", parse_mode=None)
    answer = await ask_groq(message.text)
    await thinking.edit_text(answer[:3500], parse_mode=None)
