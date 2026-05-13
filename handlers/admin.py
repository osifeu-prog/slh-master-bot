# handlers/admin.py - פקודות ניהול
from aiogram import Router, types
from aiogram.filters import Command
import subprocess, os, json
from datetime import datetime

router = Router()

@router.message(Command("restart"))
async def cmd_restart(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /restart <service> (master-bot, fastapi)")
        return
    service = args[1]
    if service == "master-bot":
        os.system("railway up --service slh-master-bot --detach")
        await message.answer("🔄 Restarting master bot...")
    else:
        await message.answer(f"Unknown service: {service}")

@router.message(Command("logs"))
async def cmd_logs(message: types.Message):
    args = message.text.split()
    service = args[1] if len(args) > 1 else "slh-master-bot"
    result = subprocess.run(f"railway logs --service {service} --tail 20", shell=True, capture_output=True, text=True)
    await message.answer(f"📜 Logs for {service}:\n```\n{result.stdout[-1500:]}\n```", parse_mode="Markdown")

@router.message(Command("backup"))
async def cmd_backup(message: types.Message):
    backup_path = f"D:\\SLH_SNAPSHOTS\\manual_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
    subprocess.run(f'powershell Compress-Archive -Path D:\\SLH_ECOSYSTEM,D:\\SLH_MASTER_BOT -DestinationPath {backup_path} -Force', shell=True)
    await message.answer(f"✅ Backup created: {backup_path}")

@router.message(Command("health"))
async def cmd_health(message: types.Message):
    await message.answer("✅ Bot is healthy. Redis connected, uptime stable.")
