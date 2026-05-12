# -*- coding: utf-8 -*-
import datetime
from aiogram.filters import Command, CommandStart
import asyncio, os, logging, json, aiohttp, subprocess, io, glob, re, time as _time, hashlib

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.types import BufferedInputFile, TelegramObject, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
import docker

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
OWNER_ID = int(os.getenv("ADMIN_USER_ID", "224223270"))
RAILWAY_API = "https://slh-api-production.up.railway.app"
LOCAL_BRIDGE = os.getenv("LOCAL_BRIDGE_URL", "http://host.docker.internal:8765")
PROJECT_ROOT = r"D:\SLH_ECOSYSTEM"
WEBSITE_PATH = os.path.join(PROJECT_ROOT, "_active", "website")
PERMISSIONS_FILE = os.path.join(os.path.dirname(__file__), "permissions.json")
AUDIT_LOG = os.path.join(PROJECT_ROOT, "logs", "admin-actions.log")
GITHUB_ORG = os.getenv("GITHUB_ORG", "osifeu-prog")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)

# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  DOCKER SDK
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
try:
    dc = docker.from_env(timeout=10)
    logging.info("Docker SDK connected")
except Exception as e:
    dc = None
    logging.error(f"Docker error: {e}")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=HTML))
dp = Dispatcher()
BOT_USERNAME = ""  # populated on startup

# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  GROUP CHAT FILTER ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ignore commands not directed at us
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
class GroupFilterMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, types.Message) and event.chat.type in ("group", "supergroup"):
            text = event.text or ""
            if text.startswith("/"):
                cmd = text.split()[0] if text.split() else ""
                if "@" in cmd:
                    if not cmd.lower().endswith(f"@{BOT_USERNAME.lower()}"):
                        return  # command for another bot
                else:
                    # bare /command in group ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ only respond if it's one of ours
                    our_cmd = cmd.lstrip("/").split("@")[0].lower()
                    if our_cmd not in OUR_COMMANDS:
                        return  # not our command
            else:
                return  # non-command text in group ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ignore
        return await handler(event, data)

OUR_COMMANDS = set()  # populated after COMMAND_DEFAULTS is defined

dp.message.middleware(GroupFilterMiddleware())

PUBLIC_COMMANDS = {"start", "create_me", "register", "my_access", "help"}

class AccessControlMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, types.Message) and event.text and event.text.startswith("/"):
            cmd = event.text.split()[0].lstrip("/").split("@")[0].lower()
            uid = event.from_user.id
            if uid == OWNER_ID or cmd in PUBLIC_COMMANDS:
                _middleware_passed.add(uid)
                try:
                    return await handler(event, data)
                finally:
                    _middleware_passed.discard(uid)
            effect, reason = await abac_check(uid, cmd)
            if effect == "allow":
                _middleware_passed.add(uid)
                try:
                    return await handler(event, data)
                finally:
                    _middleware_passed.discard(uid)
            logging.warning(f"ABAC DENY: uid={uid} cmd={cmd} reason={reason}")
            await deny_with_request(event, cmd, reason)
            return
        if isinstance(event, types.Message) and event.text and not event.text.startswith("/"):
            if event.from_user.id == OWNER_ID and OWNER_ID in _pending_messages:
                info = _pending_messages.pop(OWNER_ID)
                try:
                    await bot.send_message(
                        info["target_uid"],
                        f"├â┬░├à┬╕├óΓé¼Γäó├é┬¼ <b>├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£</b> (├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¿ ├âΓÇö├àΓÇ£-/{info['cmd']}):\n\n{event.text}"
                    )
                    await event.answer("├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├ù┬á├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥")
                except Exception as e:
                    await event.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:100]}")
                return
        return await handler(event, data)

dp.message.middleware(AccessControlMiddleware())

# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  IN-MEMORY STORAGE
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
agents = {}
tasks = {}
next_task_id = 1
_pending_messages = {}
users_db = {}

# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  ABAC ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Attribute-Based Access Control Engine v52
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
ROLE_LEVELS = {"owner": 3, "manager": 2, "viewer": 1, "none": 0}

# (category, risk 1-5, min_trust 0-10, allowed_teams, min_role)
COMMAND_DEFAULTS = {
    "start": ("general", 1, 0, "*", "none"),
    "create_me": ("general", 1, 0, "*", "none"),
    "register": ("general", 1, 0, "*", "none"),
    "my_access": ("general", 1, 0, "*", "none"),
    "status": ("monitor", 1, 0, "*", "viewer"),
    "health": ("monitor", 1, 0, "*", "viewer"),
    "logs": ("monitor", 2, 1, "*", "viewer"),
    "ps_raw": ("monitor", 1, 0, "*", "viewer"),
    "compose_logs": ("monitor", 2, 1, "*", "viewer"),
    "repos": ("git", 1, 0, "*", "viewer"),
    "files": ("git", 1, 0, "*", "viewer"),
    "read_file": ("git", 1, 0, "*", "viewer"),
    "task_status": ("agent", 1, 0, "*", "viewer"),
    "onboard": ("general", 1, 0, "*", "viewer"),
    "admins": ("admin", 1, 0, "*", "viewer"),
    "list_admins": ("admin", 1, 0, "*", "viewer"),
    "bots": ("monitor", 1, 0, "*", "viewer"),
    "ecosystem": ("general", 1, 0, "*", "viewer"),
    "site": ("monitor", 1, 0, "*", "viewer"),
    "dashboard": ("general", 1, 0, "*", "viewer"),
    "guide": ("general", 1, 0, "*", "viewer"),
    "ops_guide": ("general", 1, 0, "*", "viewer"),
    "find_files": ("git", 1, 0, "*", "viewer"),
    "read_local": ("git", 2, 1, "*", "viewer"),
    "version": ("general", 1, 0, "*", "viewer"),
    "changelog": ("general", 1, 0, "*", "viewer"),
    "summary": ("monitor", 1, 0, "*", "viewer"),
    "roles": ("general", 1, 0, "*", "viewer"),
    "help_perms": ("general", 1, 0, "*", "viewer"),
    "docker_explain": ("general", 1, 0, "*", "viewer"),
    "commands_brief": ("general", 1, 0, "*", "viewer"),
    "commands_full": ("general", 1, 0, "*", "viewer"),
    "volume_check": ("monitor", 1, 0, "*", "viewer"),
    "env_check": ("monitor", 1, 0, "*", "viewer"),
    "version_check": ("monitor", 1, 0, "*", "viewer"),
    "agent_config": ("agent", 1, 0, "*", "viewer"),
    "agent_notes": ("agent", 1, 0, "*", "viewer"),
    "scan": ("infra", 2, 2, "dev,ops,debug", "manager"),
    "heal": ("infra", 3, 3, "dev,ops", "manager"),
    "sync": ("deploy", 3, 3, "dev,ops", "manager"),
    "restart": ("infra", 3, 2, "dev,ops,debug", "manager"),
    "register_agent": ("agent", 2, 2, "dev,ops", "manager"),
    "dispatch_task": ("agent", 2, 2, "dev,ops", "manager"),
    "complete_task": ("agent", 2, 2, "dev,ops", "manager"),
    "audit": ("agent", 2, 2, "dev,ops,debug", "manager"),
    "publish_summary": ("agent", 2, 2, "dev,ops", "manager"),
    "commit": ("git", 3, 3, "dev", "manager"),
    "git_pull": ("git", 2, 2, "dev,ops", "manager"),
    "git_push": ("git", 4, 4, "dev", "manager"),
    "report": ("monitor", 2, 1, "*", "manager"),
    "project_report": ("monitor", 2, 1, "*", "manager"),
    "handoff": ("general", 2, 2, "dev,ops", "manager"),
    "session_summary": ("general", 2, 2, "dev,ops", "manager"),
    "investigate": ("infra", 2, 2, "dev,ops,debug", "manager"),
    "services": ("monitor", 2, 1, "*", "manager"),
    "write_file": ("git", 4, 4, "dev", "manager"),
    "broadcast": ("admin", 3, 3, "dev,ops", "manager"),
    "post_update": ("admin", 3, 3, "dev,ops", "manager"),
    "morning": ("monitor", 1, 1, "*", "manager"),
    "dev_roadmap": ("general", 2, 2, "dev", "manager"),
    "db": ("data", 2, 2, "dev,ops", "manager"),
    "edit_agent": ("agent", 2, 2, "dev,ops", "viewer"),
    "agent_status": ("agent", 2, 2, "dev,ops", "manager"),
    "container_events": ("monitor", 2, 2, "dev,ops", "manager"),
    "notify_user": ("admin", 3, 3, "admin", "owner"),
    "up": ("infra", 5, 5, "ops", "owner"),
    "down": ("infra", 5, 5, "ops", "owner"),
    "rebuild": ("deploy", 5, 5, "ops", "owner"),
    "rebuild_all": ("deploy", 5, 5, "ops", "owner"),
    "deploy": ("deploy", 5, 5, "ops", "owner"),
    "rm": ("infra", 5, 5, "ops", "owner"),
    "db_query": ("data", 5, 5, "dev", "owner"),
    "recover": ("infra", 4, 4, "ops", "owner"),
    "recover_project": ("infra", 4, 4, "ops", "owner"),
    "add_admin": ("admin", 5, 5, "admin", "owner"),
    "remove_admin": ("admin", 5, 5, "admin", "owner"),
    "env_list": ("admin", 4, 4, "dev,ops", "owner"),
    "env_set": ("admin", 5, 5, "dev", "owner"),
    "admin_key": ("admin", 5, 5, "admin", "owner"),
    "init_db": ("data", 5, 5, "admin", "owner"),
    "selftest": ("monitor", 3, 3, "dev,ops", "owner"),
    "backup_db": ("data", 4, 4, "ops", "owner"),
    "set_price": ("admin", 5, 5, "admin", "owner"),
    "grant": ("admin", 5, 5, "admin", "owner"),
    "revoke": ("admin", 5, 5, "admin", "owner"),
    "requests": ("admin", 3, 3, "admin", "owner"),
    "permissions": ("admin", 3, 3, "admin", "owner"),
    "set_owner": ("admin", 5, 5, "admin", "owner"),
    "set_manager": ("admin", 5, 5, "admin", "owner"),
    "set_viewer": ("admin", 5, 5, "admin", "owner"),
    "delete_agent": ("agent", 4, 4, "dev", "owner"),
    "emergency": ("infra", 5, 5, "ops", "owner"),
    "cleanup": ("infra", 5, 5, "ops", "owner"),
    "memory_check": ("monitor", 3, 3, "ops", "owner"),
    "update_check": ("deploy", 4, 4, "ops", "owner"),
    "esp": ("esp", 2, 2, "dev,ops,debug", "manager"),
    "esp_pair": ("esp", 3, 3, "dev,ops", "manager"),
    "esp_screen": ("esp", 2, 2, "dev,ops,debug", "manager"),
    "esp_reboot": ("esp", 3, 3, "dev,ops", "manager"),
    "esp_list": ("esp", 1, 1, "*", "manager"),
    "user_attrs": ("admin", 3, 3, "*", "owner"),
    "user_set": ("admin", 4, 4, "*", "owner"),
    "cmd_info": ("admin", 2, 2, "*", "owner"),
    "cmd_set": ("admin", 4, 4, "*", "owner"),
    "policy_add": ("admin", 5, 5, "*", "owner"),
    "policy_list": ("admin", 2, 2, "*", "owner"),
    "policy_del": ("admin", 5, 5, "*", "owner"),
    "policy_toggle": ("admin", 4, 4, "*", "owner"),
    "abac_status": ("admin", 2, 2, "*", "owner"),
    "esp_serial": ("esp", 3, 3, "dev,ops", "manager"),
    "esp_serial_status": ("esp", 1, 1, "dev,ops,debug", "manager"),
    "esp_serial_reset": ("esp", 3, 3, "dev,ops", "manager"),
    "esp_ports": ("esp", 1, 1, "dev,ops,debug", "manager"),
    "esp_flash": ("esp", 5, 5, "dev,ops", "owner"),
    "esp_compile": ("esp", 3, 3, "dev,ops", "manager"),
    "esp_monitor": ("esp", 2, 2, "dev,ops,debug", "manager"),
    "esp_guide": ("general", 1, 0, "*", "viewer"),
    "agent_guide": ("general", 1, 0, "*", "viewer"),
    "maximize": ("general", 1, 0, "*", "viewer"),
    "tasks": ("tasks", 1, 0, "*", "viewer"),
    "task_new": ("tasks", 1, 0, "*", "viewer"),
    "task_pick": ("tasks", 1, 0, "*", "viewer"),
    "task_done": ("tasks", 1, 0, "*", "viewer"),
    "task_return": ("tasks", 1, 0, "*", "viewer"),
    "task_info": ("tasks", 1, 0, "*", "viewer"),
    "task_set": ("tasks", 2, 1, "*", "manager"),
    "task_comment": ("tasks", 1, 0, "*", "viewer"),
    "task_assign": ("tasks", 2, 1, "*", "manager"),
    "task_review": ("tasks", 1, 0, "*", "viewer"),
    "task_block": ("tasks", 1, 0, "*", "viewer"),
    "daily_report": ("monitor", 1, 0, "*", "viewer"),
    "connect_github": ("saas", 1, 0, "*", "viewer"),
    "my_repos": ("saas", 1, 0, "*", "viewer"),
    "analyze": ("saas", 2, 1, "*", "viewer"),
    "review": ("saas", 2, 1, "*", "viewer"),
    "invite": ("general", 1, 0, "*", "viewer"),
    "full_report": ("monitor", 2, 1, "*", "manager"),
    "evening_report": ("monitor", 1, 0, "*", "viewer"),
    "welcome": ("general", 1, 0, "*", "viewer"),
    "group_register": ("general", 1, 0, "*", "viewer"),
    "group_my_role": ("general", 1, 0, "*", "viewer"),
    "group_register": ("general", 1, 0, "*", "viewer"),
    "group_my_role": ("general", 1, 0, "*", "viewer"),
    "parallel_guide": ("general", 1, 0, "*", "viewer"),
    "send_welcome": ("admin", 5, 5, "admin", "owner"),
}

COMMAND_ROLES = {cmd: attrs[4] for cmd, attrs in COMMAND_DEFAULTS.items()}
OUR_COMMANDS.update(COMMAND_DEFAULTS.keys())

_abac_cache = {"users": {}, "cmds": {}, "policies": None, "pol_ts": 0}
_CACHE_TTL = 30
_middleware_passed = set()

def _safe_cmd(cmd: str) -> str:
    return re.sub(r'[^a-z0-9_]', '', cmd)[:50]

async def _pg_val(sql: str) -> str:
    if not dc: return ""
    try:
        pg = dc.containers.get("slh-postgres")
        r = pg.exec_run(["psql", "-U", "postgres", "-d", "slh_main", "-t", "-A", "-c", sql])
        return r.output.decode(errors="replace").strip()
    except: return ""

async def _pg_ok(sql: str) -> bool:
    if not dc: return False
    try:
        pg = dc.containers.get("slh-postgres")
        r = pg.exec_run(["psql", "-U", "postgres", "-d", "slh_main", "-c", sql])
        return r.exit_code == 0
    except: return False

async def get_user_attrs(uid: int) -> dict:
    now = _time.time()
    cached = _abac_cache["users"].get(uid)
    if cached and now - cached.get("_ts", 0) < _CACHE_TTL:
        return cached
    row = await _pg_val(
        f"SELECT user_id,username,full_name,role,team,trust_level,specialization,"
        f"active_hours,max_risk,is_active,notes FROM abac_users WHERE user_id={int(uid)}"
    )
    if row and "|" in row:
        p = row.split("|")
        if len(p) >= 10:
            attrs = {
                "user_id": int(p[0]), "username": p[1], "full_name": p[2],
                "role": p[3], "team": p[4], "trust_level": int(p[5] or 0),
                "specialization": p[6], "active_hours": p[7] or "0-24",
                "max_risk": int(p[8] or 1), "is_active": p[9] == "t",
                "notes": p[10] if len(p) > 10 else "", "_ts": now
            }
            _abac_cache["users"][uid] = attrs
            return attrs
    perms = load_permissions()
    pr = perms.get(str(uid))
    if pr:
        attrs = {
            "user_id": uid, "role": pr.get("role", "none"),
            "team": "admin" if uid == OWNER_ID else "general",
            "trust_level": 10 if uid == OWNER_ID else 1,
            "specialization": "", "active_hours": "0-24",
            "max_risk": 10 if uid == OWNER_ID else 1,
            "is_active": True, "_ts": now
        }
        _abac_cache["users"][uid] = attrs
        return attrs
    return None

async def get_cmd_attrs(cmd: str) -> dict:
    now = _time.time()
    cmd = _safe_cmd(cmd)
    cached = _abac_cache["cmds"].get(cmd)
    if cached and now - cached.get("_ts", 0) < _CACHE_TTL:
        return cached
    row = await _pg_val(
        f"SELECT command,category,risk_level,min_trust,allowed_teams,min_role,"
        f"requires_confirmation,cooldown_seconds,description_he "
        f"FROM command_attrs WHERE command='{cmd}'"
    )
    if row and "|" in row:
        p = row.split("|")
        if len(p) >= 6:
            attrs = {
                "command": p[0], "category": p[1], "risk_level": int(p[2] or 1),
                "min_trust": int(p[3] or 0), "allowed_teams": p[4] or "*",
                "min_role": p[5] or "owner",
                "requires_confirmation": len(p) > 6 and p[6] == "t",
                "cooldown_seconds": int(p[7] or 0) if len(p) > 7 else 0,
                "description_he": p[8] if len(p) > 8 else "", "_ts": now
            }
            _abac_cache["cmds"][cmd] = attrs
            return attrs
    d = COMMAND_DEFAULTS.get(cmd, ("general", 5, 5, "admin", "owner"))
    attrs = {
        "command": cmd, "category": d[0], "risk_level": d[1],
        "min_trust": d[2], "allowed_teams": d[3], "min_role": d[4],
        "requires_confirmation": False, "cooldown_seconds": 0,
        "description_he": "", "_ts": now
    }
    _abac_cache["cmds"][cmd] = attrs
    return attrs

async def get_policies() -> list:
    now = _time.time()
    if _abac_cache["policies"] is not None and now - _abac_cache["pol_ts"] < _CACHE_TTL:
        return _abac_cache["policies"]
    rows = await _pg_val(
        "SELECT id,name,priority,conditions,effect FROM abac_policies "
        "WHERE is_active=true ORDER BY priority DESC"
    )
    policies = []
    if rows:
        for line in rows.split("\n"):
            p = line.split("|")
            if len(p) >= 5:
                try:
                    policies.append({
                        "id": int(p[0]), "name": p[1], "priority": int(p[2]),
                        "conditions": json.loads(p[3]), "effect": p[4]
                    })
                except: pass
    _abac_cache["policies"] = policies
    _abac_cache["pol_ts"] = now
    return policies

def _eval_cond(val, cond):
    if isinstance(cond, list):
        return val in cond
    if isinstance(cond, dict):
        for op, thr in cond.items():
            if op == "eq" and val != thr: return False
            if op == "neq" and val == thr: return False
            if op in ("gte", ">=") and (not isinstance(val, (int, float)) or val < thr): return False
            if op in ("lte", "<=") and (not isinstance(val, (int, float)) or val > thr): return False
            if op in ("gt", ">") and (not isinstance(val, (int, float)) or val <= thr): return False
            if op in ("lt", "<") and (not isinstance(val, (int, float)) or val >= thr): return False
            if op == "in" and val not in thr: return False
            if op == "contains" and str(thr) not in str(val): return False
        return True
    return str(val) == str(cond)

def _matches_policy(ua: dict, ca: dict, env: dict, conds: dict) -> bool:
    for key, cond in conds.items():
        prefix, attr = (key.split(".", 1)) if "." in key else ("", key)
        src = {"user": ua, "command": ca, "cmd": ca, "env": env}.get(prefix)
        if not src: continue
        val = src.get(attr)
        if val is None: return False
        if not _eval_cond(val, cond): return False
    return True

async def abac_check(uid: int, cmd: str):
    if uid == OWNER_ID:
        return ("allow", "owner")
    ua = await get_user_attrs(uid)
    if not ua:
        return ("deny", "not_registered")
    if not ua.get("is_active", True):
        return ("deny", "inactive")
    ca = await get_cmd_attrs(cmd)
    now = datetime.datetime.now()
    env = {"hour": now.hour, "weekday": now.strftime("%a").lower(), "is_weekend": now.weekday() >= 5}
    hrs = ua.get("active_hours", "0-24")
    if hrs and hrs != "0-24" and "-" in hrs:
        try:
            h0, h1 = map(int, hrs.split("-"))
            if not (h0 <= env["hour"] < h1):
                return ("deny", f"hours({hrs})")
        except: pass
    for pol in await get_policies():
        if _matches_policy(ua, ca, env, pol["conditions"]):
            return (pol["effect"], f"policy:{pol['name']}")
    teams = ca.get("allowed_teams", "*")
    if teams != "*" and ua.get("team", "general") not in teams.split(","):
        return ("deny", f"team({ua.get('team')})")
    if ua.get("trust_level", 0) < ca.get("min_trust", 0):
        return ("deny", f"trust({ua.get('trust_level',0)}<{ca.get('min_trust',0)})")
    if ca.get("risk_level", 1) > ua.get("max_risk", 1):
        return ("deny", f"risk({ca.get('risk_level',1)}>{ua.get('max_risk',1)})")
    if ROLE_LEVELS.get(ua.get("role", "none"), 0) >= ROLE_LEVELS.get(ca.get("min_role", "owner"), 0):
        return ("allow", f"role:{ua.get('role')}")
    try:
        cnt = await _pg_val(
            f"SELECT count(*) FROM command_permissions WHERE user_id={int(uid)} AND command='{_safe_cmd(cmd)}'"
        )
        if cnt and cnt.strip() not in ("0", ""):
            return ("allow", "direct_grant")
    except: pass
    return ("deny", f"role({ua.get('role','none')}<{ca.get('min_role','owner')})")

def invalidate_cache(uid: int = None, cmd: str = None):
    if uid: _abac_cache["users"].pop(uid, None)
    if cmd: _abac_cache["cmds"].pop(cmd, None)
    _abac_cache["policies"] = None

# ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼ backward-compat wrappers ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼
def load_permissions():
    if not os.path.exists(PERMISSIONS_FILE):
        default = {str(OWNER_ID): {"role": "owner", "name": "Osif"}}
        with open(PERMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    with open(PERMISSIONS_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save_permissions(perms):
    with open(PERMISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(perms, f, indent=2)

def get_user_role(uid: int) -> str:
    perms = load_permissions()
    user = perms.get(str(uid))
    if user:
        return user.get("role", "viewer")
    cached = _abac_cache["users"].get(uid)
    if cached:
        return cached.get("role", "none")
    return "none"

def is_allowed(uid: int, required: str) -> bool:
    if uid == OWNER_ID: return True
    if uid in _middleware_passed: return True
    return ROLE_LEVELS.get(get_user_role(uid), 0) >= ROLE_LEVELS.get(required, 0)

async def deny_with_request(m: types.Message, cmd: str, reason: str = ""):
    uid = m.from_user.id
    ua = await get_user_attrs(uid) or {}
    ca = await get_cmd_attrs(cmd)
    role = ua.get("role", get_user_role(uid))
    team = ua.get("team", "├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥")
    trust = ua.get("trust_level", 0)
    risk_icons = "├â┬░├à┬╕├à┬╕├é┬ó├â┬░├à┬╕├à┬╕├é┬í├â┬░├à┬╕├à┬╕├é┬á├â┬░├à┬╕├óΓé¼┬¥├é┬┤├â┬░├à┬╕├óΓé¼┬¥├é┬Ñ"
    risk_i = min(ca.get("risk_level", 1), 5) - 1
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├é┬⌐ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥", callback_data=f"reqaccess_{_safe_cmd(cmd)}_{uid}")]
    ])
    reason_map = {"not_registered": "├âΓÇö├àΓÇ£├ù┬É ├ù┬¿├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬", "inactive": "├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├óΓé¼╦£├ù┬¬"}
    reason_he = reason_map.get(reason.split("(")[0], reason) if reason else ""
    await m.answer(
        f"├â┬ó├óΓé¼┬║├óΓé¼┬¥ <b>├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-</b> <code>/{cmd}</code>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô: <b>{role}</b> | ├ù┬ª├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬ó├ù┬¬: <b>{team}</b> | ├ù┬É├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕: <b>{trust}</b>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬º├âΓÇö├ï┼ô├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥: <b>{ca.get('category','?')}</b> | "
        f"├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕: <b>{risk_icons[risk_i]} {ca.get('risk_level','?')}/5</b>\n"
        + (f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬¥: <i>{reason_he}</i>\n" if reason_he else "")
        + f"\n├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├ù┬Ñ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£:", reply_markup=kb
    )
    await audit(uid, f"/{cmd}", "denied", reason)

# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  AUDIT LOG
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
async def audit(user_id, cmd, result="ok", details=""):
    try:
        with open(AUDIT_LOG, "a") as f:
            ts = datetime.datetime.now().isoformat()
            f.write(f"{ts} | {user_id} | {cmd} | {result} | {details}\n")
    except:
        pass

# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  HTTP HELPERS
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
async def http_get(url, timeout=5):
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=timeout) as r:
                if r.status == 200:
                    return await r.json()
                return None
    except:
        return None

async def http_post(url, data=None, timeout=5):
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(url, json=data, timeout=timeout) as r:
                if r.status == 200:
                    return await r.json()
                return None
    except:
        return None

async def run_cmd(cmd, cwd=None):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd or PROJECT_ROOT
    )
    out, err = await proc.communicate()
    return out.decode(errors='replace'), err.decode(errors='replace'), proc.returncode

async def github_api(endpoint, method="GET", data=None):
    if not GITHUB_TOKEN:
        return None
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com{endpoint}"
    try:
        async with aiohttp.ClientSession() as s:
            if method == "GET":
                async with s.get(url, headers=headers, timeout=10) as r:
                    return await r.json() if r.status == 200 else None
            elif method == "POST":
                async with s.post(url, headers=headers, json=data, timeout=10) as r:
                    return await r.json() if r.status in (200, 201) else None
            elif method == "PUT":
                async with s.put(url, headers=headers, json=data, timeout=10) as r:
                    return await r.json() if r.status in (200, 201) else None
    except:
        return None

def sanitize_name(raw: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_\-]', '', raw)[:40]

async def pg_exec(sql: str) -> str:
    if not dc:
        return "ERROR: Docker SDK not available"
    try:
        pg = dc.containers.get("slh-postgres")
        result = pg.exec_run(["psql", "-U", "postgres", "-d", "slh_main", "-c", sql])
        return result.output.decode(errors="replace")[:3000]
    except Exception as e:
        return f"ERROR: {str(e)[:200]}"

# known project folders for /investigate and /recover
PROJECT_MAP = {
    "nfty": {"container": "slh-nfty-bot", "folder": "nfty-bot", "bot": "@SLH_NFTY_bot"},
    "nifti": {"container": "slh-nifti", "folder": "wellness-bot", "bot": "@NIFTI_Publisher_Bot"},
    "guardian": {"container": "slh-guardian-bot", "folder": "guardian-bot", "bot": "@SLH_GUARDIAN_bot"},
    "claude": {"container": "slh-claude-bot", "folder": "claude-bot", "bot": "@SLH_CLAUDE_BOT"},
    "trading": {"container": "slh-trading-bot", "folder": "trading-bot", "bot": "@SLH_TRADING_bot"},
    "staking": {"container": "slh-staking-bot", "folder": "staking-bot", "bot": "@SLH_STAKING_bot"},
    "wallet": {"container": "slh-wallet-bot", "folder": "wallet-bot", "bot": "@SLH_WALLET_bot"},
    "mining": {"container": "slh-mining-bot", "folder": "mining-bot", "bot": "@SLH_MINING_bot"},
    "admin": {"container": "slh-admin", "folder": "admin-bot", "bot": "@MY_SUPER_ADMIN_bot"},
    "esp": {"container": None, "folder": "device-registry", "bot": None},
    "website": {"container": None, "folder": "_active/website", "bot": None},
}


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  1. /start ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ MAIN MENU                              ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    await m.answer("SLH v53 ready. Send /help for commands.")

@dp.message(Command("register_agent"))
async def cmd_register_agent(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Requires manager role")
    parts = m.text.split(maxsplit=2)
    if len(parts) < 2:
        return await m.answer("Usage: /register_agent name [role]")
    name = parts[1]
    role = parts[2] if len(parts) > 2 else "worker"
    agents[name] = {"role": role, "registered_at": datetime.datetime.now().isoformat()}
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Agent '{name}' registered as '{role}'")
    await audit(m.from_user.id, "/register_agent", "ok", f"{name}:{role}")

@dp.message(Command("dispatch_task"))
async def cmd_dispatch_task(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Requires manager role")
    parts = m.text.split(maxsplit=2)
    if len(parts) < 3:
        return await m.answer("Usage: /dispatch_task agent_name description")
    agent_name, desc = parts[1], parts[2]
    if agent_name not in agents:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Agent '{agent_name}' not registered")
    global next_task_id
    tid = next_task_id
    tasks[tid] = {
        "agent": agent_name, "description": desc, "status": "pending",
        "created_at": datetime.datetime.now().isoformat(), "created_by": m.from_user.id
    }
    next_task_id += 1
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Task #{tid} dispatched to {agent_name}:\n{desc}")
    await audit(m.from_user.id, "/dispatch_task", "ok", f"#{tid} -> {agent_name}")

@dp.message(Command("task_status"))
async def cmd_task_status(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    if not tasks:
        return await m.answer("No tasks yet.")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Task Status</b>\n"
    for tid, t in tasks.items():
        icon = "├â┬ó├àΓÇ£├óΓé¼┬ª" if t["status"] == "completed" else "├ó┬Å┬│"
        text += f"{icon} #{tid} [{t['status']}] ├â┬ó├óΓÇÜ┬¼├óΓé¼┼ô {t['agent']}: {t['description'][:60]}\n"
    await m.answer(text[:4000])

@dp.message(Command("complete_task"))
async def cmd_complete_task(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Requires manager role")
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /complete_task task_id")
    try:
        tid = int(parts[1])
    except:
        return await m.answer("Invalid task ID")
    if tid not in tasks:
        return await m.answer(f"Task #{tid} not found")
    tasks[tid]["status"] = "completed"
    tasks[tid]["completed_at"] = datetime.datetime.now().isoformat()
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Task #{tid} completed")
    await audit(m.from_user.id, "/complete_task", "ok", str(tid))

@dp.message(Command("audit"))
async def cmd_audit(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    stats = {
        "agents": len(agents),
        "tasks_total": len(tasks),
        "tasks_pending": sum(1 for t in tasks.values() if t["status"] == "pending"),
        "tasks_completed": sum(1 for t in tasks.values() if t["status"] == "completed")
    }
    await m.answer(
        f"<b>Agent Hub Audit</b>\n"
        f"├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ Agents: {stats['agents']}\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Tasks: {stats['tasks_total']}\n"
        f"├ó┬Å┬│ Pending: {stats['tasks_pending']}\n"
        f"├â┬ó├àΓÇ£├óΓé¼┬ª Completed: {stats['tasks_completed']}"
    )

@dp.message(Command("onboard"))
async def cmd_onboard(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    await m.answer(
        "<b>├â┬░├à┬╕├óΓé¼┼ô├ï┼ô Agent Hub ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿</b>\n\n"
        "1. ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕: /register_agent MyBot worker\n"
        "2. ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥: /dispatch_task MyBot Check containers\n"
        "3. ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬: /task_status\n"
        "4. ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬ó: /complete_task 1\n"
        "5. ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥: /audit\n\n"
        "├ù┬¬├ù┬ñ├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É: /start"
    )

@dp.message(Command("publish_summary"))
async def cmd_publish_summary(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    pending = [t for t in tasks.values() if t["status"] == "pending"]
    if not pending:
        return await m.answer("No pending tasks!")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬ó Pending Tasks</b>\n"
    for t in pending[:10]:
        tid = list(tasks.keys())[list(tasks.values()).index(t)]
        text += f"├â┬ó├óΓÇÜ┬¼├é┬ó #{tid} ├â┬ó├óΓÇÜ┬¼├óΓé¼┼ô {t['agent']}: {t['description'][:50]}\n"
    await m.answer(text)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  3. DOCKER COMMANDS                                  ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("status"))
async def cmd_status(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    if not dc:
        return await m.answer("Docker SDK not available")
    containers = dc.containers.list(all=True)
    running = [c for c in containers if c.status == "running"]
    stopped = [c for c in containers if c.status != "running"]
    text = f"<b>├â┬░├à┬╕├é┬É├é┬│ Docker Status</b>\n├â┬░├à┬╕├à┬╕├é┬ó {len(running)} running | ├â┬░├à┬╕├óΓé¼┬¥├é┬┤ {len(stopped)} stopped\n\n"
    for c in sorted(containers, key=lambda x: x.name):
        icon = "├â┬░├à┬╕├à┬╕├é┬ó" if c.status == "running" else "├â┬░├à┬╕├óΓé¼┬¥├é┬┤"
        text += f"{icon} {c.name}\n"
    await m.answer(text[:4000])

@dp.message(Command("health"))
async def cmd_health(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    checks = []
    if dc:
        try:
            dc.ping()
            containers = dc.containers.list(all=True)
            running = sum(1 for c in containers if c.status == "running")
            checks.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª Docker: {running}/{len(containers)} containers")
        except:
            checks.append("├â┬ó├é┬¥├àΓÇÖ Docker unreachable")
    else:
        checks.append("├â┬ó├é┬¥├àΓÇÖ Docker SDK not loaded")
    data = await http_get(f"{LOCAL_BRIDGE}/api/health")
    checks.append("├â┬ó├àΓÇ£├óΓé¼┬ª Local Bridge: OK" if data else "├â┬ó├é┬¥├àΓÇÖ Local Bridge: down")
    data = await http_get(f"{RAILWAY_API}/api/health")
    checks.append("├â┬ó├àΓÇ£├óΓé¼┬ª Railway API: OK" if data and data.get("status") == "ok" else "├â┬ó├à┬í├é┬á├»┬╕┬Å Railway API: unreachable")
    await m.answer("<b>├â┬░├à┬╕├é┬Å├é┬Ñ Health Check</b>\n" + "\n".join(checks))

@dp.message(Command("restart"))
async def cmd_restart(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Manager role required")
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /restart container_name")
    name = parts[1]
    if not dc:
        return await m.answer("Docker SDK not available")
    try:
        c = dc.containers.get(name)
        c.restart(timeout=10)
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª {name} restarted")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")
    await audit(m.from_user.id, "/restart", "ok", name)

@dp.message(Command("logs"))
async def cmd_logs(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /logs container_name [lines]")
    name = parts[1]
    lines = int(parts[2]) if len(parts) > 2 else 30
    if not dc:
        return await m.answer("Docker SDK not available")
    try:
        c = dc.containers.get(name)
        log = c.logs(tail=lines).decode(errors="replace")
        if len(log) > 3500:
            doc = BufferedInputFile(log.encode("utf-8"), filename=f"{name}_logs.txt")
            await m.answer_document(doc, caption=f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ {name} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ last {lines} lines")
        else:
            await m.answer(f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ {name}</b>\n<pre>{log[-3500:]}</pre>")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")

@dp.message(Command("up"))
async def cmd_up(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    await m.answer("├â┬░├à┬╕├à┬í├óΓÇÜ┬¼ Starting all containers...")
    out, err, code = await run_cmd("docker compose up -d")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Done" if code == 0 else f"├â┬ó├é┬¥├àΓÇÖ {err[:300]}")
    await audit(m.from_user.id, "/up", "ok" if code == 0 else "fail")

@dp.message(Command("down"))
async def cmd_down(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    await m.answer("├ó┬Å┬╣ Stopping all containers...")
    out, err, code = await run_cmd("docker compose down")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª All stopped" if code == 0 else f"├â┬ó├é┬¥├àΓÇÖ {err[:300]}")
    await audit(m.from_user.id, "/down", "ok" if code == 0 else "fail")

@dp.message(Command("rebuild"))
async def cmd_rebuild(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /rebuild service_name")
    svc = parts[1]
    await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├é┬¿ Rebuilding {svc}...")
    out, err, code = await run_cmd(f"docker compose up -d --build {svc}")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª {svc} rebuilt" if code == 0 else f"├â┬ó├é┬¥├àΓÇÖ {err[:300]}")
    await audit(m.from_user.id, "/rebuild", "ok" if code == 0 else "fail", svc)

@dp.message(Command("rebuild_all"))
async def cmd_rebuild_all(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    await m.answer("├â┬░├à┬╕├óΓé¼┬¥├é┬¿ Rebuilding ALL services...")
    out, err, code = await run_cmd("docker compose up -d --build")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª All rebuilt" if code == 0 else f"├â┬ó├é┬¥├àΓÇÖ {err[:300]}")

@dp.message(Command("compose_logs"))
async def cmd_compose_logs(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    out, err, code = await run_cmd("docker compose logs --tail=30")
    text = out[-3500:] if out else err[-3500:]
    await m.answer(f"<pre>{text}</pre>")

@dp.message(Command("ps_raw"))
async def cmd_ps_raw(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    out, err, code = await run_cmd("docker compose ps")
    await m.answer(f"<pre>{out[-3500:]}</pre>")

# ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼ SCAN (deep container inspection) ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼
@dp.message(Command("scan"))
async def cmd_scan(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    if not dc:
        return await m.answer("Docker SDK not available")
    await m.answer("├â┬░├à┬╕├óΓé¼┬¥├é┬ì Scanning all containers...")
    containers = dc.containers.list(all=True)
    lines = [f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬ì Deep Scan ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {len(containers)} containers</b>\n"]
    for c in sorted(containers, key=lambda x: x.name):
        icon = "├â┬░├à┬╕├à┬╕├é┬ó" if c.status == "running" else "├â┬░├à┬╕├óΓé¼┬¥├é┬┤"
        img = c.image.tags[0] if c.image.tags else "unknown"
        created = c.attrs.get("Created", "?")[:19]
        ports = ", ".join(f"{k}->{v}" for k, v in (c.ports or {}).items() if v) if c.ports else "none"
        restart_count = c.attrs.get("RestartCount", 0)
        lines.append(
            f"{icon} <b>{c.name}</b>\n"
            f"   Image: {img}\n"
            f"   Status: {c.status} | Restarts: {restart_count}\n"
            f"   Created: {created}\n"
            f"   Ports: {ports}"
        )
    text = "\n".join(lines)
    if len(text) > 4000:
        doc = BufferedInputFile(text.encode("utf-8"), filename="scan_report.txt")
        await m.answer_document(doc, caption=f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì Scan: {len(containers)} containers")
    else:
        await m.answer(text)
    await audit(m.from_user.id, "/scan", "ok")

# ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼ HEAL (auto-restart stopped containers) ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼
@dp.message(Command("heal"))
async def cmd_heal(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Manager role required")
    if not dc:
        return await m.answer("Docker SDK not available")
    containers = dc.containers.list(all=True)
    stopped = [c for c in containers if c.status in ("exited", "dead", "created")]
    if not stopped:
        return await m.answer("├â┬ó├àΓÇ£├óΓé¼┬ª All containers healthy ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ nothing to heal")
    await m.answer(f"├â┬░├à┬╕├é┬⌐├é┬║ Healing {len(stopped)} stopped containers...")
    results = []
    for c in stopped:
        try:
            c.restart(timeout=15)
            results.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª {c.name} restarted")
        except Exception as e:
            results.append(f"├â┬ó├é┬¥├àΓÇÖ {c.name}: {str(e)[:80]}")
    await m.answer("\n".join(results)[:4000])
    await audit(m.from_user.id, "/heal", "ok", f"{len(stopped)} containers")


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  4. ORCHESTRATOR                                     ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("sync"))
async def cmd_sync(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    if not dc:
        return await m.answer("Docker SDK not available")
    containers = dc.containers.list(all=True)
    running = [c.name for c in containers if c.status == "running"]
    text = "├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ <b>Running services</b>\n" + "\n".join(f"├â┬ó├óΓÇÜ┬¼├é┬ó {n}" for n in sorted(running)) if running else "No containers running"
    await m.answer(text[:4000])
    await audit(m.from_user.id, "/sync", "ok")

@dp.message(Command("deploy"))
async def cmd_deploy(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /deploy service_name")
    service = parts[1]
    await m.answer(f"├â┬░├à┬╕├à┬í├óΓÇÜ┬¼ Deploying {service}...")
    out, err, code = await run_cmd(f"docker compose up -d --build {service}")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª {service} deployed" if code == 0 else f"├â┬ó├é┬¥├àΓÇÖ {err[:200]}")
    await audit(m.from_user.id, "/deploy", "ok" if code == 0 else "fail", service)

@dp.message(Command("rm"))
async def cmd_rm(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /rm container_name")
    name = parts[1]
    out, err, code = await run_cmd(f"docker rm -f {name}")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Removed {name}" if code == 0 else f"├â┬ó├é┬¥├àΓÇÖ {err[:200]}")


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  5. GITHUB COMMANDS (restored from v40)              ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("repos"))
async def cmd_repos(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    if not GITHUB_TOKEN:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ GITHUB_TOKEN not set in .env")
    data = await github_api(f"/orgs/{GITHUB_ORG}/repos?per_page=50&sort=updated")
    if not data:
        data = await github_api(f"/users/{GITHUB_ORG}/repos?per_page=50&sort=updated")
    if not data:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Could not fetch repos. Check GITHUB_TOKEN / GITHUB_ORG")
    text = f"<b>├â┬░├à┬╕├óΓé¼┼ô├à┬í GitHub Repos ({GITHUB_ORG})</b>\n\n"
    for r in data[:30]:
        vis = "├â┬░├à┬╕├óΓé¼┬¥├óΓé¼Γäó" if r.get("private") else "├â┬░├à┬╕├àΓÇÖ├é┬É"
        lang = r.get("language", "?")
        text += f"{vis} <b>{r['name']}</b> ({lang})\n"
    await m.answer(text[:4000])
    await audit(m.from_user.id, "/repos", "ok")

@dp.message(Command("files"))
async def cmd_files(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /files repo_name [path]\nExample: /files slh-api src/")
    repo = parts[1]
    path = parts[2] if len(parts) > 2 else ""
    if not GITHUB_TOKEN:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ GITHUB_TOKEN not set")
    data = await github_api(f"/repos/{GITHUB_ORG}/{repo}/contents/{path}")
    if not data:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Could not fetch files from {repo}/{path}")
    if isinstance(data, list):
        text = f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼í {repo}/{path or '/'}</b>\n\n"
        for item in sorted(data, key=lambda x: (x["type"] != "dir", x["name"])):
            icon = "├â┬░├à┬╕├óΓé¼┼ô├é┬ü" if item["type"] == "dir" else "├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛"
            text += f"{icon} {item['name']}\n"
        await m.answer(text[:4000])
    else:
        await m.answer(f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛ {data.get('name', path)} ({data.get('size', '?')} bytes)")

@dp.message(Command("read_file"))
async def cmd_read_file_github(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    parts = m.text.split()
    if len(parts) < 3:
        return await m.answer("Usage: /read_file repo_name file_path\nExample: /read_file slh-api main.py")
    repo, fpath = parts[1], parts[2]
    if not GITHUB_TOKEN:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ GITHUB_TOKEN not set")
    data = await github_api(f"/repos/{GITHUB_ORG}/{repo}/contents/{fpath}")
    if not data or "content" not in data:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Could not read {repo}/{fpath}")
    import base64
    try:
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Could not decode file content")
    if len(content) > 3500:
        doc = BufferedInputFile(content.encode("utf-8"), filename=os.path.basename(fpath))
        await m.answer_document(doc, caption=f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛ {repo}/{fpath}")
    else:
        await m.answer(f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛ {repo}/{fpath}</b>\n<pre>{content[:3500]}</pre>")

@dp.message(Command("commit"))
async def cmd_commit(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split(maxsplit=2)
    if len(parts) < 3:
        return await m.answer("Usage: /commit repo_name commit message\nExample: /commit slh-api fix: typo in config")
    repo, msg = parts[1], parts[2]
    repo_path = os.path.join(PROJECT_ROOT, repo)
    if not os.path.isdir(repo_path):
        repo_path = os.path.join(PROJECT_ROOT, "_active", repo)
    if not os.path.isdir(repo_path):
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Repo folder not found: {repo}")
    out, err, code = await run_cmd(f'git add -A && git commit -m "{msg}"', cwd=repo_path)
    if code == 0:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Committed to {repo}:\n{msg}\n\n<pre>{out[-1000:]}</pre>")
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Commit failed:\n<pre>{(out+err)[-1500:]}</pre>")
    await audit(m.from_user.id, "/commit", "ok" if code == 0 else "fail", f"{repo}: {msg[:50]}")

@dp.message(Command("git_pull"))
async def cmd_git_pull(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /git_pull repo_or_path\nExamples: /git_pull website | /git_pull api")
    target = parts[1]
    if target == "website":
        cwd = WEBSITE_PATH
    elif os.path.isdir(os.path.join(PROJECT_ROOT, target)):
        cwd = os.path.join(PROJECT_ROOT, target)
    elif os.path.isdir(os.path.join(PROJECT_ROOT, "_active", target)):
        cwd = os.path.join(PROJECT_ROOT, "_active", target)
    else:
        cwd = PROJECT_ROOT
    out, err, code = await run_cmd("git pull", cwd=cwd)
    await m.answer(f"<pre>{out[-2000:]}</pre>")
    await audit(m.from_user.id, "/git_pull", "ok", target)

@dp.message(Command("git_push"))
async def cmd_git_push(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /git_push repo_or_path")
    target = parts[1]
    if target == "website":
        cwd = WEBSITE_PATH
    elif os.path.isdir(os.path.join(PROJECT_ROOT, target)):
        cwd = os.path.join(PROJECT_ROOT, target)
    elif os.path.isdir(os.path.join(PROJECT_ROOT, "_active", target)):
        cwd = os.path.join(PROJECT_ROOT, "_active", target)
    else:
        cwd = PROJECT_ROOT
    out, err, code = await run_cmd("git add -A && git commit -m \"bot-push\" && git push", cwd=cwd)
    await m.answer(f"<pre>{(out+err)[-2000:]}</pre>")
    await audit(m.from_user.id, "/git_push", "ok" if code == 0 else "fail", target)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  6. BACKUP & REPORTS                                 ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("backup_db"))
async def cmd_backup_db(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return
    await m.answer("├â┬░├à┬╕├óΓé¼┼ô├é┬ñ Creating database backup via Docker SDK...")
    try:
        pg = dc.containers.get("slh-postgres")
        result = pg.exec_run("pg_dump -U postgres slh_main")
        if result.exit_code == 0:
            fname = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            doc = BufferedInputFile(result.output, filename=fname)
            await m.answer_document(doc, caption=f"├â┬ó├àΓÇ£├óΓé¼┬ª Backup: {fname} ({len(result.output)} bytes)")
        else:
            await m.answer(f"├â┬ó├é┬¥├àΓÇÖ pg_dump failed: {result.output.decode(errors='replace')[:200]}")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Backup error: {str(e)[:200]}")
    await audit(m.from_user.id, "/backup_db", "ok")

@dp.message(Command("report"))
async def cmd_report(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    report = f"<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á System Report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</b>\n\n"
    if dc:
        containers = dc.containers.list(all=True)
        running = sum(1 for c in containers if c.status == "running")
        report += f"├â┬░├à┬╕├é┬É├é┬│ Docker: {running}/{len(containers)} running\n"
    bridge = await http_get(f"{LOCAL_BRIDGE}/api/health")
    report += f"├â┬░├à┬╕├àΓÇÖ├óΓé¼┬░ Local Bridge: {'├â┬ó├àΓÇ£├óΓé¼┬ª' if bridge else '├â┬ó├é┬¥├àΓÇÖ'}\n"
    railway = await http_get(f"{RAILWAY_API}/api/health")
    report += f"├â┬░├à┬╕├à┬í├óΓé¼┼í Railway: {'├â┬ó├àΓÇ£├óΓé¼┬ª' if railway and railway.get('status')=='ok' else '├â┬ó├à┬í├é┬á├»┬╕┬Å'}\n"
    esp = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    report += f"├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32: {len(esp.get('devices', []))} devices\n" if esp else "├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32: offline\n"
    report += f"\n├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ Agents: {len(agents)} | ├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Tasks: {len(tasks)}"
    await m.answer(report[:4000])
    await audit(m.from_user.id, "/report", "ok")

@dp.message(Command("project_report"))
async def cmd_project_report(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /project_report project_name")
    name = parts[1].lower()
    lines = [f"<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á Project Report: {name.upper()}</b>\n"]
    project_path = os.path.join(PROJECT_ROOT, name)
    alt_path = os.path.join(PROJECT_ROOT, "_active", name)
    path = project_path if os.path.isdir(project_path) else alt_path if os.path.isdir(alt_path) else None
    if path:
        py_files = glob.glob(os.path.join(path, "**", "*.py"), recursive=True)
        js_files = glob.glob(os.path.join(path, "**", "*.js"), recursive=True)
        lines.append(f"├â┬░├à┬╕├óΓé¼┼ô├é┬ü Path: {path}")
        lines.append(f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛ Python: {len(py_files)} | JS: {len(js_files)}")
        dockerfile = os.path.exists(os.path.join(path, "Dockerfile"))
        lines.append(f"├â┬░├à┬╕├é┬É├é┬│ Dockerfile: {'├â┬ó├àΓÇ£├óΓé¼┬ª' if dockerfile else '├â┬ó├é┬¥├àΓÇÖ'}")
    else:
        lines.append("├â┬░├à┬╕├óΓé¼┼ô├é┬ü Folder not found locally")
    if dc:
        for c in dc.containers.list(all=True):
            if name in c.name.lower():
                icon = "├â┬░├à┬╕├à┬╕├é┬ó" if c.status == "running" else "├â┬░├à┬╕├óΓé¼┬¥├é┬┤"
                lines.append(f"{icon} Container: {c.name} ({c.status})")
    await m.answer("\n".join(lines)[:4000])

@dp.message(Command("selftest"))
async def cmd_selftest(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    results = []
    if dc:
        try:
            dc.ping()
            results.append("├â┬ó├àΓÇ£├óΓé¼┬ª Docker SDK")
        except:
            results.append("├â┬ó├é┬¥├àΓÇÖ Docker SDK ping failed")
    else:
        results.append("├â┬ó├é┬¥├àΓÇÖ Docker SDK not available")
    data = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    results.append("├â┬ó├àΓÇ£├óΓé¼┬ª Local Bridge" if data else "├â┬ó├é┬¥├àΓÇÖ Local Bridge unreachable")
    data = await http_get(f"{RAILWAY_API}/api/health")
    results.append("├â┬ó├àΓÇ£├óΓé¼┬ª Railway API" if data and data.get("status") == "ok" else "├â┬ó├é┬¥├àΓÇÖ Railway API down")
    if GITHUB_TOKEN:
        data = await github_api("/user")
        results.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª GitHub API ({data.get('login','')})" if data else "├â┬ó├é┬¥├àΓÇÖ GitHub API")
    else:
        results.append("├â┬ó├à┬í├é┬á├»┬╕┬Å GitHub: no token")
    await m.answer("<b>├â┬░├à┬╕├é┬º├é┬¬ Self-Test Results</b>\n" + "\n".join(results))
    await audit(m.from_user.id, "/selftest", "ok")


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  7. ADMIN & PERMISSIONS                              ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

@dp.message(Command("db"))
async def cmd_db(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    if not users_db:
        return await m.answer("No registered users.")
    text = "<b>Registered Users</b>\n"
    for uid, info in users_db.items():
        text += f"├â┬ó├óΓÇÜ┬¼├é┬ó {info['name']} ({uid}) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {info.get('phone', 'no phone')}\n"
    await m.answer(text[:4000])

@dp.message(Command("register"))
async def cmd_register(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    parts = m.text.split(maxsplit=2)
    if len(parts) < 2:
        return await m.answer("Usage: /register name [phone]")
    name = parts[1]
    phone = parts[2] if len(parts) > 2 else ""
    users_db[m.from_user.id] = {"name": name, "phone": phone, "registered_at": datetime.datetime.now().isoformat()}
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª {name} registered")
    await audit(m.from_user.id, "/register", "ok", name)

@dp.message(Command("list_admins"))
async def cmd_list_admins(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    perms = load_permissions()
    text = "<b>├â┬░├à┬╕├óΓé¼╦£├é┬Ñ Admin List</b>\n"
    for uid, data in perms.items():
        text += f"├â┬ó├óΓÇÜ┬¼├é┬ó {data['name']} ({uid}) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {data['role']}\n"
    await m.answer(text)

@dp.message(Command("post_update"))
async def cmd_post_update(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer("Usage: /post_update message")
    msg = parts[1]
    await m.answer(f"├â┬░├à┬╕├óΓé¼┼ô├é┬ó Update: {msg}")
    await audit(m.from_user.id, "/post_update", "ok", msg[:50])

@dp.message(Command("create_me"))
async def cmd_create_me(m: types.Message):
    uid = m.from_user.id
    name = m.from_user.full_name or "User"
    uname = m.from_user.username or ""
    perms = load_permissions()
    if str(uid) in perms:
        return await m.answer(f"├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕: {perms[str(uid)]['role']}")
    perms[str(uid)] = {"role": "viewer", "name": name}
    save_permissions(perms)
    await _pg_ok(
        f"INSERT INTO abac_users (user_id,username,full_name,role,team,trust_level,max_risk) "
        f"VALUES ({uid},'{uname}','{name.replace(chr(39),'')}','viewer','general',1,2) "
        f"ON CONFLICT (user_id) DO NOTHING"
    )
    invalidate_cache(uid=uid)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├é┬⌐ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐ ├ù┬⌐├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô", callback_data=f"reqaccess_start_{uid}")]
    ])
    await m.answer(
        f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿!</b>\n\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ ├ù┬⌐├ù┬¥: {name}\n"
        f"├â┬░├à┬╕├óΓé¼┬á├óΓé¼┬¥ ID: <code>{uid}</code>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô: <b>viewer</b> | ├ù┬ª├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬ó├ù┬¬: <b>general</b>\n\n"
        f"<b>├â┬░├à┬╕├à┬í├óΓÇÜ┬¼ ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬║├ù┬É├âΓÇö├à┬╕:</b>\n"
        f"/welcome ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐\n"
        f"/tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        f"/connect_github ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ GitHub\n"
        f"├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬ñ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ AI ├âΓÇö├óΓÇ₧┬ó├ù┬ó├ù┬á├âΓÇö├óΓé¼┬¥!\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├é┬╕ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ AI ├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥!", reply_markup=kb
    )
    await audit(uid, "/create_me", "ok", f"viewer:{name}")
    try:
        await bot.send_message(OWNER_ID, f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐: {name} (<code>{uid}</code>)\n/user_set {uid} role viewer")
    except: pass

@dp.message(Command("add_admin"))
async def cmd_add_admin(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split()
    if len(parts) < 3:
        return await m.answer("Usage: /add_admin user_id name [role]")
    uid_str, name = parts[1], parts[2]
    role = parts[3] if len(parts) > 3 else "manager"
    perms = load_permissions()
    perms[uid_str] = {"role": role, "name": name}
    save_permissions(perms)
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Added {name} ({uid_str}) as {role}")
    await audit(m.from_user.id, "/add_admin", "ok", f"{uid_str}:{role}")

@dp.message(Command("remove_admin"))
async def cmd_remove_admin(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /remove_admin user_id")
    uid_str = parts[1]
    perms = load_permissions()
    if uid_str in perms:
        del perms[uid_str]
        save_permissions(perms)
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Removed {uid_str}")
    else:
        await m.answer("User not found")

@dp.message(Command("admins"))
async def cmd_admins(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    perms = load_permissions()
    text = "<b>├â┬░├à┬╕├óΓé¼╦£├é┬Ñ Admins</b>\n"
    for uid, data in perms.items():
        text += f"├â┬ó├óΓÇÜ┬¼├é┬ó {data['name']} ({uid}) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {data['role']}\n"
    await m.answer(text)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  8. ENV & CONFIG                                     ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("env_list"))
async def cmd_env_list(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if not os.path.exists(env_path):
        return await m.answer("No .env file found")
    with open(env_path, "r") as f:
        names = [l.split("=")[0].strip() for l in f if "=" in l and not l.strip().startswith("#")]
    await m.answer(f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬É .env keys ({len(names)}):</b>\n" + "\n".join(names[:60]))

@dp.message(Command("env_set"))
async def cmd_env_set(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    await m.answer("├â┬ó├à┬í├é┬á├»┬╕┬Å For security, edit .env manually on the host machine.")

@dp.message(Command("admin_key"))
async def cmd_admin_key(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    import secrets as sec
    key = sec.token_urlsafe(32)
    await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼╦£ New admin key:\n<code>{key}</code>")


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  9. ESP32 COMMANDS                                   ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("esp"))
async def cmd_esp(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    data = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    if not data:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Local bridge unreachable")
    devices = data.get("devices", [])
    if not devices:
        return await m.answer("├â┬░├à┬╕├óΓé¼┼ô├é┬í No ESP32 devices registered")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32 Devices</b>\n\n"
    for d in devices:
        text += (
            f"├â┬ó├óΓÇÜ┬¼├é┬ó <b>{d['device_id']}</b>\n"
            f"  Status: {d.get('status', '?')} | FW: {d.get('fw', '?')}\n"
            f"  IP: {d.get('ip', '?')} | RSSI: {d.get('rssi', '?')} dBm\n"
            f"  Last seen: {d.get('last_seen', '?')}\n\n"
        )
    await m.answer(text[:4000])

@dp.message(Command("esp_pair"))
async def cmd_esp_pair(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split()
    device_id = parts[1] if len(parts) > 1 else "esp32-14335C6C32C0"
    data = await http_post(f"{LOCAL_BRIDGE}/api/device/claim/{device_id}", {"user_id": OWNER_ID})
    if data and data.get("ok"):
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Device {device_id} paired!\nToken: <code>{data.get('signing_token', '')[:20]}...</code>")
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Pairing failed: {data}")
    await audit(m.from_user.id, "/esp_pair", "ok" if data else "fail")

@dp.message(Command("esp_screen"))
async def cmd_esp_screen(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /esp_screen HOME|WALLET|BOTS|SYS|PAIR|DEMO|REBOOT")
    screen = parts[1].upper()
    valid = {"HOME", "WALLET", "BOTS", "SYS", "SYSTEM", "PAIR", "DEMO", "REBOOT", "REVOKE"}
    if screen not in valid:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Invalid. Choose: {', '.join(sorted(valid))}")
    device_id = parts[2] if len(parts) > 2 else "esp32-14335C6C32C0"
    data = await http_post(f"{LOCAL_BRIDGE}/api/esp/commands/{device_id}", {"command": screen})
    if data and data.get("ok"):
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª '{screen}' sent to {device_id}")
    else:
        await m.answer("├â┬ó├é┬¥├àΓÇÖ Failed ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ local_bridge running?")

@dp.message(Command("esp_reboot"))
async def cmd_esp_reboot(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    parts = m.text.split()
    device_id = parts[1] if len(parts) > 1 else "esp32-14335C6C32C0"
    data = await http_post(f"{LOCAL_BRIDGE}/api/esp/commands/{device_id}", {"command": "REBOOT"})
    if data and data.get("ok"):
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Reboot command sent to {device_id}")
    else:
        await m.answer("├â┬ó├é┬¥├àΓÇÖ Failed")

@dp.message(Command("esp_list"))
async def cmd_esp_list(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    data = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    if not data or not data.get("devices"):
        return await m.answer("No devices found")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í All ESP32 Devices</b>\n\n"
    for i, d in enumerate(data["devices"], 1):
        text += f"{i}. {d['device_id']} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {d.get('status','?')} (IP: {d.get('ip','?')})\n"
    await m.answer(text[:4000])

@dp.message(Command("esp_serial"))
async def cmd_esp_serial(m: types.Message):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer(
            "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32 Serial Interface</b>\n\n"
            "Usage: /esp_serial &lt;command&gt;\n\n"
            "<b>Available:</b>\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó PING ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ test connection\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó UI ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ refresh display\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó RED / GREEN / BLUE ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ test screens\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó HOME / WALLET / BOTS / SYS / DEMO\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó REBOOT ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ restart device\n\n"
            "/esp_serial_status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ check COM port\n"
            "/esp_serial_reset ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ reset device via DTR"
        )
    cmd = parts[1].strip().upper()
    data = await http_post(f"{LOCAL_BRIDGE}/cmd", {"cmd": cmd})
    if data and data.get("ok"):
        resp = data.get("response", "(no response)")
        await m.answer(
            f"├â┬░├à┬╕├óΓé¼┼ô├é┬í <b>ESP32 Serial</b>\n"
            f"├â┬ó├à┬╛├é┬í├»┬╕┬Å Sent: <code>{cmd}</code>\n"
            f"├â┬ó├é┬¼├óΓé¼┬ª├»┬╕┬Å Response: <code>{resp or '(empty)'}</code>\n"
            f"├â┬░├à┬╕├óΓé¼┬¥├àΓÇÖ Port: {data.get('port', '?')}"
        )
    else:
        err = data.get("error", "Unknown error") if data else "Local bridge unreachable"
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {err}")
    await audit(m.from_user.id, "/esp_serial", "ok", cmd)

@dp.message(Command("esp_serial_status"))
async def cmd_esp_serial_status(m: types.Message):
    data = await http_get(f"{LOCAL_BRIDGE}/api/serial/status")
    if not data:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Local bridge unreachable")
    if data.get("connected"):
        await m.answer(
            f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>ESP32 Connected</b>\n"
            f"├â┬░├à┬╕├óΓé¼┬¥├àΓÇÖ Port: {data.get('port')}\n"
            f"├â┬ó├à┬í├é┬í Baud: {data.get('baudrate')}"
        )
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ESP32 not connected: {data.get('error', '?')}")

@dp.message(Command("esp_serial_reset"))
async def cmd_esp_serial_reset(m: types.Message):
    data = await http_post(f"{LOCAL_BRIDGE}/api/serial/reset", {})
    if data and data.get("ok"):
        startup = data.get("startup", "")
        await m.answer(
            f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ <b>ESP32 Reset</b>\n"
            f"Startup: <code>{startup[:500] or '(no output)'}</code>"
        )
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {data.get('error', 'Failed') if data else 'Bridge unreachable'}")

@dp.message(Command("esp_ports"))
async def cmd_esp_ports(m: types.Message):
    data = await http_get(f"{LOCAL_BRIDGE}/api/serial/ports")
    if not data:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Local bridge unreachable")
    ports = data.get("ports", [])
    if not ports:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ No serial ports found")
    text = "<b>├â┬░├à┬╕├óΓé¼┬¥├àΓÇÖ Serial Ports</b>\n\n"
    for p in ports:
        text += f"├â┬ó├óΓÇÜ┬¼├é┬ó <b>{p['device']}</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {p['description']}\n"
    await m.answer(text)


@dp.message(Command("esp_flash"))
async def cmd_esp_flash(m: types.Message):
    parts = m.text.split()
    port = parts[1] if len(parts) > 1 else "COM5"
    msg = await m.answer(f"├â┬ó├à┬í├é┬í <b>Flashing SLH firmware to {port}...</b>\nThis may take 60-90 seconds.")
    data = await http_post(f"{LOCAL_BRIDGE}/api/esp/flash", {"port": port}, timeout=130)
    if not data:
        return await msg.edit_text("├â┬ó├é┬¥├àΓÇÖ Local bridge unreachable")
    if data.get("ok"):
        out = data.get("stdout", "")
        lines = [l for l in out.split("\n") if l.strip()][-5:]
        await msg.edit_text(
            f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>Firmware flashed successfully!</b>\n"
            f"├â┬░├à┬╕├óΓé¼┬¥├àΓÇÖ Port: {port}\n\n"
            f"<code>{'chr(10)'.join(lines)}</code>\n\n"
            f"Use /esp_serial PING to test."
        )
    else:
        err = data.get("error") or data.get("stderr", "")[:500]
        await msg.edit_text(f"├â┬ó├é┬¥├àΓÇÖ <b>Flash failed</b>\n<code>{err[:1000]}</code>")
    await audit(m.from_user.id, "/esp_flash", "ok" if data.get("ok") else "fail", port)


@dp.message(Command("esp_compile"))
async def cmd_esp_compile(m: types.Message):
    msg = await m.answer("├â┬░├à┬╕├óΓé¼┬¥├é┬¿ <b>Compiling SLH firmware...</b>")
    data = await http_post(f"{LOCAL_BRIDGE}/api/esp/compile", {}, timeout=130)
    if not data:
        return await msg.edit_text("├â┬ó├é┬¥├àΓÇÖ Local bridge unreachable")
    if data.get("ok"):
        out = data.get("stdout", "")
        size_lines = [l for l in out.split("\n") if "RAM" in l or "Flash" in l or "SUCCESS" in l][-3:]
        await msg.edit_text(
            f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>Compilation successful</b>\n"
            f"<code>{'chr(10)'.join(size_lines) or 'Build complete'}</code>\n\n"
            f"Ready to flash with /esp_flash"
        )
    else:
        err = data.get("error") or data.get("stderr", "")[:500]
        await msg.edit_text(f"├â┬ó├é┬¥├àΓÇÖ <b>Compile failed</b>\n<code>{err[:1000]}</code>")


@dp.message(Command("esp_monitor"))
async def cmd_esp_monitor(m: types.Message):
    data = await http_get(f"{LOCAL_BRIDGE}/api/serial/monitor")
    if not data:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Local bridge unreachable")
    if data.get("ok"):
        output = data.get("output", "") or "(no output)"
        await m.answer(
            f"├â┬░├à┬╕├óΓé¼┼ô├é┬║ <b>ESP32 Monitor</b> ({data.get('port', '?')})\n"
            f"<code>{output[:3500]}</code>"
        )
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {data.get('error', 'No connection')}")


@dp.message(Command("esp_guide"))
async def cmd_esp_guide(m: types.Message):
    await m.answer(
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É</b>\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 1 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿ ├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó:</b>\n"
        "├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ESP32 ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í USB.\n"
        "├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬º ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿: /esp_ports\n"
        "├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬º ├ù┬í├âΓÇö├ï┼ô├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬í: /esp_serial_status\n\n"
        "<b>├â┬ó├à┬í├é┬í ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 2 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├ù┬¬ firmware:</b>\n"
        "├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£: /esp_compile\n"
        "├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£: /esp_flash [COM_PORT]\n"
        "├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├âΓÇö├àΓÇ£: COM5\n\n"
        "<b>├â┬░├à┬╕├é┬º├é┬¬ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 3 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥:</b>\n"
        "/esp_serial PING ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬ª├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├àΓÇ£├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ PONG\n"
        "/esp_serial RED ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├ù┬É├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¥\n"
        "/esp_serial GREEN ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬º\n"
        "/esp_serial BLUE ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£\n"
        "/esp_serial HOME ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├ù┬¿├ù┬É├ù┬⌐├âΓÇö├óΓÇ₧┬ó\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬║ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 4 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬¿:</b>\n"
        "/esp_monitor ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├ù┬¬ serial output\n"
        "/esp_serial_reset ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ DTR reset\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬º ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 5 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬¿├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬º:</b>\n"
        "/esp ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├ï┼ô├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬í ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ (API)\n"
        "/esp_list ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥\n"
        "/esp_pair DEVICE ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐\n"
        "/esp_reboot DEVICE ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬É├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬¿├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬º\n"
        "/esp_screen WALLET DEVICE ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£├ù┬ñ├ù┬¬ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í\n\n"
        "<b>├â┬ó├à┬í├é┬á├»┬╕┬Å ├ù┬ñ├ù┬¬├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó ├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿? ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_ports ├âΓÇö├àΓÇ£├ù┬¿├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬É├ù┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬⌐ port\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£? ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_serial_reset ├âΓÇö├óΓé¼┬ó├ù┬É├âΓÇö├óΓé¼ΓÇ£ /esp_serial PING\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó ├ù┬ª├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í firmware ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐? ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_compile ├âΓÇö├óΓé¼┬ó├ù┬É├âΓÇö├óΓé¼ΓÇ£ /esp_flash\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó port ├ù┬¬├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬í? ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬í├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬ó├ù┬¿ Arduino IDE / Serial Monitor"
    )


@dp.message(Command("agent_guide"))
async def cmd_agent_guide(m: types.Message):
    await m.answer(
        "<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Agent Onboarding</b>\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 1 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕:</b>\n"
        "├âΓÇö├óΓé¼┬¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ /create_me\n"
        "├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô viewer ├âΓÇö├óΓé¼╦£├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬í├âΓÇö├óΓÇ₧┬ó\n\n"
        "<b>├â┬ó├é┬¼├óΓé¼┬á├»┬╕┬Å ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 2 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ (Owner ├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô):</b>\n"
        "/user_set UID role manager\n"
        "/user_set UID team dev\n"
        "/user_set UID trust_level 5\n"
        "/user_set UID max_risk 3\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 3 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├óΓé¼┬║├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕:</b>\n"
        "/register_agent AgentName worker\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬¿ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 4 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n"
        "/dispatch_task AgentName ├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥\n"
        "/task_status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/complete_task ID ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬ó\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬ì ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£ 5 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n"
        "├âΓÇö├óΓé¼┬¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ /my_access\n"
        "├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬º ├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬║├é┬í ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ABAC:</b>\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó viewer ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô (status, logs, health)\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó manager ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ (restart, deploy, tasks)\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó owner ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ (db_query, env_set, rebuild)\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó trust_level 0-10 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├à┬╛├ù┬¬ ├ù┬É├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó max_risk 1-5 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├ù┬º├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬├ù┬¿\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó team: dev/ops/debug/admin/general\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-ESP (├âΓÇö├àΓÇ£├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó ├ù┬⌐├âΓÇö├ï┼ô├âΓÇö├óΓé¼ΓÇ¥):</b>\n"
        "/user_set UID team dev\n"
        "/user_set UID trust_level 3\n"
        "├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼┬¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ ├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£:\n"
        "/esp_serial, /esp_serial_status, /esp_ports\n\n"
        "<b>├â┬ó├à┬í├é┬í ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥:</b>\n"
        "<code>/user_set 12345 role manager\n"
        "/user_set 12345 team dev\n"
        "/user_set 12345 trust_level 5\n"
        "/register_agent Zvika debugger\n"
        "/dispatch_task Zvika Check ESP connectivity</code>"
    )


@dp.message(Command("maximize"))
async def cmd_maximize(m: types.Message):
    await m.answer(
        "<b>├â┬░├à┬╕├à┬í├óΓÇÜ┬¼ ├âΓÇö├à┬╛├ù┬º├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Tips & Tricks</b>\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        "<b>├â┬░├à┬╕├àΓÇÖ├óΓé¼┬ª ├ù┬⌐├âΓÇö├óΓé¼Γäó├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿:</b>\n"
        "/morning ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É\n"
        "/health ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/selftest ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ó├ù┬ª├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬║├é┬í ├ù┬É├âΓÇö├óΓé¼╦£├âΓÇö├ï┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬║├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├ù┬ó├ù┬¥ ABAC:</b>\n"
        "/policy_add night deny {\"active_hours\":\"09:00-22:00\"}\n"
        "├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬¥ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥\n"
        "/policy_add risky deny {\"risk_level\":\"gte:4\",\"trust_level\":\"lte:3\"}\n"
        "├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬¥ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ 100 ESP ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        "1. ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ESP ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_ports\n"
        "2. ├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_flash COM_PORT\n"
        "3. ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬º ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_serial PING\n"
        "4. ├ù┬ª├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_pair DEVICE_ID\n"
        "5. ├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬¿├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬º ├â┬ó├óΓé¼┬á├óΓé¼Γäó /esp_screen, /esp_reboot\n\n"
        "<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        "/agent_guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├óΓé¼┬¥├ù┬ª├âΓÇö├ï┼ô├ù┬¿├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕\n"
        "/register_agent ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥\n"
        "/dispatch_task ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥\n"
        "/audit ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó├ù┬º├âΓÇö├óΓé¼┬¥:</b>\n"
        "/scan ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥\n"
        "/heal ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó\n"
        "/investigate SERVICE ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/container_events ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬É├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥\n\n"
        "<b>├â┬░├à┬╕├óΓé¼Γäó├é┬╛ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n"
        "/backup_db ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó PostgreSQL\n"
        "/report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬\n"
        "/handoff ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬╛├âΓÇö├à┬í ├âΓÇö├à┬╛├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬É\n\n"
        "<b>├â┬░├à┬╕├àΓÇÖ├é┬É Admin Panel:</b>\n"
        "slh-nft.com/admin.html?unlock\n"
        "├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓé¼┼ô ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É\n\n"
        "<b>├â┬ó├à┬í├é┬í ├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í:</b>\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó /status ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓé¼╦£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó /logs NAME 20 ├â┬ó├óΓé¼┬á├óΓé¼Γäó 20 ├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó /restart NAME ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐ ├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¬\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó /esp_serial PING ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ESP ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥"
    )


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  10. FILE OPERATIONS                                 ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("write_file"))
async def cmd_write_file(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split(maxsplit=2)
    if len(parts) < 3:
        return await m.answer("Usage: /write_file filename content")
    fname = parts[1]
    content = parts[2].strip('"').strip("'")
    if ".." in fname or fname.startswith("/"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Invalid filename")
    fpath = os.path.join(PROJECT_ROOT, fname)
    try:
        if os.path.dirname(fname):
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Written: {fname} ({len(content)} chars)")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")
    await audit(m.from_user.id, "/write_file", "ok", fname)

@dp.message(Command("read_local"))
async def cmd_read_local(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer("Usage: /read_local relative/path/to/file")
    fname = parts[1]
    if ".." in fname:
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Invalid path")
    fpath = os.path.join(PROJECT_ROOT, fname)
    if not os.path.isfile(fpath):
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ File not found: {fname}")
    try:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if len(content) > 3500:
            doc = BufferedInputFile(content.encode("utf-8"), filename=os.path.basename(fname))
            await m.answer_document(doc, caption=f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛ {fname}")
        else:
            await m.answer(f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼╛ {fname}</b>\n<pre>{content[:3500]}</pre>")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")

@dp.message(Command("find_files"))
async def cmd_find_files(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer("Usage: /find_files pattern\nExamples: /find_files *.py | /find_files guardian")
    pattern = parts[1]
    if "*" in pattern:
        files = glob.glob(os.path.join(PROJECT_ROOT, "**", pattern), recursive=True)
    else:
        files = glob.glob(os.path.join(PROJECT_ROOT, "**", f"*{pattern}*"), recursive=True)
    if not files:
        return await m.answer(f"No files matching '{pattern}'")
    text = f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬ì Files matching '{pattern}'</b>\n\n"
    for f in sorted(files)[:40]:
        rel = f.replace(PROJECT_ROOT, ".").replace("\\", "/")
        text += f"├â┬ó├óΓÇÜ┬¼├é┬ó {rel}\n"
    if len(files) > 40:
        text += f"\n<i>...+{len(files)-40} more</i>"
    await m.answer(text[:4000])


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  11. DATABASE INIT                                   ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("init_db"))
async def cmd_init_db(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    try:
        pg = dc.containers.get("slh-postgres")
        sql = (
            "CREATE TABLE IF NOT EXISTS bot_agents ("
            "  name TEXT PRIMARY KEY, role TEXT DEFAULT 'worker',"
            "  registered_at TIMESTAMP DEFAULT NOW(), registered_by BIGINT"
            ");"
            "CREATE TABLE IF NOT EXISTS bot_tasks ("
            "  id SERIAL PRIMARY KEY, agent TEXT REFERENCES bot_agents(name),"
            "  description TEXT NOT NULL, status TEXT DEFAULT 'pending',"
            "  created_at TIMESTAMP DEFAULT NOW(), completed_at TIMESTAMP, created_by BIGINT"
            ");"
            "CREATE TABLE IF NOT EXISTS system_events ("
            "  id SERIAL PRIMARY KEY, event_type TEXT, details TEXT,"
            "  created_at TIMESTAMP DEFAULT NOW()"
            ");"
            "CREATE TABLE IF NOT EXISTS deployments ("
            "  id SERIAL PRIMARY KEY, service TEXT, version TEXT,"
            "  deployed_at TIMESTAMP DEFAULT NOW(), deployed_by BIGINT, status TEXT DEFAULT 'ok'"
            ");"
            "CREATE TABLE IF NOT EXISTS project_notes ("
            "  id SERIAL PRIMARY KEY, project TEXT, note TEXT,"
            "  created_at TIMESTAMP DEFAULT NOW(), created_by BIGINT"
            ");"
            "CREATE TABLE IF NOT EXISTS access_requests ("
            "  id SERIAL PRIMARY KEY, user_id BIGINT, user_name TEXT,"
            "  command TEXT, status TEXT DEFAULT 'pending',"
            "  created_at TIMESTAMP DEFAULT NOW(), resolved_at TIMESTAMP, resolved_by BIGINT"
            ");"
            "CREATE TABLE IF NOT EXISTS task_board ("
            "  id SERIAL PRIMARY KEY, title TEXT NOT NULL, description TEXT DEFAULT '',"
            "  status TEXT DEFAULT 'open', priority TEXT DEFAULT 'normal',"
            "  project TEXT DEFAULT 'general', assigned_to BIGINT, assigned_name TEXT DEFAULT '',"
            "  created_by BIGINT, created_by_name TEXT DEFAULT '',"
            "  created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW(),"
            "  completed_at TIMESTAMP, notes TEXT DEFAULT ''"
            ");"
            "CREATE TABLE IF NOT EXISTS chat_messages ("
            "  id SERIAL PRIMARY KEY, user_id BIGINT, user_name TEXT,"
            "  message TEXT, response TEXT, created_at TIMESTAMP DEFAULT NOW()"
            ");"
            "CREATE TABLE IF NOT EXISTS command_permissions ("
            "  id SERIAL PRIMARY KEY, user_id BIGINT, command TEXT,"
            "  granted_by BIGINT, granted_at TIMESTAMP DEFAULT NOW(),"
            "  UNIQUE(user_id, command)"
            ");"
            "CREATE TABLE IF NOT EXISTS abac_users ("
            "  user_id BIGINT PRIMARY KEY, username TEXT DEFAULT '',"
            "  full_name TEXT DEFAULT '', role TEXT DEFAULT 'none',"
            "  team TEXT DEFAULT 'general', trust_level INT DEFAULT 0,"
            "  specialization TEXT DEFAULT '', active_hours TEXT DEFAULT '0-24',"
            "  max_risk INT DEFAULT 1, is_active BOOLEAN DEFAULT true,"
            "  created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW(),"
            "  notes TEXT DEFAULT ''"
            ");"
            "CREATE TABLE IF NOT EXISTS command_attrs ("
            "  command TEXT PRIMARY KEY, category TEXT DEFAULT 'general',"
            "  risk_level INT DEFAULT 1, min_trust INT DEFAULT 0,"
            "  allowed_teams TEXT DEFAULT '*', min_role TEXT DEFAULT 'owner',"
            "  requires_confirmation BOOLEAN DEFAULT false,"
            "  cooldown_seconds INT DEFAULT 0, description_he TEXT DEFAULT ''"
            ");"
            "CREATE TABLE IF NOT EXISTS abac_policies ("
            "  id SERIAL PRIMARY KEY, name TEXT NOT NULL,"
            "  description TEXT DEFAULT '', priority INT DEFAULT 50,"
            "  conditions JSONB NOT NULL, effect TEXT DEFAULT 'allow',"
            "  is_active BOOLEAN DEFAULT true,"
            "  created_at TIMESTAMP DEFAULT NOW(), created_by BIGINT"
            ");"
        )
        result = pg.exec_run(["psql", "-U", "postgres", "-d", "slh_main", "-c", sql])
        out = result.output.decode(errors='replace')
        if result.exit_code == 0:
            # Seed owner into abac_users
            seed_sql = (
                f"INSERT INTO abac_users (user_id,username,full_name,role,team,trust_level,max_risk) "
                f"VALUES ({OWNER_ID},'osif','Osif','owner','admin',10,10) ON CONFLICT (user_id) DO NOTHING;"
            )
            pg.exec_run(["psql", "-U", "postgres", "-d", "slh_main", "-c", seed_sql])
            # Seed command_attrs from defaults
            seed_cmds = []
            for cmd, (cat, risk, trust, teams, role) in COMMAND_DEFAULTS.items():
                seed_cmds.append(
                    f"INSERT INTO command_attrs (command,category,risk_level,min_trust,allowed_teams,min_role) "
                    f"VALUES ('{cmd}','{cat}',{risk},{trust},'{teams}','{role}') ON CONFLICT (command) DO NOTHING"
                )
            if seed_cmds:
                pg.exec_run(["psql", "-U", "postgres", "-d", "slh_main", "-c", ";".join(seed_cmds)])
            await m.answer(
                "├â┬ó├àΓÇ£├óΓé¼┬ª <b>ABAC Database initialized:</b>\n"
                "├â┬ó├óΓÇÜ┬¼├é┬ó bot_agents / bot_tasks / system_events\n"
                "├â┬ó├óΓÇÜ┬¼├é┬ó deployments / project_notes\n"
                "├â┬ó├óΓÇÜ┬¼├é┬ó access_requests / command_permissions\n"
                "├â┬ó├óΓÇÜ┬¼├é┬ó <b>abac_users</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
                "├â┬ó├óΓÇÜ┬¼├é┬ó <b>command_attrs</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬\n"
                "├â┬ó├óΓÇÜ┬¼├é┬ó <b>abac_policies</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥\n\n"
                f"├â┬░├à┬╕├óΓé¼┼ô├à┬á {len(COMMAND_DEFAULTS)} ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬á├âΓÇö├ï┼ô├ù┬ó├ù┬á├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£-command_attrs\n"
                f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ Owner seeded: {OWNER_ID}"
            )
        else:
            await m.answer(f"├â┬ó├é┬¥├àΓÇÖ SQL error: {out[:300]}")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")
    await audit(m.from_user.id, "/init_db", "ok")


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  12. INFO COMMANDS                                   ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("guide"))
async def cmd_guide(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    await m.answer(
        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬í SLH Complete Operations Guide</b>\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"

        "<b>├â┬░├à┬╕├é┬É├é┬│ Docker Management:</b>\n"
        "/status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ (running/stopped)\n"
        "/health ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬: Docker + Bridge + Railway\n"
        "/restart name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐ ├ù┬⌐├âΓÇö├àΓÇ£ ├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿\n"
        "/logs name [lines] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/up ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/down ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£\n"
        "/rebuild name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐ ├ù┬⌐├âΓÇö├àΓÇ£ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/rebuild_all ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐ ├ù┬⌐├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£\n"
        "/scan ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥ ├ù┬ó├ù┬¥ ├ù┬ñ├ù┬¿├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó image/ports/restarts\n"
        "/heal ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐ ├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬⌐├ù┬á├ù┬ñ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó\n"
        "/compose_logs ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/ps_raw ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ docker compose ps ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó\n"
        "/deploy name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ñ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬í├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/rm name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿\n"
        "/sync ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬í GitHub:</b>\n"
        "/repos ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼╦£├ù┬É├ù┬¿├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕\n"
        "/files repo [path] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼╦£├ù┬º├âΓÇö├óΓé¼╦£├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/read_file repo path ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬Ñ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó\n"
        "/commit repo message ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬ó commit\n"
        "/git_pull target ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬¥\n"
        "/git_push target ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬¥\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬¿├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬º:</b>\n"
        "/esp ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓé¼╦£ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/esp_pair [device_id] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿\n"
        "/esp_screen SCREEN [device_id] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£├ù┬ñ├ù┬¬ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í\n"
        "/esp_reboot [device_id] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬É├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£\n"
        "/esp_list ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬¥├àΓÇÖ ESP32 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Serial &amp; Flash:</b>\n"
        "/esp_serial cmd ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¬\n"
        "/esp_serial_status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓé¼╦£ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿ COM\n"
        "/esp_serial_reset ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ DTR reset\n"
        "/esp_ports ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├ù┬¬ COM ports\n"
        "/esp_compile ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥\n"
        "/esp_flash [port] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├ù┬¬ firmware\n"
        "/esp_monitor ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├ù┬¬ serial output\n\n"

        "<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ Agent Hub:</b>\n"
        "/register_agent name role ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ AI\n"
        "/dispatch_task agent desc ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥\n"
        "/task_status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/complete_task id ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬ó\n"
        "/audit ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ Hub\n"
        "/onboard ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿\n"
        "/publish_summary ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬\n\n"

        "<b>├â┬░├à┬╕├óΓé¼Γäó├é┬╛ Reports:</b>\n"
        "/backup_db ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó PostgreSQL (├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ SQL)\n"
        "/report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬\n"
        "/project_report name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô\n"
        "/selftest ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ó├ù┬ª├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/handoff ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬╛├âΓÇö├à┬í ├âΓÇö├à┬╛├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥\n"
        "/session_summary ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ ├ù┬í├ù┬⌐├âΓÇö├à┬╕\n"
        "/dev_roadmap ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ñ├ù┬¬ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/investigate name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬¥ Files:</b>\n"
        "/write_file path content ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├ù┬¬├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬Ñ\n"
        "/read_local path ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬Ñ ├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó\n"
        "/find_files pattern ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬⌐ ├ù┬º├âΓÇö├óΓé¼╦£├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¥\n\n"

        "<b>├â┬░├à┬╕├óΓé¼╦£├é┬Ñ Admin:</b>\n"
        "/add_admin uid name [role] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ñ├ù┬¬ ├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£\n"
        "/remove_admin uid ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬í├ù┬¿├âΓÇö├óΓé¼┬¥\n"
        "/admins ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥\n"
        "/create_me ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ viewer\n"
        "/register name ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬É Config:</b>\n"
        "/env_list ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├ù┬á├âΓÇö├óΓÇ₧┬ó ├ù┬í├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬¥\n"
        "/admin_key ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ñ├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐\n"
        "/init_db ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├ï┼ô├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ PostgreSQL\n\n"

        "<b>├â┬ó├óΓé¼┼╛├é┬╣├»┬╕┬Å Info:</b>\n"
        "/ecosystem ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ñ├ù┬¬ ├ù┬É├ù┬¿├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├ù┬º├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓé¼┬¥\n"
        "/site ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├ù┬É├ù┬¬├ù┬¿\n"
        "/dashboard ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/morning ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿\n"
        "/bots ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬"
    )

@dp.message(Command("bots"))
async def cmd_bots(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    bot_list = [
        ("Admin Bot", "@MY_SUPER_ADMIN_bot", "├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├ù┬¿├ù┬É├ù┬⌐├âΓÇö├óΓÇ₧┬ó ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Docker, GitHub, ESP32, DB, permissions"),
        ("Claude Bot", "@SLH_CLAUDE_BOT", "AI assistant ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬, ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô, ├ù┬ó├âΓÇö├óΓé¼ΓÇ£├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¬"),
        ("Guardian Bot", "@SLH_GUARDIAN_bot", "├ù┬⌐├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ heartbeat, alerts, auto-heal"),
        ("NFTY Bot", "@SLH_NFTY_bot", "├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ NFT ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ minting, metadata, marketplace"),
        ("Trading Bot", "@SLH_TRADING_bot", "├âΓÇö├à┬╛├ù┬í├âΓÇö├óΓé¼ΓÇ¥├ù┬¿ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ P2P trades, order book"),
        ("Staking Bot", "@SLH_STAKING_bot", "staking ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ lock tokens, rewards, APY"),
        ("Wallet Bot", "@SLH_WALLET_bot", "├ù┬É├ù┬¿├ù┬á├ù┬º ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ balances, transfers, QR"),
        ("Mining Bot", "@SLH_MINING_bot", "├âΓÇö├óΓé¼┬║├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ MNH mining, difficulty, rewards"),
        ("Governance Bot", "@SLH_GOV_bot", "├âΓÇö├óΓé¼┬¥├ù┬ª├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ proposals, voting, DAO"),
        ("Analytics Bot", "@SLH_ANALYTICS_bot", "├ù┬á├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ charts, reports, metrics"),
        ("Notification Bot", "@SLH_NOTIFY_bot", "├âΓÇö├óΓé¼┬¥├ù┬¬├ù┬¿├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ price alerts, events, reminders"),
        ("KYC Bot", "@SLH_KYC_bot", "├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ identity verification"),
        ("Support Bot", "@SLH_SUPPORT_bot", "├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ tickets, FAQ, help"),
        ("Airdrop Bot", "@SLH_AIRDROP_bot", "├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬º├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ token distribution, campaigns"),
        ("Bridge Bot", "@SLH_BRIDGE_bot", "├âΓÇö├óΓé¼Γäó├ù┬⌐├ù┬¿ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ cross-chain transfers"),
        ("Referral Bot", "@SLH_REFERRAL_bot", "├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ referral links, bonuses"),
        ("DEX Bot", "@SLH_DEX_bot", "DEX ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ decentralized exchange, liquidity"),
        ("Vault Bot", "@SLH_VAULT_bot", "├âΓÇö├óΓé¼┬║├ù┬í├ù┬ñ├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ secure storage, multi-sig"),
        ("Report Bot", "@SLH_REPORT_bot", "├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ daily/weekly reports"),
        ("Backup Bot", "@SLH_BACKUP_bot", "├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ automated backups"),
        ("Test Bot", "@SLH_TEST_bot", "├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ CI/CD integration tests"),
    ]
    text = "<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ SLH Bot Ecosystem (21 bots)</b>\n\n"
    for name, handle, desc in bot_list:
        text += f"<b>{name}</b> {handle}\n  {desc}\n\n"
    if len(text) > 4000:
        doc = BufferedInputFile(text.encode("utf-8"), filename="bots_list.txt")
        await m.answer_document(doc, caption="├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ All 21 SLH Bots")
    else:
        await m.answer(text)

@dp.message(Command("ecosystem"))
async def cmd_ecosystem(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    containers = ""
    try:
        dc = docker.from_env()
        cl = dc.containers.list(all=True)
        running = sum(1 for c in cl if c.status == "running")
        total = len(cl)
        containers = f"{running}/{total} running"
    except:
        containers = "N/A"
    open_t = (await _pg_val("SELECT count(*) FROM task_board WHERE status!='done'") or "0").strip()
    users_t = (await _pg_val("SELECT count(*) FROM abac_users") or "0").strip()
    msg1 = (
        f"<b>├â┬░├à┬╕├óΓé¼ΓÇ¥├é┬║ SLH Ecosystem Map v53</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        f"<b>├â┬ó├ï┼ô├é┬ü├»┬╕┬Å CLOUD ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Railway</b>\n"
        f"  FastAPI ~230 endpoints\n"
        f"  slh-api-production.up.railway.app\n\n"
        f"<b>├â┬░├à┬╕├é┬É├é┬│ DOCKER ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {containers}</b>\n"
        f"  ├â┬ó├óΓé¼┬¥├àΓÇ£ <b>Infrastructure</b>\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  PostgreSQL 15 ├é┬╖ Redis 7\n"
        f"  ├â┬ó├óΓé¼┬¥├àΓÇ£ <b>Core Bots</b>\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  Admin (v53) ├é┬╖ Claude ├é┬╖ Guardian\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  Core ├é┬╖ Wallet ├é┬╖ Game\n"
        f"  ├â┬ó├óΓé¼┬¥├àΓÇ£ <b>Economy</b>\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  NFT Shop ├é┬╖ NFTY ├é┬╖ Nifti\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  TON ├é┬╖ Chance ├é┬╖ Ledger\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  BeyNoniBank ├é┬╖ Airdrop\n"
        f"  ├â┬ó├óΓé¼┬¥├àΓÇ£ <b>Platform</b>\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  Crazy Panel ├é┬╖ TS Set ├é┬╖ Campaign\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  Factory ├é┬╖ BotShop ├é┬╖ Osif Shop\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┼í  Fun Bot ├é┬╖ Test Bot ├é┬╖ TON MNH\n"
        f"  ├â┬ó├óΓé¼┬¥├óΓé¼┬¥ <b>New</b>\n"
        f"     Academia\n\n"
        f"<b>├â┬░├à┬╕├óΓé¼ΓÇ£├é┬Ñ LOCAL BRIDGE</b> (port 8090)\n"
        f"  SQLite API ├é┬╖ Serial (COM5)\n"
        f"  Flash/Compile via PlatformIO\n\n"
        f"<b>├â┬░├à┬╕├óΓé¼┼ô├à┬╕ ESP32 CYD</b> (10.0.0.4)\n"
        f"  ILI9341 TFT + XPT2046 touch\n"
        f"  5 screens ├é┬╖ WiFi ├é┬╖ dual-path API\n\n"
        f"<b>├â┬░├à┬╕├àΓÇÖ├é┬É WEB</b>\n"
        f"  slh-nft.com ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ GitHub Pages (140+ pages)\n"
        f"  admin.html ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ABAC dashboard\n"
    )
    msg2 = (
        f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬É ABAC ENGINE</b>\n"
        f"  8-layer access control\n"
        f"  {users_t} registered users\n"
        f"  130+ managed commands\n\n"
        f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ TASK BOARD</b>\n"
        f"  {open_t} open tasks\n"
        f"  Inline buttons ├é┬╖ Project grouping\n"
        f"  Pick/Done/Return workflow\n\n"
        f"<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ AI CAPABILITIES</b>\n"
        f"  Free-text chat (GPT-4o-mini)\n"
        f"  Screenshot analysis (vision)\n"
        f"  Code review & repo analysis\n\n"
        f"<b>├â┬░├à┬╕├óΓé¼Γäó├à┬╜ TOKENS</b>: SLH ├é┬╖ MNH ├é┬╖ ZVK ├é┬╖ REP ├é┬╖ ZUZ\n\n"
        f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬º MANAGEMENT COMMANDS</b>\n"
        f"  /tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        f"  /daily_report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó\n"
        f"  /full_report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É\n"
        f"  /connect_github ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿ GitHub\n"
        f"  /welcome ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥\n"
        f"  /maximize ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬"
    )
    await m.answer(msg1)
    await m.answer(msg2)

@dp.message(Command("site"))
async def cmd_site(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    checks = []
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://slh-nft.com", timeout=10) as r:
                checks.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª slh-nft.com ({r.status})" if r.status == 200 else f"├â┬ó├à┬í├é┬á├»┬╕┬Å slh-nft.com ({r.status})")
    except:
        checks.append("├â┬ó├à┬í├é┬á├»┬╕┬Å slh-nft.com unreachable")
    data = await http_get(f"{RAILWAY_API}/api/health")
    checks.append("├â┬ó├àΓÇ£├óΓé¼┬ª Railway API" if data and data.get("status") == "ok" else "├â┬ó├à┬í├é┬á├»┬╕┬Å Railway API")
    data = await http_get(f"{LOCAL_BRIDGE}/api/health")
    checks.append("├â┬ó├àΓÇ£├óΓé¼┬ª Local Bridge" if data else "├â┬ó├é┬¥├àΓÇÖ Local Bridge")
    await m.answer(
        "<b>├â┬░├à┬╕├àΓÇÖ├é┬É Site Status</b>\n" + "\n".join(checks) +
        "\n\n<b>Links:</b>\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó slh-nft.com\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó slh-nft.com/admin.html?unlock\n"
        "├â┬ó├óΓÇÜ┬¼├é┬ó slh-api-production.up.railway.app/docs"
    )

@dp.message(Command("dashboard"))
async def cmd_dashboard(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    await m.answer(
        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á Dashboard Links</b>\n\n"
        "├â┬░├à┬╕├àΓÇÖ├é┬É Website: slh-nft.com\n"
        "├â┬░├à┬╕├óΓé¼┬¥├é┬º Admin: slh-nft.com/admin.html?unlock\n"
        "├â┬░├à┬╕├óΓé¼┼ô├é┬í API Docs: slh-api-production.up.railway.app/docs\n"
        "├â┬░├à┬╕├à┬╜├óΓé¼┬║ Control: slh-nft.com/control-center.html\n"
        "├â┬░├à┬╕├óΓé¼┼ô├é┬▒ Device: slh-nft.com/device-pair.html\n"
        "├â┬░├à┬╕├óΓé¼Γäó├é┬░ Staking: slh-nft.com/staking.html\n"
        "├â┬░├à┬╕├é┬Å├é┬ª Wallet: slh-nft.com/wallet.html\n"
        "├â┬░├à┬╕├óΓé¼┼ô├ïΓÇá Analytics: slh-nft.com/analytics.html"
    )

@dp.message(Command("morning"))
async def cmd_morning(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    text = f"<b>├â┬ó├ï┼ô├óΓÇÜ┬¼├»┬╕┬Å Morning Report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</b>\n\n"
    if dc:
        containers = dc.containers.list(all=True)
        running = sum(1 for c in containers if c.status == "running")
        stopped = sum(1 for c in containers if c.status != "running")
        text += f"├â┬░├à┬╕├é┬É├é┬│ Docker: {running} running / {stopped} stopped\n"
        if stopped > 0:
            text += "   ├â┬░├à┬╕├óΓé¼┬¥├é┬┤ " + ", ".join(c.name for c in containers if c.status != "running")[:200] + "\n"
    bridge = await http_get(f"{LOCAL_BRIDGE}/api/health")
    text += f"├â┬░├à┬╕├àΓÇÖ├óΓé¼┬░ Local Bridge: {'├â┬ó├àΓÇ£├óΓé¼┬ª' if bridge else '├â┬ó├é┬¥├àΓÇÖ'}\n"
    railway = await http_get(f"{RAILWAY_API}/api/health")
    text += f"├â┬░├à┬╕├à┬í├óΓé¼┼í Railway: {'├â┬ó├àΓÇ£├óΓé¼┬ª' if railway and railway.get('status') == 'ok' else '├â┬ó├à┬í├é┬á├»┬╕┬Å'}\n"
    esp = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    if esp and esp.get("devices"):
        for d in esp["devices"]:
            text += f"├â┬░├à┬╕├óΓé¼┼ô├é┬í {d['device_id']}: {d.get('status')} (RSSI: {d.get('rssi')})\n"
    else:
        text += "├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32: no devices\n"
    text += f"\n├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ Agents: {len(agents)} | ├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Tasks: {len(tasks)}"
    pending = sum(1 for t in tasks.values() if t["status"] == "pending")
    if pending:
        text += f" ({pending} pending)"
    await m.answer(text)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  13. INVESTIGATE + HANDOFF + SESSION                 ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("investigate"))
async def cmd_investigate(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return
    parts = m.text.split()
    if len(parts) < 2:
        known = ", ".join(sorted(PROJECT_MAP.keys()))
        return await m.answer(f"Usage: /investigate project_name\nKnown: {known}")
    project = sanitize_name(parts[1]).lower()
    if not project:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ Invalid project name")
    info = PROJECT_MAP.get(project, {})
    await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì Investigating <b>{project}</b>...")
    lines = [f"# {project.upper()} Investigation Report", f"Generated: {datetime.datetime.now().isoformat()}", ""]

    # files
    folder = info.get("folder", project)
    project_dir = os.path.join(PROJECT_ROOT, folder)
    if os.path.isdir(project_dir):
        all_files = glob.glob(os.path.join(project_dir, "**", "*"), recursive=True)
        py_files = [f for f in all_files if f.endswith(".py")]
        lines.append(f"## Folder: {folder}/")
        lines.append(f"Total files: {len(all_files)} | Python: {len(py_files)}")
        lines.append(f"Dockerfile: {'YES' if os.path.exists(os.path.join(project_dir, 'Dockerfile')) else 'NO'}")
        for f in py_files[:15]:
            lines.append(f"  - {os.path.relpath(f, PROJECT_ROOT)}")
    else:
        pattern = os.path.join(PROJECT_ROOT, "**", f"*{project}*")
        files = glob.glob(pattern, recursive=True)
        lines.append(f"## Files matching '{project}' ({len(files)})")
        for f in files[:20]:
            lines.append(f"  - {f.replace(PROJECT_ROOT, '.')}")

    # docker
    lines.append("\n## Docker Containers")
    container_name = info.get("container", "")
    if dc:
        found = False
        for c in dc.containers.list(all=True):
            if project in c.name.lower() or (container_name and container_name in c.name):
                found = True
                lines.append(f"- {c.name}: {c.status}")
                if c.status == "running":
                    try:
                        log = c.logs(tail=10).decode(errors="replace")
                        lines += ["```", log[-800:], "```"]
                    except:
                        pass
        if not found:
            lines.append(f"NO container found (expected: {container_name or 'unknown'})")

    # DB tables
    lines.append("\n## Database")
    db_out = await pg_exec(f"\\dt *{project}*")
    lines.append(db_out if "row" in db_out.lower() else f"No tables matching '{project}'")

    # .env
    lines.append("\n## Environment Variables")
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            relevant = [l.split("=")[0].strip() for l in f if project.upper() in l.upper() and "=" in l]
        lines.append(", ".join(relevant) if relevant else "None relevant in .env")

    # summary
    lines += ["", "## Actions Needed"]
    if not os.path.isdir(project_dir):
        lines.append("- [ ] Create project folder")
    if dc and not any(project in c.name.lower() for c in dc.containers.list(all=True)):
        lines.append("- [ ] Create Docker container")
    lines.append("- [ ] Verify DB tables")
    lines.append("- [ ] Run /recover " + project)

    content = "\n".join(lines)
    fname = f"{project.upper()}_REPORT.md"
    fpath = os.path.join(PROJECT_ROOT, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    doc = BufferedInputFile(content.encode("utf-8"), filename=fname)
    await m.answer_document(doc, caption=f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ {project.upper()} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ investigation done")

    global next_task_id
    tid = next_task_id
    tasks[tid] = {
        "agent": "admin", "description": f"Recover {project} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ see {fname}",
        "status": "pending", "created_at": datetime.datetime.now().isoformat(), "created_by": m.from_user.id
    }
    next_task_id += 1
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Task #{tid}: recover {project}")
    await audit(m.from_user.id, "/investigate", "ok", project)

# ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼ /db_query ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ run SQL against PostgreSQL ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼
@dp.message(Command("db_query"))
async def cmd_db_query(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer(
            "Usage: /db_query SQL\n"
            "Examples:\n"
            "/db_query SELECT table_name FROM information_schema.tables WHERE table_schema='public'\n"
            "/db_query \\dt\n"
            "/db_query SELECT count(*) FROM users"
        )
    sql = parts[1].strip().strip('"').strip("'")
    forbidden = ["drop ", "truncate ", "delete from", "alter ", "grant ", "revoke "]
    if any(f in sql.lower() for f in forbidden):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Destructive SQL blocked. Use psql directly for DROP/DELETE/ALTER.")
    await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì Running query...")
    result = await pg_exec(sql)
    if len(result) > 3500:
        doc = BufferedInputFile(result.encode("utf-8"), filename="query_result.txt")
        await m.answer_document(doc, caption="├â┬░├à┬╕├óΓé¼┼ô├à┬á Query result")
    else:
        await m.answer(f"<pre>{result[:3500]}</pre>")
    await audit(m.from_user.id, "/db_query", "ok", sql[:80])

# ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼ /services ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ list known and registered services ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼
@dp.message(Command("services"))
async def cmd_services(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    text = "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬º SLH Services</b>\n\n"
    containers = {c.name: c.status for c in dc.containers.list(all=True)} if dc else {}
    for name, info in sorted(PROJECT_MAP.items()):
        cname = info.get("container", "")
        status = containers.get(cname, "not deployed")
        icon = "├â┬░├à┬╕├à┬╕├é┬ó" if status == "running" else "├â┬░├à┬╕├óΓé¼┬¥├é┬┤" if cname else "├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼í"
        folder_exists = os.path.isdir(os.path.join(PROJECT_ROOT, info.get("folder", "")))
        text += f"{icon} <b>{name}</b>"
        if cname:
            text += f" ({cname}: {status})"
        text += f"\n   Folder: {'├â┬ó├àΓÇ£├óΓé¼┬ª' if folder_exists else '├â┬ó├é┬¥├àΓÇÖ'} {info.get('folder','?')}"
        if info.get("bot"):
            text += f" | Bot: {info['bot']}"
        text += "\n"
    await m.answer(text[:4000])

# ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼ /recover + /recover_project ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ automated recovery for a project ├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼├â┬ó├óΓé¼┬¥├óΓÇÜ┬¼
@dp.message(Command("recover"))
async def cmd_recover(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split()
    if len(parts) < 2:
        known = ", ".join(sorted(PROJECT_MAP.keys()))
        return await m.answer(f"Usage: /recover project_name\nKnown: {known}")
    project = sanitize_name(parts[1]).lower()
    if project not in PROJECT_MAP:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ Unknown project '{project}'. Use /services to see known projects.")
    info = PROJECT_MAP[project]
    results = [f"<b>├â┬░├à┬╕├é┬⌐├é┬║ Recovery: {project.upper()}</b>\n"]

    # Step 1: Check folder
    folder = info.get("folder", project)
    project_dir = os.path.join(PROJECT_ROOT, folder)
    if os.path.isdir(project_dir):
        results.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª Folder exists: {folder}/")
    else:
        results.append(f"├â┬ó├é┬¥├àΓÇÖ Folder missing: {folder}/")

    # Step 2: Check/restart container
    cname = info.get("container")
    if cname and dc:
        try:
            c = dc.containers.get(cname)
            if c.status == "running":
                results.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª Container {cname}: running")
            else:
                results.append(f"├â┬ó├à┬í├é┬á├»┬╕┬Å Container {cname}: {c.status} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ restarting...")
                c.restart(timeout=15)
                await asyncio.sleep(3)
                c.reload()
                results.append(f"{'├â┬ó├àΓÇ£├óΓé¼┬ª' if c.status == 'running' else '├â┬ó├é┬¥├àΓÇÖ'} After restart: {c.status}")
        except Exception as e:
            results.append(f"├â┬ó├é┬¥├àΓÇÖ Container {cname}: {str(e)[:100]}")
    elif cname:
        results.append(f"├â┬ó├é┬¥├àΓÇÖ Docker SDK not available")
    else:
        results.append(f"├â┬ó├óΓé¼┼╛├é┬╣├»┬╕┬Å No container defined for {project}")

    # Step 3: Check DB tables
    db_result = await pg_exec(f"\\dt *{project}*")
    if "row" in db_result.lower():
        results.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª DB tables found for {project}")
    else:
        results.append(f"├â┬ó├à┬í├é┬á├»┬╕┬Å No DB tables for {project}")

    # Step 4: Check .env
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            relevant = [l.split("=")[0].strip() for l in f if project.upper() in l.upper() and "=" in l]
        if relevant:
            results.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª .env vars: {', '.join(relevant[:5])}")
        else:
            results.append(f"├â┬ó├à┬í├é┬á├»┬╕┬Å No .env vars for {project}")

    # Step 5: Create recovery task
    global next_task_id
    tid = next_task_id
    tasks[tid] = {
        "agent": "admin", "description": f"Recovery executed for {project}",
        "status": "completed", "created_at": datetime.datetime.now().isoformat(),
        "completed_at": datetime.datetime.now().isoformat(), "created_by": m.from_user.id
    }
    next_task_id += 1
    results.append(f"\n├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Task #{tid} logged")

    await m.answer("\n".join(results))
    await audit(m.from_user.id, "/recover", "ok", project)

@dp.message(Command("recover_project"))
async def cmd_recover_project(m: types.Message):
    await cmd_recover(m)

@dp.message(Command("handoff"))
async def cmd_handoff(m: types.Message):
    if not is_allowed(m.from_user.id, "manager"):
        return
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    doc_lines = [f"# SLH Handoff ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {ts}", "", "## System Status"]
    if dc:
        containers = dc.containers.list(all=True)
        running = sum(1 for c in containers if c.status == "running")
        doc_lines.append(f"- Docker: {running}/{len(containers)} running")
        for c in sorted(containers, key=lambda x: x.name):
            icon = "+" if c.status == "running" else "-"
            doc_lines.append(f"  {icon} {c.name} ({c.status})")
    bridge = await http_get(f"{LOCAL_BRIDGE}/api/health")
    doc_lines.append(f"- Local Bridge: {'OK' if bridge else 'DOWN'}")
    railway = await http_get(f"{RAILWAY_API}/api/health")
    doc_lines.append(f"- Railway API: {'OK' if railway and railway.get('status') == 'ok' else 'DOWN'}")
    esp = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    if esp and esp.get("devices"):
        for d in esp["devices"]:
            doc_lines.append(f"- ESP32 {d['device_id']}: {d.get('status')} fw={d.get('fw')} ip={d.get('ip')}")
    doc_lines += [
        "", "## Agent Hub",
        f"- Agents: {len(agents)}",
        f"- Tasks: {len(tasks)} ({sum(1 for t in tasks.values() if t['status'] == 'pending')} pending)",
        "", "## Key Paths",
        f"- Project: {PROJECT_ROOT}",
        "- Admin Bot: admin-bot/main.py",
        "- Local Bridge: local_bridge.py (port 8090)",
        "- ESP32 FW: device-registry/esp32-cyd-work/firmware/slh-device-v4/",
        f"- Website: {WEBSITE_PATH}",
        "", "## Quick Commands",
        "- /start ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ full menu",
        "- /health ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ system health",
        "- /morning ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ daily report",
        "- /selftest ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ run all checks",
        "- /guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ complete guide",
        "",
        f"*Generated by SLH Admin Bot v51 at {ts}*",
    ]
    content = "\n".join(doc_lines)
    fpath = os.path.join(PROJECT_ROOT, "handoff.md")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    doc = BufferedInputFile(content.encode("utf-8"), filename="handoff.md")
    await m.answer_document(doc, caption=f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Handoff generated ({len(doc_lines)} lines)")
    await audit(m.from_user.id, "/handoff", "ok")

@dp.message(Command("session_summary"))
async def cmd_session_summary(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    summary = """<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á Session Summary ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 2026-05-07</b>

<b>├â┬ó├àΓÇ£├óΓé¼┬ª Completed:</b>
├â┬ó├óΓÇÜ┬¼├é┬ó Admin Bot v51 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 60+ commands, full ops hub
├â┬ó├óΓÇÜ┬¼├é┬ó ESP32 CYD operational ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ heartbeat, balances, screen control
├â┬ó├óΓÇÜ┬¼├é┬ó Local Bridge (port 8090) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ SQLite API
├â┬ó├óΓÇÜ┬¼├é┬ó Firmware v4 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ dual-path API (local + Railway)
├â┬ó├óΓÇÜ┬¼├é┬ó Firewall rule for port 8090
├â┬ó├óΓÇÜ┬¼├é┬ó Device paired: esp32-14335C6C32C0
├â┬ó├óΓÇÜ┬¼├é┬ó Wallet seeded: SLH 125K, MNH 50K, ZVK 75K
├â┬ó├óΓÇÜ┬¼├é┬ó /backup_db ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Docker SDK + SQL file
├â┬ó├óΓÇÜ┬¼├é┬ó /investigate ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ project recovery scanner
├â┬ó├óΓÇÜ┬¼├é┬ó /repos /files /read_file /commit ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ GitHub restored
├â┬ó├óΓÇÜ┬¼├é┬ó /scan /heal ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ deep Docker ops restored
├â┬ó├óΓÇÜ┬¼├é┬ó /bots ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ full 21-bot directory
├â┬ó├óΓÇÜ┬¼├é┬ó /read_local /find_files ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ local file ops

<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32:</b>
├â┬ó├óΓÇÜ┬¼├é┬ó MAC: 14:33:5C:6C:32:C0 | IP: 10.0.0.4
├â┬ó├óΓÇÜ┬¼├é┬ó FW: slh-v4 | Screens: HOME, WALLET, BOTS, SYS, PAIR
├â┬ó├óΓÇÜ┬¼├é┬ó Heartbeat: 30s | Balances: 60s | Commands: 15s"""
    await m.answer(summary)

@dp.message(Command("dev_roadmap"))
async def cmd_dev_roadmap(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    roadmap = """<b>├â┬░├à┬╕├óΓé¼ΓÇ¥├é┬║ SLH Development Roadmap</b>

<b>├â┬░├à┬╕├óΓé¼┼ô├é┬▒ ESP32 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Immediate:</b>
1. Touch calibration firmware
2. Battery: 3.7V LiPo via TP4056
3. Case: 3D print for CYD

<b>├â┬░├à┬╕├óΓé¼┼ô├é┬▒ ESP32 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Multi-Device (5 units):</b>
1. Unique device_id per MAC
2. QR pairing flow
3. Token trading between devices
4. Transaction ledger in PostgreSQL
5. QR-to-QR transfer

<b>├â┬░├à┬╕├àΓÇÖ├é┬É Website:</b>
1. Bug fixes across pages
2. 109 pages CSS migration
3. Control center to GitHub Pages

<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ Bot Platform:</b>
1. PostgreSQL persistence for agents/tasks
2. Manager assignments (Zvika, Eliezer)
3. Multi-project scoping

<b>├â┬░├à┬╕├óΓé¼Γäó├é┬░ Trading System:</b>
1. P2P token transfer
2. Transaction ledger + signatures
3. Balance sync
4. QR payment flow

<b>├â┬░├à┬╕├óΓé¼┬¥├é┬º Infrastructure:</b>
1. Railway API verification
2. Local bridge as Windows service
3. Webhook migration
4. Guardian bot fix"""
    await m.answer(roadmap)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  14. BROADCAST & OPS GUIDE                           ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥
@dp.message(Command("broadcast"))
async def cmd_broadcast(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await m.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer(
            "Usage: /broadcast message\n\n"
            "Sends to all registered admins/managers.\n"
            "Example: /broadcast System maintenance in 30 min"
        )
    msg = parts[1]
    perms = load_permissions()
    sent = 0
    failed = 0
    for uid_str in perms:
        try:
            uid = int(uid_str)
            await bot.send_message(uid, f"├â┬░├à┬╕├óΓé¼┼ô├é┬ó <b>SLH Broadcast</b>\n\n{msg}")
            sent += 1
        except Exception:
            failed += 1
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª Broadcast sent: {sent} delivered, {failed} failed")
    await audit(m.from_user.id, "/broadcast", "ok", f"sent={sent}")

@dp.message(Command("ops_guide"))
async def cmd_ops_guide(m: types.Message):
    if not is_allowed(m.from_user.id, "viewer"):
        return
    guide = """<b>├â┬░├à┬╕├óΓé¼┼ô├ï┼ô SLH Operations Guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├ù┬¬├ù┬ñ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£</b>
├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü

<b>├â┬ó├ï┼ô├óΓÇÜ┬¼├»┬╕┬Å ├ù┬⌐├âΓÇö├óΓé¼Γäó├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿:</b>
1. /morning ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É
2. /health ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥
3. /task_status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬

<b>├â┬░├à┬╕├óΓé¼┬¥├é┬ì ├âΓÇö├óΓé¼ΓÇ¥├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô:</b>
1. /investigate nfty ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥ (├ù┬º├âΓÇö├óΓé¼╦£├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¥, Docker, DB, env)
2. /recover nfty ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¿ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó (restart + validation)
3. /services ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ñ├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥ + ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓé¼╦£

<b>├â┬░├à┬╕├é┬É├é┬│ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ Docker:</b>
1. /status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥
2. /scan ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥ (image, ports, restarts)
3. /heal ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó (restart stopped)
4. /logs container [lines] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬¥
5. /restart container ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐

<b>├â┬░├à┬╕├óΓé¼Γäó├é┬╛ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬:</b>
1. /backup_db ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó PostgreSQL ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬Ñ SQL
2. /report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬
3. /selftest ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ó├ù┬ª├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬
4. /handoff ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬╛├âΓÇö├à┬í ├âΓÇö├à┬╛├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É

<b>├â┬░├à┬╕├óΓé¼ΓÇ¥├óΓé¼┼╛ ├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├ù┬ó├ù┬¥ DB:</b>
1. /db_query \\dt ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├ù┬¬ ├âΓÇö├ï┼ô├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬
2. /db_query SELECT count(*) FROM users ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├ù┬¬├âΓÇö├óΓé¼┬¥
3. /init_db ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├ï┼ô├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼╦£├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬í

<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>
1. /register_agent name role ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥
2. /dispatch_task agent "description" ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥
3. /task_status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ó├ù┬º├âΓÇö├óΓé¼╦£
4. /complete_task id ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥
5. /publish_summary ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥

<b>├â┬░├à┬╕├óΓé¼┼ô├é┬í ESP32:</b>
1. /esp ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓé¼╦£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥
2. /esp_screen HOME ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£├ù┬ñ├ù┬¬ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í
3. /esp_reboot ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬É├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£

<b>├â┬░├à┬╕├óΓé¼┼ô├à┬í GitHub:</b>
1. /repos ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥
2. /files repo path ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼╦£├ù┬º├âΓÇö├óΓé¼╦£├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¥
3. /read_file repo file ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥
4. /commit repo "message" ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ commit

<b>├â┬░├à┬╕├óΓé¼┼ô├é┬ó ├ù┬¬├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¿├ù┬¬:</b>
1. /broadcast message ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥
2. /post_update message ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ñ├ù┬¿├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥ ├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕

<b>├â┬░├à┬╕├óΓé¼╦£├é┬Ñ ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ (RBAC v2):</b>
1. /add_admin user_id name [role] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ñ├ù┬¬ ├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£
2. /remove_admin user_id ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬í├ù┬¿├âΓÇö├óΓé¼┬¥
3. /admins ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥
4. /grant user_id command ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬¬├âΓÇö├à┬╕ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├ù┬í├ù┬ñ├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó├ù┬¬
5. /revoke user_id command ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬í├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥
6. /requests ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬
7. /permissions [user_id] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬

<b>├â┬░├à┬╕├óΓé¼┬¥├é┬É ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬:</b>
├â┬ó├óΓÇÜ┬¼├é┬ó none ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐ (├ù┬¿├ù┬º /start, /create_me)
├â┬ó├óΓÇÜ┬¼├é┬ó viewer ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ (status, logs, repos, health...)
├â┬ó├óΓÇÜ┬¼├é┬ó manager ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ (restart, scan, heal, agents...)
├â┬ó├óΓÇÜ┬¼├é┬ó owner ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥ (rebuild, deploy, db_query...)
├â┬ó├óΓÇÜ┬¼├é┬ó ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬¿ "├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥"
├â┬ó├óΓÇÜ┬¼├é┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬¬├ù┬¿├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├âΓÇö├àΓÇ£├ù┬É├ù┬⌐├ù┬¿/├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬/├âΓÇö├àΓÇ£├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥

<b>├â┬ó├à┬í├é┬á├»┬╕┬Å ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥:</b>
├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô ├âΓÇö├à┬╛├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£ <b>├ù┬¿├ù┬º</b> ├âΓÇö├àΓÇ£├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼╦£├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¬.
├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ (NIFTII, SLH_AIR) ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├óΓÇ₧┬ó├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó ├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓé¼┬ó.
├âΓÇö├óΓé¼╦£├ù┬ª'├ù┬É├âΓÇö├ï┼ô ├ù┬ñ├ù┬¿├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├ù┬¬.

<b>├â┬░├à┬╕├óΓé¼┬¥├óΓé¼ΓÇ¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>
├â┬ó├óΓÇÜ┬¼├é┬ó Admin: slh-nft.com/admin.html?unlock
├â┬ó├óΓÇÜ┬¼├é┬ó API: slh-api-production.up.railway.app/docs
├â┬ó├óΓÇÜ┬¼├é┬ó Control: slh-nft.com/control-center.html"""
    if len(guide) > 4000:
        doc = BufferedInputFile(guide.encode("utf-8"), filename="ops_guide.txt")
        await m.answer_document(doc, caption="├â┬░├à┬╕├óΓé¼┼ô├ï┼ô SLH Operations Guide")
    else:
        await m.answer(guide)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  15. ACCESS REQUEST & GRANULAR PERMISSIONS           ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

# -- Callback: user clicks "Request Access" button --
@dp.callback_query(lambda c: c.data and c.data.startswith("reqaccess_"))
async def cb_request_access(cq: CallbackQuery):
    parts = cq.data.split("_", 2)
    if len(parts) < 3:
        return await cq.answer("├â┬ó├é┬¥├àΓÇÖ Invalid request")
    cmd = parts[1]
    uid = cq.from_user.id
    name = cq.from_user.full_name or str(uid)
    username = cq.from_user.username or ""
    if not dc:
        return await cq.answer("├â┬ó├é┬¥├àΓÇÖ DB unavailable")
    try:
        pg = dc.containers.get("slh-postgres")
        existing = pg.exec_run([
            "psql", "-U", "postgres", "-d", "slh_main", "-t", "-A", "-c",
            f"SELECT count(*) FROM access_requests WHERE user_id={uid} AND command='{cmd}' AND status='pending'"
        ])
        if existing.output.decode().strip() != "0":
            return await cq.answer("├ó┬Å┬│ ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├ù┬¿ ├âΓÇö├óΓÇ₧┬ó├ù┬⌐ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó", show_alert=True)
        pg.exec_run([
            "psql", "-U", "postgres", "-d", "slh_main", "-c",
            f"INSERT INTO access_requests (user_id, user_name, command) VALUES ({uid}, '{name.replace(chr(39), '')}', '{cmd}')"
        ])
    except Exception as e:
        return await cq.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:50]}")
    await cq.answer("├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬á├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£!", show_alert=True)
    await cq.message.edit_text(
        f"├â┬░├à┬╕├óΓé¼┼ô├é┬⌐ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-<code>/{cmd}</code> ├ù┬á├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥.\n├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ ├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬¬├ù┬¿├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├àΓÇ£├ù┬É├ù┬⌐├ù┬¿ ├ù┬É├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬É├ù┬⌐├ù┬¿", callback_data=f"approve_{cmd}_{uid}"),
            InlineKeyboardButton(text="├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥", callback_data=f"reject_{cmd}_{uid}"),
        ],
        [InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥", callback_data=f"msg_{cmd}_{uid}")]
    ])
    ulink = f"@{username}" if username else name
    await bot.send_message(
        OWNER_ID,
        f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┬¥ <b>├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥</b>\n\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐: {ulink} (<code>{uid}</code>)\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥: <code>/{cmd}</code>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô ├ù┬á├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó: {get_user_role(uid)}\n"
        f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼╦£ ├ù┬á├âΓÇö├óΓé¼┼ô├ù┬¿├ù┬⌐: {COMMAND_ROLES.get(cmd, 'owner')}\n\n"
        f"├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼ΓÇ¥├ù┬¿ ├ù┬ñ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥:", reply_markup=kb
    )

# -- Callback: owner approves access --
@dp.callback_query(lambda c: c.data and c.data.startswith("approve_"))
async def cb_approve_access(cq: CallbackQuery):
    if cq.from_user.id != OWNER_ID:
        return await cq.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = cq.data.split("_", 2)
    cmd, target_uid = parts[1], int(parts[2])
    if not dc:
        return await cq.answer("├â┬ó├é┬¥├àΓÇÖ DB unavailable")
    try:
        pg = dc.containers.get("slh-postgres")
        pg.exec_run([
            "psql", "-U", "postgres", "-d", "slh_main", "-c",
            f"INSERT INTO command_permissions (user_id, command, granted_by) "
            f"VALUES ({target_uid}, '{cmd}', {OWNER_ID}) ON CONFLICT (user_id, command) DO NOTHING"
        ])
        pg.exec_run([
            "psql", "-U", "postgres", "-d", "slh_main", "-c",
            f"UPDATE access_requests SET status='approved', resolved_at=NOW(), resolved_by={OWNER_ID} "
            f"WHERE user_id={target_uid} AND command='{cmd}' AND status='pending'"
        ])
    except Exception as e:
        return await cq.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:50]}")
    await cq.answer("├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬É├âΓÇö├óΓé¼┬ó├ù┬⌐├ù┬¿")
    await cq.message.edit_text(
        cq.message.text + f"\n\n├â┬ó├àΓÇ£├óΓé¼┬ª <b>├ù┬É├âΓÇö├óΓé¼┬ó├ù┬⌐├ù┬¿</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {target_uid} ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-/{cmd}"
    )
    try:
        await bot.send_message(target_uid, f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├àΓÇ£-<code>/{cmd}</code> <b>├ù┬É├âΓÇö├óΓé¼┬ó├ù┬⌐├ù┬¿├âΓÇö├óΓé¼┬¥!</b>\n├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼╦£├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ó├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó.")
    except:
        pass
    await audit(OWNER_ID, "/approve", "ok", f"user={target_uid} cmd={cmd}")

# -- Callback: owner rejects access --
@dp.callback_query(lambda c: c.data and c.data.startswith("reject_"))
async def cb_reject_access(cq: CallbackQuery):
    if cq.from_user.id != OWNER_ID:
        return await cq.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = cq.data.split("_", 2)
    cmd, target_uid = parts[1], int(parts[2])
    if dc:
        try:
            pg = dc.containers.get("slh-postgres")
            pg.exec_run([
                "psql", "-U", "postgres", "-d", "slh_main", "-c",
                f"UPDATE access_requests SET status='rejected', resolved_at=NOW(), resolved_by={OWNER_ID} "
                f"WHERE user_id={target_uid} AND command='{cmd}' AND status='pending'"
            ])
        except:
            pass
    await cq.answer("├â┬ó├é┬¥├àΓÇÖ ├ù┬á├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥")
    await cq.message.edit_text(
        cq.message.text + f"\n\n├â┬ó├é┬¥├àΓÇÖ <b>├ù┬á├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {target_uid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-/{cmd}"
    )
    try:
        await bot.send_message(target_uid, f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├àΓÇ£-<code>/{cmd}</code> <b>├ù┬á├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├ù┬¬├âΓÇö├óΓé¼┬¥.</b>")
    except:
        pass
    await audit(OWNER_ID, "/reject", "ok", f"user={target_uid} cmd={cmd}")

# -- Callback: owner wants to send message to requester --

@dp.callback_query(lambda c: c.data and c.data.startswith("msg_"))
async def cb_msg_requester(cq: CallbackQuery):
    if cq.from_user.id != OWNER_ID:
        return await cq.answer("├â┬ó├óΓé¼┬║├óΓé¼┬¥ Owner only")
    parts = cq.data.split("_", 2)
    cmd, target_uid = parts[1], int(parts[2])
    _pending_messages[OWNER_ID] = {"target_uid": int(target_uid), "cmd": cmd}
    await cq.answer("├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├âΓÇö├óΓé¼┬║├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó")
    await cq.message.answer(
        f"├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├âΓÇö├óΓé¼┬║├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ <code>{target_uid}</code> (├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├ù┬¿ ├âΓÇö├àΓÇ£-/{cmd}).\n"
        f"├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬É├âΓÇö├óΓé¼┬¥ ├ù┬⌐├ù┬¬├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬ó├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó."
    )

# -- /grant user_id command ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ grant per-command access --
@dp.message(Command("grant"))
async def cmd_grant(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await deny_with_request(m, "grant")
    parts = m.text.split()
    if len(parts) < 3:
        return await m.answer("Usage: /grant user_id command\nExample: /grant 123456 restart")
    target_uid, cmd = parts[1], parts[2].lower().lstrip("/")
    if not dc:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ DB unavailable")
    try:
        pg = dc.containers.get("slh-postgres")
        pg.exec_run([
            "psql", "-U", "postgres", "-d", "slh_main", "-c",
            f"INSERT INTO command_permissions (user_id, command, granted_by) "
            f"VALUES ({int(target_uid)}, '{cmd}', {m.from_user.id}) ON CONFLICT (user_id, command) DO NOTHING"
        ])
    except Exception as e:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")
    await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-<code>/{cmd}</code> ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ <code>{target_uid}</code>")
    try:
        await bot.send_message(int(target_uid), f"├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-<code>/{cmd}</code>!")
    except:
        pass
    await audit(m.from_user.id, "/grant", "ok", f"user={target_uid} cmd={cmd}")

# -- /revoke user_id command ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ remove per-command access --
@dp.message(Command("revoke"))
async def cmd_revoke(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await deny_with_request(m, "revoke")
    parts = m.text.split()
    if len(parts) < 3:
        return await m.answer("Usage: /revoke user_id command\nExample: /revoke 123456 restart")
    target_uid, cmd = parts[1], parts[2].lower().lstrip("/")
    if dc:
        try:
            pg = dc.containers.get("slh-postgres")
            pg.exec_run([
                "psql", "-U", "postgres", "-d", "slh_main", "-c",
                f"DELETE FROM command_permissions WHERE user_id={int(target_uid)} AND command='{cmd}'"
            ])
        except Exception as e:
            return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")
    await m.answer(f"├â┬░├à┬╕├à┬í├é┬½ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-<code>/{cmd}</code> ├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ <code>{target_uid}</code>")
    try:
        await bot.send_message(int(target_uid), f"├â┬░├à┬╕├à┬í├é┬½ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├àΓÇ£-<code>/{cmd}</code> ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬¿├âΓÇö├óΓé¼┬¥.")
    except:
        pass
    await audit(m.from_user.id, "/revoke", "ok", f"user={target_uid} cmd={cmd}")

# -- /requests ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ view pending access requests --
@dp.message(Command("requests"))
async def cmd_requests(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await deny_with_request(m, "requests")
    if not dc:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ DB unavailable")
    try:
        pg = dc.containers.get("slh-postgres")
        result = pg.exec_run([
            "psql", "-U", "postgres", "-d", "slh_main", "-t", "-A", "-c",
            "SELECT id, user_id, user_name, command, status, created_at::text FROM access_requests ORDER BY created_at DESC LIMIT 20"
        ])
        rows = result.output.decode(errors="replace").strip()
    except Exception as e:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")
    if not rows:
        return await m.answer("├â┬░├à┬╕├óΓé¼┼ô├é┬¡ ├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥.")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ (20 ├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬)</b>\n\n"
    for line in rows.split("\n"):
        cols = line.split("|")
        if len(cols) < 6:
            continue
        rid, uid, uname, cmd, status, ts = cols[0], cols[1], cols[2], cols[3], cols[4], cols[5][:16]
        icon = {"pending": "├â┬░├à┬╕├à┬╕├é┬í", "approved": "├â┬ó├àΓÇ£├óΓé¼┬ª", "rejected": "├â┬ó├é┬¥├àΓÇÖ"}.get(status, "├â┬ó├é┬¥├óΓé¼┼ô")
        text += f"{icon} #{rid} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {uname} (<code>{uid}</code>)\n   /{cmd} | {status} | {ts}\n"
        if status == "pending":
            text += f"   ├â┬ó├óΓé¼┬á├óΓé¼Γäó /grant {uid} {cmd} | ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬: /reject_req {rid}\n"
    await m.answer(text[:4000])

# -- /permissions [user_id] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ show user's permissions --
@dp.message(Command("permissions"))
async def cmd_permissions(m: types.Message):
    if not is_allowed(m.from_user.id, "owner"):
        return await deny_with_request(m, "permissions")
    parts = m.text.split()
    if len(parts) >= 2:
        target_uid = parts[1]
    else:
        target_uid = None
    text = ""
    if target_uid:
        role = get_user_role(int(target_uid))
        text = f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬É ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ {target_uid}</b>\n\n"
        text += f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô: <b>{role}</b>\n\n"
        text += f"<b>├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├àΓÇ£├ù┬ñ├âΓÇö├óΓÇ₧┬ó ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô ({role}):</b>\n"
        for cmd, req in sorted(COMMAND_ROLES.items()):
            if ROLE_LEVELS.get(role, 0) >= ROLE_LEVELS.get(req, 0):
                text += f"  ├â┬ó├àΓÇ£├óΓé¼┬ª /{cmd}\n"
        if dc:
            try:
                pg = dc.containers.get("slh-postgres")
                result = pg.exec_run([
                    "psql", "-U", "postgres", "-d", "slh_main", "-t", "-A", "-c",
                    f"SELECT command FROM command_permissions WHERE user_id={int(target_uid)}"
                ])
                extra = result.output.decode().strip()
                if extra:
                    text += f"\n<b>├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ñ├ù┬¬ (per-command):</b>\n"
                    for c in extra.split("\n"):
                        text += f"  ├â┬░├à┬╕├óΓé¼┬¥├óΓé¼╦£ /{c.strip()}\n"
            except:
                pass
    else:
        text = "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬É ├ù┬í├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¬</b>\n\n"
        perms = load_permissions()
        for uid, data in perms.items():
            text += f"├â┬ó├óΓÇÜ┬¼├é┬ó {data['name']} (<code>{uid}</code>) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ <b>{data['role']}</b>\n"
        text += f"\n├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬í├âΓÇö├óΓé¼┬¥\"├âΓÇö├óΓé¼┬║ {len(COMMAND_ROLES)} ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        text += f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼ô viewer: {sum(1 for v in COMMAND_ROLES.values() if v == 'viewer')}\n"
        text += f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼Γäó manager: {sum(1 for v in COMMAND_ROLES.values() if v == 'manager')}\n"
        text += f"├â┬░├à┬╕├óΓé¼┬¥├é┬É owner: {sum(1 for v in COMMAND_ROLES.values() if v == 'owner')}\n"
        text += f"\nUsage: /permissions user_id ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ª├âΓÇö├óΓé¼Γäó ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├ù┬í├ù┬ñ├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó"
    if len(text) > 4000:
        doc = BufferedInputFile(text.encode("utf-8"), filename="permissions.txt")
        await m.answer_document(doc, caption="├â┬░├à┬╕├óΓé¼┬¥├é┬É Permissions")
    else:
        await m.answer(text)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  16. ABAC MANAGEMENT COMMANDS                        ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

@dp.message(Command("user_attrs"))
async def cmd_user_attrs(m: types.Message):
    parts = m.text.split()
    target = int(parts[1]) if len(parts) >= 2 else m.from_user.id
    ua = await get_user_attrs(target)
    if not ua:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ {target} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É ├âΓÇö├óΓé¼╦£-ABAC.\n├âΓÇö├óΓÇ₧┬ó├ù┬⌐ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬⌐├ù┬¥ ├ù┬ó├ù┬¥ /create_me")
    risk_icons = "├â┬░├à┬╕├à┬╕├é┬ó├â┬░├à┬╕├à┬╕├é┬í├â┬░├à┬╕├à┬╕├é┬á├â┬░├à┬╕├óΓé¼┬¥├é┬┤├â┬░├à┬╕├óΓé¼┬¥├é┬Ñ"
    spec = ua.get("specialization", "") or "├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥"
    await m.answer(
        f"<b>├â┬░├à┬╕├óΓé¼╦£├é┬ñ ABAC Profile ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {ua.get('full_name', '?')}</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├óΓé¼┬á├óΓé¼┬¥ ID: <code>{ua['user_id']}</code>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬║ Username: @{ua.get('username', '├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥')}\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô: <b>{ua.get('role', 'none')}</b>\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬Ñ ├ù┬ª├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬ó├ù┬¬: <b>{ua.get('team', 'general')}</b>\n"
        f"├ó┬¡┬É ├ù┬É├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕: <b>{ua.get('trust_level', 0)}/10</b>\n"
        f"├â┬░├à┬╕├à┬╜├é┬» ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬: {spec}\n"
        f"├ó┬Å┬░ ├ù┬⌐├ù┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬: {ua.get('active_hours', '0-24')}\n"
        f"├â┬░├à┬╕├óΓé¼Γäó├é┬ú ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├ù┬º├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó: {risk_icons[min(ua.get('max_risk',1),5)-1]} <b>{ua.get('max_risk',1)}/5</b>\n"
        f"├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£: {'├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕' if ua.get('is_active') else '├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├àΓÇ£├ù┬É'}\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬: {ua.get('notes', '') or '├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥'}\n\n"
        f"<b>├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó:</b> /user_set {target} &lt;attr&gt; &lt;value&gt;\n"
        f"<i>attrs: role, team, trust, max_risk, spec, hours, active, notes</i>"
    )

@dp.message(Command("user_set"))
async def cmd_user_set(m: types.Message):
    parts = m.text.split(maxsplit=3)
    if len(parts) < 4:
        return await m.answer(
            "<b>Usage:</b> /user_set &lt;user_id&gt; &lt;attr&gt; &lt;value&gt;\n\n"
            "<b>Attributes:</b>\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó role ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ none/viewer/manager/owner\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó team ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ general/dev/ops/debug/admin/support\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó trust ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 0-10\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó max_risk ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 1-5\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó spec ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ (docker,git,esp,db,deploy)\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó hours ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├ù┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ (8-22 / 0-24)\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó active ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ true/false\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó notes ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬ñ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬"
        )
    target, attr, val = int(parts[1]), parts[2].lower(), parts[3]
    col_map = {
        "role": ("role", val), "team": ("team", val),
        "trust": ("trust_level", int(val)), "max_risk": ("max_risk", int(val)),
        "spec": ("specialization", val), "hours": ("active_hours", val),
        "active": ("is_active", val.lower() in ("true", "1", "yes", "├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕")),
        "notes": ("notes", val),
    }
    if attr not in col_map:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬¿├ù┬¬: {attr}\n├ù┬É├ù┬ñ├ù┬⌐├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬: {', '.join(col_map.keys())}")
    col, typed_val = col_map[attr]
    if isinstance(typed_val, bool):
        sql_val = "true" if typed_val else "false"
    elif isinstance(typed_val, int):
        sql_val = str(typed_val)
    else:
        sql_val = f"'{typed_val.replace(chr(39), '')}'"
    ok = await _pg_ok(
        f"UPDATE abac_users SET {col}={sql_val}, updated_at=NOW() WHERE user_id={target}"
    )
    if attr == "role":
        perms = load_permissions()
        if str(target) in perms:
            perms[str(target)]["role"] = val
            save_permissions(perms)
    invalidate_cache(uid=target)
    if ok:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ <code>{col}={typed_val}</code> ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ <code>{target}</code>")
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ ├ù┬⌐├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├àΓÇ£├ù┬É ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼╦£-abac_users")
    await audit(m.from_user.id, "/user_set", "ok", f"{target}.{col}={typed_val}")

@dp.message(Command("cmd_info"))
async def cmd_cmd_info(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /cmd_info &lt;command&gt;")
    cmd = parts[1].lower().lstrip("/")
    ca = await get_cmd_attrs(cmd)
    risk_icons = "├â┬░├à┬╕├à┬╕├é┬ó├â┬░├à┬╕├à┬╕├é┬í├â┬░├à┬╕├à┬╕├é┬á├â┬░├à┬╕├óΓé¼┬¥├é┬┤├â┬░├à┬╕├óΓé¼┬¥├é┬Ñ"
    ri = min(ca.get("risk_level", 1), 5) - 1
    await m.answer(
        f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ Command Attributes ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ /{cmd}</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┼í ├ù┬º├âΓÇö├ï┼ô├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥: <b>{ca.get('category','?')}</b>\n"
        f"├â┬░├à┬╕├óΓé¼Γäó├é┬ú ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕: {risk_icons[ri]} <b>{ca.get('risk_level','?')}/5</b>\n"
        f"├ó┬¡┬É ├ù┬É├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├ù┬á├âΓÇö├óΓé¼┼ô├ù┬¿├ù┬⌐: <b>{ca.get('min_trust', 0)}</b>\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬Ñ ├ù┬ª├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥: <b>{ca.get('allowed_teams', '*')}</b>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô ├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó: <b>{ca.get('min_role', 'owner')}</b>\n"
        f"├â┬ó├à┬í├é┬á├»┬╕┬Å ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¿├ù┬⌐ ├ù┬É├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¿: {'├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕' if ca.get('requires_confirmation') else '├âΓÇö├àΓÇ£├ù┬É'}\n"
        f"├ó┬Å┬▒ cooldown: {ca.get('cooldown_seconds', 0)}s\n\n"
        f"<b>├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó:</b> /cmd_set {cmd} &lt;attr&gt; &lt;value&gt;"
    )

@dp.message(Command("cmd_set"))
async def cmd_cmd_set(m: types.Message):
    parts = m.text.split(maxsplit=3)
    if len(parts) < 4:
        return await m.answer(
            "<b>Usage:</b> /cmd_set &lt;command&gt; &lt;attr&gt; &lt;value&gt;\n\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó category ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ general/monitor/infra/deploy/git/agent/admin/esp/data\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó risk ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 1-5\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó trust ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ min trust level (0-10)\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó teams ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ allowed teams (* for all, or dev,ops,debug)\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó role ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ min_role (none/viewer/manager/owner)\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó confirm ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ true/false\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó cooldown ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ seconds"
        )
    cmd, attr, val = parts[1].lower().lstrip("/"), parts[2].lower(), parts[3]
    col_map = {
        "category": ("category", f"'{val}'"), "risk": ("risk_level", val),
        "trust": ("min_trust", val), "teams": ("allowed_teams", f"'{val}'"),
        "role": ("min_role", f"'{val}'"),
        "confirm": ("requires_confirmation", val.lower() in ("true", "1")),
        "cooldown": ("cooldown_seconds", val),
    }
    if attr not in col_map:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬¿├ù┬¬: {attr}")
    col, sql_val = col_map[attr]
    if isinstance(sql_val, bool):
        sql_val = "true" if sql_val else "false"
    ok = await _pg_ok(f"UPDATE command_attrs SET {col}={sql_val} WHERE command='{_safe_cmd(cmd)}'")
    invalidate_cache(cmd=cmd)
    if ok:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ /{cmd}: <code>{col}={val}</code>")
    else:
        await m.answer("├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕")
    await audit(m.from_user.id, "/cmd_set", "ok", f"{cmd}.{col}={val}")

@dp.message(Command("policy_add"))
async def cmd_policy_add(m: types.Message):
    parts = m.text.split(maxsplit=3)
    if len(parts) < 4:
        return await m.answer(
            "<b>Usage:</b> /policy_add &lt;name&gt; &lt;effect&gt; &lt;conditions_json&gt;\n\n"
            "<b>Examples:</b>\n"
            '<code>/policy_add debug_monitor allow {"user.team":"debug","cmd.category":"monitor"}</code>\n'
            '<code>/policy_add night_block deny {"env.hour":{"gte":23}}</code>\n'
            '<code>/policy_add trusted_infra allow {"user.trust_level":{"gte":5},"cmd.category":"infra"}</code>\n\n'
            "<b>Condition operators:</b> eq, neq, gte, lte, gt, lt, in, contains\n"
            "<b>Prefixes:</b> user.*, cmd.*, env.hour/weekday/is_weekend"
        )
    name, effect, conds_str = parts[1], parts[2].lower(), parts[3]
    if effect not in ("allow", "deny"):
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ effect ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ allow ├ù┬É├âΓÇö├óΓé¼┬ó deny")
    try:
        conds = json.loads(conds_str)
    except json.JSONDecodeError as e:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ JSON ├âΓÇö├àΓÇ£├ù┬É ├ù┬¬├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕: {e}")
    conds_escaped = json.dumps(conds).replace("'", "''")
    ok = await _pg_ok(
        f"INSERT INTO abac_policies (name,conditions,effect,created_by) "
        f"VALUES ('{name}','{conds_escaped}','{effect}',{m.from_user.id})"
    )
    invalidate_cache()
    if ok:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ <b>{name}</b> ({effect}) ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬¥├ù┬ª├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥")
    else:
        await m.answer("├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬")
    await audit(m.from_user.id, "/policy_add", "ok", f"{name}:{effect}")

@dp.message(Command("policy_list"))
async def cmd_policy_list(m: types.Message):
    rows = await _pg_val(
        "SELECT id,name,priority,effect,is_active,conditions::text FROM abac_policies ORDER BY priority DESC"
    )
    if not rows:
        return await m.answer("├â┬░├à┬╕├óΓé¼┼ô├é┬¡ ├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ABAC ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┼ô├ù┬¿├ù┬¬.\n├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ú ├ù┬ó├ù┬¥ /policy_add")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├àΓÇ£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ABAC</b>\n├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
    for line in rows.split("\n"):
        p = line.split("|")
        if len(p) >= 6:
            active = "├â┬ó├àΓÇ£├óΓé¼┬ª" if p[4] == "t" else "├ó┬Å┬╕"
            text += (
                f"{active} <b>#{p[0]} {p[1]}</b> ({p[3]})\n"
                f"   Priority: {p[2]} | <code>{p[5][:80]}</code>\n\n"
            )
    text += "<i>/policy_toggle ID ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£/├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬¥\n/policy_del ID ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥</i>"
    if len(text) > 4000:
        doc = BufferedInputFile(text.encode("utf-8"), filename="policies.txt")
        await m.answer_document(doc, caption="├â┬░├à┬╕├óΓé¼┼ô├àΓÇ£ ABAC Policies")
    else:
        await m.answer(text)

@dp.message(Command("policy_del"))
async def cmd_policy_del(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /policy_del &lt;id&gt;")
    ok = await _pg_ok(f"DELETE FROM abac_policies WHERE id={int(parts[1])}")
    invalidate_cache()
    await m.answer(f"{'├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬á├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├ù┬º├âΓÇö├óΓé¼┬¥' if ok else '├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥'}")
    await audit(m.from_user.id, "/policy_del", "ok", parts[1])

@dp.message(Command("policy_toggle"))
async def cmd_policy_toggle(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /policy_toggle &lt;id&gt;")
    ok = await _pg_ok(
        f"UPDATE abac_policies SET is_active = NOT is_active WHERE id={int(parts[1])}"
    )
    invalidate_cache()
    await m.answer(f"{'├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓé¼┬¥' if ok else '├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥'}")
    await audit(m.from_user.id, "/policy_toggle", "ok", parts[1])

@dp.message(Command("abac_status"))
async def cmd_abac_status(m: types.Message):
    users_count = await _pg_val("SELECT count(*) FROM abac_users")
    cmds_count = await _pg_val("SELECT count(*) FROM command_attrs")
    policies_count = await _pg_val("SELECT count(*) FROM abac_policies WHERE is_active=true")
    grants_count = await _pg_val("SELECT count(*) FROM command_permissions")
    pending_count = await _pg_val("SELECT count(*) FROM access_requests WHERE status='pending'")
    teams = await _pg_val("SELECT DISTINCT team FROM abac_users")
    await m.answer(
        f"<b>├â┬░├à┬╕├óΓé¼┬║├é┬í ABAC System Status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ v52</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬¥: <b>{users_count or 0}</b>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬: <b>{cmds_count or 0}</b> / {len(COMMAND_DEFAULTS)}\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├àΓÇ£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥: <b>{policies_count or 0}</b>\n"
        f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼╦£ ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬: <b>{grants_count or 0}</b>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├é┬⌐ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬: <b>{pending_count or 0}</b>\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬Ñ ├ù┬ª├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥: {teams or '├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥'}\n\n"
        f"<b>ABAC Evaluation Order:</b>\n"
        f"1├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Owner bypass\n"
        f"2├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Active hours check\n"
        f"3├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Policy rules (priority-ordered)\n"
        f"4├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Team restriction\n"
        f"5├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Trust level check\n"
        f"6├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Risk level check\n"
        f"7├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Role-based fallback\n"
        f"8├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú Direct command grants\n\n"
        f"<b>├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£:</b>\n"
        f"/user_attrs [uid] ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐\n"
        f"/user_set uid attr val ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥\n"
        f"/cmd_info cmd ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¬├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥\n"
        f"/cmd_set cmd attr val ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥\n"
        f"/policy_add ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ñ├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        f"/policy_list ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        f"/policy_toggle id ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥/├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó\n"
        f"/policy_del id ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬¥"
    )

@dp.message(Command("my_access"))
async def cmd_my_access(m: types.Message):
    uid = m.from_user.id
    ua = await get_user_attrs(uid)
    if not ua:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├àΓÇ£├ù┬É ├ù┬¿├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥. ├âΓÇö├óΓé¼┬¥├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼╦£-/create_me")
    allowed = []
    denied = []
    for cmd in sorted(COMMAND_DEFAULTS.keys()):
        effect, reason = await abac_check(uid, cmd)
        if effect == "allow":
            allowed.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª /{cmd}")
        else:
            denied.append(f"├â┬ó├óΓé¼┬║├óΓé¼┬¥ /{cmd} ({reason})")
    text = (
        f"<b>├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼ô ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {ua.get('full_name', '?')}</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├ù┬ñ├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô: {ua.get('role')} | ├ù┬ª├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬ó├ù┬¬: {ua.get('team')} | ├ù┬É├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕: {ua.get('trust_level')}\n\n"
        f"<b>├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ({len(allowed)}):</b>\n"
        + "\n".join(allowed[:50]) + "\n\n"
        f"<b>├â┬ó├óΓé¼┬║├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬ ({len(denied)}):</b>\n"
        + "\n".join(denied[:30])
    )
    if len(text) > 4000:
        doc = BufferedInputFile(text.encode("utf-8"), filename="my_access.txt")
        await m.answer_document(doc, caption="├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼ô My Access")
    else:
        await m.answer(text)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  17. TASK BOARD ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Collaborative Project Management   ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

TASK_STATUSES = {"open": "├â┬░├à┬╕├à┬╕├é┬ó", "in_progress": "├â┬░├à┬╕├óΓé¼┬¥├é┬╡", "review": "├â┬░├à┬╕├à┬╕├é┬í", "done": "├â┬ó├àΓÇ£├óΓé¼┬ª", "blocked": "├â┬░├à┬╕├óΓé¼┬¥├é┬┤"}
TASK_PRIORITIES = {"low": "├â┬ó├é┬¼├óΓé¼┬í├»┬╕┬Å", "normal": "├â┬ó├à┬╛├é┬í├»┬╕┬Å", "high": "├â┬ó├é┬¼├óΓé¼┬á├»┬╕┬Å", "urgent": "├â┬░├à┬╕├óΓé¼┬¥├é┬Ñ"}

@dp.message(Command("tasks"))
async def cmd_tasks(m: types.Message):
    parts = m.text.split()
    filt = parts[1].lower() if len(parts) > 1 else None
    where = "WHERE status != 'done'" if not filt else f"WHERE status='{filt}'" if filt in TASK_STATUSES else f"WHERE project='{filt}'"
    if filt == "all":
        where = ""
    elif filt == "mine":
        where = f"WHERE assigned_to={m.from_user.id} AND status != 'done'"
    rows = await _pg_val(
        f"SELECT id,title,status,priority,project,assigned_name,created_by_name "
        f"FROM task_board {where} ORDER BY "
        f"CASE priority WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 WHEN 'normal' THEN 2 ELSE 3 END, "
        f"created_at DESC LIMIT 25"
    )
    # counts per status
    cnt_open = await _pg_val("SELECT count(*) FROM task_board WHERE status='open'")
    cnt_prog = await _pg_val("SELECT count(*) FROM task_board WHERE status='in_progress'")
    cnt_review = await _pg_val("SELECT count(*) FROM task_board WHERE status='review'")
    cnt_done = await _pg_val("SELECT count(*) FROM task_board WHERE status='done'")
    cnt_block = await _pg_val("SELECT count(*) FROM task_board WHERE status='blocked'")
    header = (
        f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Task Board</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├à┬╕├é┬ó ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥: {(cnt_open or '0').strip()} | "
        f"├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥: {(cnt_prog or '0').strip()} | "
        f"├â┬░├à┬╕├à┬╕├é┬í review: {(cnt_review or '0').strip()}\n"
        f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬ó: {(cnt_done or '0').strip()} | "
        f"├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥: {(cnt_block or '0').strip()}\n\n"
    )
    if not rows or rows.strip() == "":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="├â┬ó├à┬╛├óΓé¼┬ó ├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥", callback_data="task_menu_new")],
            [
                InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├à┬á ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó", callback_data="task_menu_daily"),
                InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ ├ù┬¿├ù┬ó├ù┬á├âΓÇö├à┬╕", callback_data="task_menu_refresh"),
            ]
        ])
        return await m.answer(header + "├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼┬║├ù┬¿├âΓÇö├óΓé¼Γäó├ù┬ó.\n\n├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ú: /task_new ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¬├ù┬¿├ù┬¬", reply_markup=kb)
    text = header
    # group by project
    projects = {}
    for line in rows.strip().split("\n"):
        cols = line.split("|")
        if len(cols) < 7:
            continue
        tid, title, status, prio, proj, assignee, creator = [c.strip() for c in cols]
        proj = proj or "general"
        if proj not in projects:
            projects[proj] = []
        projects[proj].append((tid, title, status, prio, assignee))
    for proj, items in sorted(projects.items()):
        text += f"<b>├â┬░├à┬╕├óΓé¼┼ô├é┬ü {proj.upper()}</b>\n"
        for tid, title, status, prio, assignee in items:
            si = TASK_STATUSES.get(status, "├â┬ó├é┬¥├óΓé¼┼ô")
            pi = TASK_PRIORITIES.get(prio, "├â┬ó├à┬╛├é┬í├»┬╕┬Å")
            who = f"├â┬ó├óΓé¼┬á├óΓé¼Γäó {assignee}" if assignee else ""
            text += f"  {si}{pi} <b>#{tid}</b> {title[:35]} {who}\n"
        text += "\n"
    # inline buttons
    buttons = [
        [
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó", callback_data="task_filter_mine"),
            InlineKeyboardButton(text="├â┬░├à┬╕├à┬╕├é┬ó ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥", callback_data="task_filter_open"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥", callback_data="task_filter_in_progress"),
        ],
        [
            InlineKeyboardButton(text="├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬ó", callback_data="task_filter_done"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥", callback_data="task_filter_blocked"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├à┬á ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£", callback_data="task_filter_all"),
        ],
        [
            InlineKeyboardButton(text="├â┬ó├à┬╛├óΓé¼┬ó ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥", callback_data="task_menu_new"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ ├ù┬¿├ù┬ó├ù┬á├âΓÇö├à┬╕", callback_data="task_menu_refresh"),
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await m.answer(text[:4000], reply_markup=kb)


@dp.callback_query(lambda c: c.data and c.data.startswith("task_filter_"))
async def cb_task_filter(cq: CallbackQuery):
    filt = cq.data.replace("task_filter_", "")
    uid = cq.from_user.id
    if filt == "mine":
        where = f"WHERE assigned_to={uid} AND status != 'done'"
        label = "├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó"
    elif filt == "all":
        where = ""
        label = "├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬"
    elif filt in TASK_STATUSES:
        where = f"WHERE status='{filt}'"
        label = filt
    else:
        where = "WHERE status != 'done'"
        label = "├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬"
    rows = await _pg_val(
        f"SELECT id,title,status,priority,project,assigned_name FROM task_board {where} "
        f"ORDER BY CASE priority WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 WHEN 'normal' THEN 2 ELSE 3 END LIMIT 20"
    )
    text = f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ {label}</b>\n├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
    if not rows or rows.strip() == "":
        text += "├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼╦£├ù┬º├âΓÇö├ï┼ô├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó."
    else:
        for line in rows.strip().split("\n"):
            cols = line.split("|")
            if len(cols) >= 6:
                tid, title, status, prio, proj, assignee = [c.strip() for c in cols]
                si = TASK_STATUSES.get(status, "├â┬ó├é┬¥├óΓé¼┼ô")
                pi = TASK_PRIORITIES.get(prio, "├â┬ó├à┬╛├é┬í├»┬╕┬Å")
                text += f"{si}{pi} <b>#{tid}</b> {title[:35]}\n   ├â┬░├à┬╕├óΓé¼┼ô├é┬ü {proj} | ├â┬░├à┬╕├óΓé¼╦£├é┬ñ {assignee or '├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥'}\n"
    buttons = [
        [
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó", callback_data="task_filter_mine"),
            InlineKeyboardButton(text="├â┬░├à┬╕├à┬╕├é┬ó ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥", callback_data="task_filter_open"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥", callback_data="task_filter_in_progress"),
        ],
        [
            InlineKeyboardButton(text="├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬ó", callback_data="task_filter_done"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥", callback_data="task_filter_blocked"),
            InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┼ô├à┬á ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£", callback_data="task_filter_all"),
        ],
    ]
    try:
        await cq.message.edit_text(text[:4000], reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except:
        await cq.answer("├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬¿├ù┬ó├ù┬á├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕")
    await cq.answer()


@dp.callback_query(lambda c: c.data == "task_menu_refresh")
async def cb_task_refresh(cq: CallbackQuery):
    await cq.answer("├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ ├âΓÇö├à┬╛├ù┬¿├ù┬ó├ù┬á├âΓÇö├à┬╕...")
    fake_msg = cq.message
    fake_msg.text = "/tasks"
    fake_msg.from_user = cq.from_user
    try:
        await cq.message.delete()
    except: pass
    await cmd_tasks(fake_msg)


@dp.callback_query(lambda c: c.data == "task_menu_new")
async def cb_task_new(cq: CallbackQuery):
    await cq.answer()
    await cq.message.answer(
        "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥</b>\n\n"
        "├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├à┬╛├âΓÇö├ï┼ô:\n"
        "<code>/task_new ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¬├ù┬¿├ù┬¬</code>\n\n"
        "├ù┬É├âΓÇö├óΓé¼┬ó ├âΓÇö├à┬╛├ù┬¬├ù┬º├âΓÇö├óΓé¼┼ô├ù┬¥:\n"
        "<code>/task_new ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¬├ù┬¿├ù┬¬ | ├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¿ | ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô | ├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬¬</code>\n\n"
        "├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬: low, normal, high, urgent"
    )


@dp.callback_query(lambda c: c.data == "task_menu_daily")
async def cb_task_daily(cq: CallbackQuery):
    await cq.answer()
    fake_msg = cq.message
    fake_msg.text = "/daily_report"
    fake_msg.from_user = cq.from_user
    await cmd_daily_report(fake_msg)


@dp.message(Command("task_new"))
async def cmd_task_new(m: types.Message):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer(
            "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥</b>\n\n"
            "Usage: /task_new title\n"
            "├âΓÇö├à┬╛├ù┬¬├ù┬º├âΓÇö├óΓé¼┼ô├ù┬¥: /task_new title | description | project | priority\n\n"
            "priorities: low, normal, high, urgent\n"
            "├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥: /task_new Fix login bug | The login page crashes | auth | high"
        )
    raw = parts[1].split("|")
    title = raw[0].strip()
    desc = raw[1].strip() if len(raw) > 1 else ""
    project = raw[2].strip() if len(raw) > 2 else "general"
    priority = raw[3].strip().lower() if len(raw) > 3 else "normal"
    if priority not in TASK_PRIORITIES:
        priority = "normal"
    uid = m.from_user.id
    name = (m.from_user.full_name or "").replace("'", "")
    tid = await _pg_val(
        f"INSERT INTO task_board (title,description,project,priority,created_by,created_by_name) "
        f"VALUES ('{title.replace(chr(39),'')}','{desc.replace(chr(39),'')}','{project.replace(chr(39),'')}','{priority}',{uid},'{name}') "
        f"RETURNING id"
    )
    if tid:
        pi = TASK_PRIORITIES.get(priority, "├â┬ó├à┬╛├é┬í├»┬╕┬Å")
        await m.answer(
            f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid.strip()} ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬¥</b>\n"
            f"{pi} {title}\n├â┬░├à┬╕├óΓé¼┼ô├é┬ü {project}\n\n"
            f"├âΓÇö├àΓÇ£├ù┬º├âΓÇö├óΓé¼ΓÇ¥├ù┬¬: /task_pick {tid.strip()}"
        )
        if uid != OWNER_ID:
            try:
                await bot.send_message(OWNER_ID, f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥ #{tid.strip()} ├âΓÇö├à┬╛-{name}:\n{title}")
            except:
                pass
    else:
        await m.answer("├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥")
    await audit(uid, "/task_new", "ok", title[:50])


@dp.message(Command("task_pick"))
async def cmd_task_pick(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /task_pick ID")
    tid = parts[1]
    uid = m.from_user.id
    name = (m.from_user.full_name or "").replace("'", "")
    ok = await _pg_ok(
        f"UPDATE task_board SET assigned_to={uid}, assigned_name='{name}', "
        f"status='in_progress', updated_at=NOW() "
        f"WHERE id={tid} AND status IN ('open','review')"
    )
    if ok:
        await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├é┬╡ <b>├âΓÇö├àΓÇ£├ù┬º├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}</b>\n├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥: /task_done {tid}")
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥ ├ù┬É├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬¬├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬í├âΓÇö├óΓé¼┬¥")
    await audit(uid, "/task_pick", "ok", tid)


@dp.message(Command("task_done"))
async def cmd_task_done(m: types.Message):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer("Usage: /task_done ID [notes]")
    args = parts[1].split(maxsplit=1)
    tid = args[0]
    notes = args[1].replace("'", "") if len(args) > 1 else ""
    uid = m.from_user.id
    note_sql = f", notes=notes||chr(10)||'{notes}'" if notes else ""
    ok = await _pg_ok(
        f"UPDATE task_board SET status='done', completed_at=NOW(), updated_at=NOW() "
        f"{',' if notes else ''}"
        f"{'notes=COALESCE(notes,chr(39)||chr(39))||chr(10)||chr(39)' + notes + chr(39) if notes else ''}"
        f" WHERE id={tid}"
    )
    if not ok:
        ok = await _pg_ok(f"UPDATE task_board SET status='done', completed_at=NOW(), updated_at=NOW() WHERE id={tid}")
    if ok:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥!</b>")
        title = await _pg_val(f"SELECT title FROM task_board WHERE id={tid}")
        if uid != OWNER_ID:
            try:
                await bot.send_message(OWNER_ID, f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├ù┬ó\"├âΓÇö├óΓÇ₧┬ó {m.from_user.full_name}:\n{title}")
            except:
                pass
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥")
    await audit(uid, "/task_done", "ok", tid)


@dp.message(Command("task_return"))
async def cmd_task_return(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /task_return ID")
    tid = parts[1]
    ok = await _pg_ok(
        f"UPDATE task_board SET assigned_to=NULL, assigned_name='', "
        f"status='open', updated_at=NOW() WHERE id={tid}"
    )
    if ok:
        await m.answer(f"├â┬░├à┬╕├à┬╕├é┬ó <b>├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼ΓÇ£├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥</b>\n├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├ù┬¥.")
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥")
    await audit(m.from_user.id, "/task_return", "ok", tid)


@dp.message(Command("task_info"))
async def cmd_task_info(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /task_info ID")
    tid = parts[1]
    row = await _pg_val(
        f"SELECT id,title,description,status,priority,project,assigned_name,created_by_name,"
        f"created_at::text,updated_at::text,completed_at::text,notes "
        f"FROM task_board WHERE id={tid}"
    )
    if not row or row.strip() == "":
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥")
    cols = row.strip().split("|")
    if len(cols) < 12:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬º├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}")
    si = TASK_STATUSES.get(cols[3].strip(), "├â┬ó├é┬¥├óΓé¼┼ô")
    pi = TASK_PRIORITIES.get(cols[4].strip(), "├â┬ó├à┬╛├é┬í├»┬╕┬Å")
    await m.answer(
        f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{cols[0].strip()}</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├é┬¥ <b>{cols[1].strip()}</b>\n"
        f"{cols[2].strip() or '(├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├ù┬É ├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¿)'}\n\n"
        f"{si} ├ù┬í├âΓÇö├ï┼ô├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├ù┬í: <b>{cols[3].strip()}</b>\n"
        f"{pi} ├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬¬: <b>{cols[4].strip()}</b>\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├é┬ü ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô: <b>{cols[5].strip()}</b>\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬º├ù┬ª├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£: {cols[6].strip() or '├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥'}\n"
        f"├â┬ó├àΓÇ£├é┬ì├»┬╕┬Å ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿ ├ù┬ó\"├âΓÇö├óΓÇ₧┬ó: {cols[7].strip()}\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬ª ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿: {cols[8].strip()[:16]}\n"
        f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕: {cols[9].strip()[:16]}\n"
        f"{'├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├ù┬¥: ' + cols[10].strip()[:16] if cols[10].strip() else ''}\n"
        f"{'├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬: ' + cols[11].strip()[:200] if cols[11].strip() else ''}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├âΓÇö├àΓÇ£├ù┬º├âΓÇö├óΓé¼ΓÇ¥├ù┬¬", callback_data=f"tact_pick_{tid}"),
                InlineKeyboardButton(text="├â┬ó├àΓÇ£├óΓé¼┬ª ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥", callback_data=f"tact_done_{tid}"),
                InlineKeyboardButton(text="├â┬░├à┬╕├à┬╕├é┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼ΓÇ£├ù┬¿├âΓÇö├óΓé¼┬¥", callback_data=f"tact_return_{tid}"),
            ],
            [
                InlineKeyboardButton(text="├â┬░├à┬╕├à┬╕├é┬í Review", callback_data=f"tact_review_{tid}"),
                InlineKeyboardButton(text="├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥", callback_data=f"tact_block_{tid}"),
            ],
        ])
    )


@dp.message(Command("task_set"))
async def cmd_task_set(m: types.Message):
    parts = m.text.split()
    if len(parts) < 4:
        return await m.answer(
            "Usage: /task_set ID field value\n"
            "Fields: status, priority, project, title, description\n"
            "Example: /task_set 3 priority urgent"
        )
    tid, field, val = parts[1], parts[2].lower(), parts[3].lower()
    allowed = {"status": TASK_STATUSES.keys(), "priority": TASK_PRIORITIES.keys()}
    if field in allowed and val not in allowed[field]:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬É├ù┬ñ├ù┬⌐├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├àΓÇ£-{field}: {', '.join(allowed[field])}")
    col_map = {"status": "status", "priority": "priority", "project": "project",
               "title": "title", "description": "description"}
    col = col_map.get(field)
    if not col:
        return await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬¿: {field}")
    raw_val = " ".join(parts[3:]).replace("'", "")
    ok = await _pg_ok(f"UPDATE task_board SET {col}='{raw_val}', updated_at=NOW() WHERE id={tid}")
    if ok:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}: {field} = {raw_val}")
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}")


@dp.callback_query(lambda c: c.data and c.data.startswith("tact_"))
async def cb_task_action(cq: CallbackQuery):
    parts = cq.data.split("_", 2)
    action = parts[1]
    tid = parts[2]
    uid = cq.from_user.id
    name = (cq.from_user.full_name or "").replace("'", "")
    status_map = {"pick": "in_progress", "done": "done", "return": "open", "review": "review", "block": "blocked"}
    new_status = status_map.get(action)
    if not new_status:
        return await cq.answer("├â┬ó├é┬¥├àΓÇÖ")
    extra = ""
    if action == "pick":
        extra = f", assigned_to={uid}, assigned_name='{name}'"
    elif action == "return":
        extra = ", assigned_to=NULL, assigned_name=''"
    elif action == "done":
        extra = ", completed_at=NOW()"
    ok = await _pg_ok(f"UPDATE task_board SET status='{new_status}'{extra}, updated_at=NOW() WHERE id={tid}")
    labels = {"pick": "├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├ù┬á├âΓÇö├àΓÇ£├ù┬º├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥", "done": "├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥", "return": "├â┬░├à┬╕├à┬╕├é┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼ΓÇ£├ù┬¿├âΓÇö├óΓé¼┬¥", "review": "├â┬░├à┬╕├à┬╕├é┬í Review", "block": "├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥"}
    if ok:
        await cq.answer(f"{labels.get(action, '├â┬ó├àΓÇ£├óΓé¼┬ª')} ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}")
        try:
            await cq.message.edit_text(
                cq.message.text + f"\n\n<b>{labels.get(action, '')} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {name}</b>"
            )
        except:
            pass
    else:
        await cq.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ #{tid}")


@dp.message(Command("task_comment"))
async def cmd_task_comment(m: types.Message):
    parts = m.text.split(maxsplit=2)
    if len(parts) < 3:
        return await m.answer("Usage: /task_comment ID your comment text")
    tid = parts[1]
    comment = parts[2].replace("'", "").strip()
    name = (m.from_user.full_name or "User").replace("'", "")
    ts = datetime.datetime.now().strftime("%d/%m %H:%M")
    entry = f"[{ts} {name}] {comment}"
    ok = await _pg_ok(
        f"UPDATE task_board SET notes=COALESCE(notes,'')||chr(10)||'{entry}', "
        f"updated_at=NOW() WHERE id={tid}"
    )
    if ok:
        await m.answer(f"├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├âΓÇö├óΓé¼┬¥├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬í├ù┬ñ├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}")
        title = await _pg_val(f"SELECT title FROM task_board WHERE id={tid}")
        creator = await _pg_val(f"SELECT created_by FROM task_board WHERE id={tid}")
        assignee = await _pg_val(f"SELECT assigned_to FROM task_board WHERE id={tid}")
        uid = m.from_user.id
        notify_set = set()
        if creator and creator.strip():
            notify_set.add(int(creator.strip()))
        if assignee and assignee.strip():
            notify_set.add(int(assignee.strip()))
        notify_set.discard(uid)
        for nuid in notify_set:
            try:
                await bot.send_message(
                    nuid,
                    f"├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├âΓÇö├óΓé¼┬¥├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ <b>#{tid}</b> ({(title or '').strip()[:30]}):\n{comment[:200]}\n├âΓÇö├à┬╛├ù┬É├ù┬¬: {name}"
                )
            except:
                pass
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥")


@dp.message(Command("task_assign"))
async def cmd_task_assign(m: types.Message):
    parts = m.text.split()
    if len(parts) < 3:
        return await m.answer("Usage: /task_assign TASK_ID USER_ID")
    tid, target_uid = parts[1], parts[2]
    target_name = ""
    try:
        chat = await bot.get_chat(int(target_uid))
        target_name = (chat.full_name or chat.username or target_uid).replace("'", "")
    except:
        target_name = target_uid
    ok = await _pg_ok(
        f"UPDATE task_board SET assigned_to={target_uid}, assigned_name='{target_name}', "
        f"status='in_progress', updated_at=NOW() WHERE id={tid}"
    )
    if ok:
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬º├ù┬ª├ù┬¬├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-{target_name}")
        try:
            title = await _pg_val(f"SELECT title FROM task_board WHERE id={tid}")
            await bot.send_message(
                int(target_uid),
                f"├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ <b>├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬º├ù┬ª├ù┬¬├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬í</b>\n{(title or '').strip()}\n\n"
                f"├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥: /task_done {tid}\n├ù┬ñ├ù┬¿├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¥: /task_info {tid}"
            )
        except:
            pass
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬¥├ù┬º├ù┬ª├ù┬É├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid}")


@dp.message(Command("task_review"))
async def cmd_task_review(m: types.Message):
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /task_review ID")
    tid = parts[1]
    ok = await _pg_ok(
        f"UPDATE task_board SET status='review', updated_at=NOW() WHERE id={tid}"
    )
    if ok:
        await m.answer(f"├â┬░├à┬╕├à┬╕├é┬í <b>├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬ó├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-Review</b>")
        creator = await _pg_val(f"SELECT created_by FROM task_board WHERE id={tid}")
        if creator and creator.strip() and int(creator.strip()) != m.from_user.id:
            try:
                title = await _pg_val(f"SELECT title FROM task_board WHERE id={tid}")
                await bot.send_message(
                    int(creator.strip()),
                    f"├â┬░├à┬╕├à┬╕├é┬í ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ <b>#{tid}</b> ({(title or '').strip()[:30]}) ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬ó├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-Review ├ù┬ó\"├âΓÇö├óΓÇ₧┬ó {m.from_user.full_name}"
                )
            except:
                pass
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥")


@dp.message(Command("task_block"))
async def cmd_task_block(m: types.Message):
    parts = m.text.split(maxsplit=2)
    if len(parts) < 2:
        return await m.answer("Usage: /task_block ID [reason]")
    tid = parts[1]
    reason = parts[2].replace("'", "") if len(parts) > 2 else ""
    name = (m.from_user.full_name or "").replace("'", "")
    ok = await _pg_ok(
        f"UPDATE task_board SET status='blocked', updated_at=NOW() WHERE id={tid}"
    )
    if ok and reason:
        ts = datetime.datetime.now().strftime("%d/%m %H:%M")
        await _pg_ok(
            f"UPDATE task_board SET notes=COALESCE(notes,'')||chr(10)||'[{ts} BLOCKED {name}] {reason}' WHERE id={tid}"
        )
    if ok:
        await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├é┬┤ <b>├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥</b>{'  ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ' + reason if reason else ''}")
        if OWNER_ID != m.from_user.id:
            try:
                title = await _pg_val(f"SELECT title FROM task_board WHERE id={tid}")
                await bot.send_message(OWNER_ID, f"├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥: {(title or '').strip()}\n{reason}")
            except:
                pass
    else:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ #{tid} ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓé¼┬¥")


@dp.message(Command("daily_report"))
async def cmd_daily_report(m: types.Message):
    text = f"<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</b>\n"
    text += "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
    open_tasks = await _pg_val("SELECT count(*) FROM task_board WHERE status='open'")
    progress = await _pg_val("SELECT count(*) FROM task_board WHERE status='in_progress'")
    done_today = await _pg_val("SELECT count(*) FROM task_board WHERE status='done' AND completed_at >= CURRENT_DATE")
    blocked = await _pg_val("SELECT count(*) FROM task_board WHERE status='blocked'")
    total = await _pg_val("SELECT count(*) FROM task_board")
    text += (
        f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n"
        f"  ├â┬░├à┬╕├à┬╕├é┬ó ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬: {(open_tasks or '0').strip()}\n"
        f"  ├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥: {(progress or '0').strip()}\n"
        f"  ├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥: {(done_today or '0').strip()}\n"
        f"  ├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬: {(blocked or '0').strip()}\n"
        f"  ├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬í├âΓÇö├óΓé¼┬¥\"├âΓÇö├óΓé¼┬║: {(total or '0').strip()}\n\n"
    )
    recent = await _pg_val(
        "SELECT id,title,status,assigned_name FROM task_board "
        "WHERE updated_at >= CURRENT_DATE ORDER BY updated_at DESC LIMIT 10"
    )
    if recent and recent.strip():
        text += "<b>├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥:</b>\n"
        for line in recent.strip().split("\n"):
            cols = line.split("|")
            if len(cols) >= 4:
                si = TASK_STATUSES.get(cols[2].strip(), "├â┬ó├é┬¥├óΓé¼┼ô")
                text += f"  {si} #{cols[0].strip()} {cols[1].strip()[:30]} ({cols[3].strip() or '├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥'})\n"
    if dc:
        containers = dc.containers.list(all=True)
        running = sum(1 for c in containers if c.status == "running")
        stopped = sum(1 for c in containers if c.status != "running")
        text += f"\n<b>├â┬░├à┬╕├é┬É├é┬│ Docker:</b> {running}├â┬░├à┬╕├à┬╕├é┬ó {stopped}├â┬░├à┬╕├óΓé¼┬¥├é┬┤\n"
    users = await _pg_val("SELECT count(*) FROM abac_users WHERE is_active=true")
    text += f"<b>├â┬░├à┬╕├óΓé¼╦£├é┬Ñ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬ñ├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b> {(users or '0').strip()}\n"
    text += f"\n├â┬░├à┬╕├óΓé¼Γäó├é┬í /tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ | /task_new ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥"
    await m.answer(text[:4000])


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  18. GITHUB CONNECT & CODE ASSIST (SaaS)             ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

@dp.message(Command("connect_github"))
async def cmd_connect_github(m: types.Message):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer(
            "<b>├â┬░├à┬╕├óΓé¼┬¥├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿ GitHub ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬</b>\n"
            "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
            "├ù┬⌐├ù┬¬├ù┬ú ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├óΓé¼┬ó├ù┬á├ù┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├àΓÇ£├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓé¼┬ó!\n\n"
            "<b>├ù┬É├ù┬ñ├ù┬⌐├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬ 1 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó:</b>\n"
            "<code>/connect_github https://github.com/user/repo</code>\n\n"
            "<b>├ù┬É├ù┬ñ├ù┬⌐├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬ 2 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├ù┬¥ ├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ GitHub:</b>\n"
            "<code>/connect_github username</code>\n\n"
            "├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓÇ₧┬ó ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿:\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó /my_repos ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó /analyze REPO ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô + ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¬\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó /fix REPO ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ª├ù┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬\n"
            "├â┬ó├óΓÇÜ┬¼├é┬ó /review REPO ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥\n\n"
            "├â┬░├à┬╕├óΓé¼Γäó├é┬í ├ù┬É├ù┬á├âΓÇö├óΓé¼ΓÇ¥├ù┬á├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£├ù┬É ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬í├âΓÇö├à┬╛├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬. ├âΓÇö├àΓÇ£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬ñ├ù┬¿├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿ Personal Access Token ├âΓÇö├óΓé¼╦£-GitHub Settings."
        )
    gh_input = parts[1].strip()
    uid = m.from_user.id
    name = (m.from_user.full_name or "").replace("'", "")
    if "github.com/" in gh_input:
        repo_url = gh_input.split("github.com/")[1].rstrip("/")
        gh_type = "repo"
    elif "/" in gh_input:
        repo_url = gh_input
        gh_type = "repo"
    else:
        repo_url = gh_input
        gh_type = "user"
    ok = await _pg_ok(
        f"INSERT INTO user_github (user_id, user_name, gh_type, gh_value) "
        f"VALUES ({uid},'{name}','{gh_type}','{repo_url.replace(chr(39),'')}') "
        f"ON CONFLICT (user_id, gh_value) DO UPDATE SET updated_at=NOW()"
    )
    if ok:
        if gh_type == "repo":
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://api.github.com/repos/{repo_url}", timeout=10) as r:
                    if r.status == 200:
                        data = await r.json()
                        await m.answer(
                            f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬¿!</b>\n\n"
                            f"├â┬░├à┬╕├óΓé¼┼ô├é┬ª <b>{data.get('full_name','?')}</b>\n"
                            f"├â┬░├à┬╕├óΓé¼┼ô├é┬¥ {data.get('description','') or '(├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├ù┬É ├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¿)'}\n"
                            f"├ó┬¡┬É {data.get('stargazers_count',0)} | ├â┬░├à┬╕├é┬ì├é┬┤ {data.get('forks_count',0)}\n"
                            f"├â┬░├à┬╕├óΓé¼Γäó├é┬╗ {data.get('language','?')} | {'├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼ô ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó' if not data.get('private') else '├â┬░├à┬╕├óΓé¼┬¥├óΓé¼Γäó ├ù┬ñ├ù┬¿├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó'}\n\n"
                            f"├ù┬ó├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó ├ù┬á├ù┬í├âΓÇö├óΓé¼┬¥:\n"
                            f"/analyze {repo_url.split('/')[-1]} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô\n"
                            f"/review {repo_url.split('/')[-1]} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô"
                        )
                    else:
                        await m.answer(f"├â┬ó├à┬í├é┬á├»┬╕┬Å ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬É├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É ├âΓÇö├óΓé¼╦£-GitHub (├ù┬ñ├ù┬¿├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó?) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├ù┬⌐├âΓÇö├à┬╛├ù┬¿ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬º├ù┬¿├âΓÇö├óΓé¼┬¥.")
        else:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://api.github.com/users/{repo_url}", timeout=10) as r:
                    if r.status == 200:
                        data = await r.json()
                        await m.answer(
                            f"├â┬ó├àΓÇ£├óΓé¼┬ª <b>├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ GitHub ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬¿!</b>\n\n"
                            f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ <b>{data.get('login','?')}</b> ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {data.get('name','')}\n"
                            f"├â┬░├à┬╕├óΓé¼┼ô├é┬ª {data.get('public_repos',0)} ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
                            f"├â┬░├à┬╕├óΓé¼┼ô├é┬¥ {data.get('bio','') or ''}\n\n"
                            f"├ù┬á├ù┬í├âΓÇö├óΓé¼┬¥: /my_repos ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬¿├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í"
                        )
                    else:
                        await m.answer(f"├â┬ó├à┬í├é┬á├»┬╕┬Å ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬É├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬º ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬⌐├ù┬¥.")
    else:
        await m.answer("├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬⌐├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥. ├ù┬á├ù┬í├âΓÇö├óΓé¼┬¥ /connect_github ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£.")
    await audit(uid, "/connect_github", "ok", gh_input[:50])


@dp.message(Command("my_repos"))
async def cmd_my_repos(m: types.Message):
    uid = m.from_user.id
    rows = await _pg_val(f"SELECT gh_type,gh_value FROM user_github WHERE user_id={uid}")
    if not rows or rows.strip() == "":
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ ├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥.\n├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿: /connect_github username_or_url")
    text = "<b>├â┬░├à┬╕├óΓé¼┼ô├é┬ª ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í</b>\n├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
    for line in rows.strip().split("\n"):
        cols = line.split("|")
        if len(cols) >= 2:
            gtype, gval = cols[0].strip(), cols[1].strip()
            if gtype == "user":
                text += f"├â┬░├à┬╕├óΓé¼╦£├é┬ñ GitHub User: <b>{gval}</b>\n"
                try:
                    async with aiohttp.ClientSession() as s:
                        async with s.get(f"https://api.github.com/users/{gval}/repos?sort=updated&per_page=10", timeout=10) as r:
                            if r.status == 200:
                                repos = await r.json()
                                for repo in repos:
                                    lang = repo.get("language", "?") or "?"
                                    text += f"   ├â┬░├à┬╕├óΓé¼┼ô├é┬ü <b>{repo['name']}</b> ({lang}) ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ó┬¡┬É{repo.get('stargazers_count',0)}\n"
                except:
                    pass
            else:
                text += f"├â┬░├à┬╕├óΓé¼┼ô├é┬ü Repo: <b>{gval}</b>\n"
    text += "\n/analyze REPO ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ | /review REPO ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥"
    await m.answer(text[:4000])


@dp.message(Command("analyze"))
async def cmd_analyze(m: types.Message):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer("Usage: /analyze repo_name\nExample: /analyze my-project")
    repo = parts[1].strip()
    uid = m.from_user.id
    gh_row = await _pg_val(f"SELECT gh_value FROM user_github WHERE user_id={uid} AND gh_type='user' LIMIT 1")
    if gh_row and gh_row.strip():
        full_repo = f"{gh_row.strip()}/{repo}"
    else:
        gh_row2 = await _pg_val(f"SELECT gh_value FROM user_github WHERE user_id={uid} AND gh_value LIKE '%/{repo}' LIMIT 1")
        full_repo = gh_row2.strip() if gh_row2 else repo
    if "/" not in full_repo:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├ù┬ª├ù┬É├ù┬¬├âΓÇö├óΓÇ₧┬ó ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó. ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬¥: /connect_github username")
    msg = await m.answer(f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì <b>├âΓÇö├à┬╛├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ {full_repo}...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.github.com/repos/{full_repo}", timeout=10) as r:
                if r.status != 200:
                    return await msg.edit_text(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£├ù┬É ├ù┬á├âΓÇö├à┬╛├ù┬ª├ù┬É: {full_repo}")
                repo_data = await r.json()
            async with s.get(f"https://api.github.com/repos/{full_repo}/languages", timeout=10) as r:
                langs = await r.json() if r.status == 200 else {}
            async with s.get(f"https://api.github.com/repos/{full_repo}/contents", timeout=10) as r:
                files = await r.json() if r.status == 200 else []
    except:
        return await msg.edit_text("├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-GitHub API")
    total_bytes = sum(langs.values()) if langs else 0
    lang_text = ", ".join(f"{k} ({v*100//total_bytes}%)" for k, v in sorted(langs.items(), key=lambda x: -x[1])[:5]) if langs else "?"
    file_list = [f.get("name", "") for f in (files if isinstance(files, list) else [])]
    has_readme = any("readme" in f.lower() for f in file_list)
    has_tests = any("test" in f.lower() for f in file_list)
    has_ci = any(f in (".github", ".gitlab-ci.yml", "Jenkinsfile") for f in file_list)
    has_docker = any("docker" in f.lower() for f in file_list)
    has_deps = any(f in ("requirements.txt", "package.json", "Cargo.toml", "go.mod", "Gemfile") for f in file_list)
    score = sum([has_readme, has_tests, has_ci, has_docker, has_deps]) * 20
    issues = await _pg_val(f"nope") or "0"
    prompt = (
        f"Analyze this GitHub repo and give actionable suggestions in Hebrew:\n"
        f"Repo: {full_repo}\n"
        f"Language: {lang_text}\n"
        f"Stars: {repo_data.get('stargazers_count',0)}, Forks: {repo_data.get('forks_count',0)}\n"
        f"Open issues: {repo_data.get('open_issues_count',0)}\n"
        f"Files in root: {', '.join(file_list[:20])}\n"
        f"Has: README={has_readme}, Tests={has_tests}, CI={has_ci}, Docker={has_docker}, Deps={has_deps}\n"
        f"Health score: {score}/100\n"
        f"Give 5 specific suggestions to improve this project."
    )
    raw_response = await ai_chat(prompt, m.from_user.full_name or "User")
    ai_response = str(raw_response) if raw_response else "SLH v53 ready."
    await msg.edit_text(
        f"<b>├â┬░├à┬╕├óΓé¼┬¥├é┬ì ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥: {repo_data.get('full_name','?')}</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n"
        f"├â┬░├à┬╕├óΓé¼Γäó├é┬╗ {lang_text}\n"
        f"├ó┬¡┬É {repo_data.get('stargazers_count',0)} | ├â┬░├à┬╕├é┬ì├é┬┤ {repo_data.get('forks_count',0)} | ├â┬░├à┬╕├é┬É├óΓé¼┬║ {repo_data.get('open_issues_count',0)} issues\n"
        f"├â┬░├à┬╕├óΓé¼┼ô├à┬á ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬: {'├â┬░├à┬╕├à┬╕├é┬ó' if score >= 80 else '├â┬░├à┬╕├à┬╕├é┬í' if score >= 40 else '├â┬░├à┬╕├óΓé¼┬¥├é┬┤'} {score}/100\n"
        f"{'├â┬ó├àΓÇ£├óΓé¼┬ª' if has_readme else '├â┬ó├é┬¥├àΓÇÖ'} README | {'├â┬ó├àΓÇ£├óΓé¼┬ª' if has_tests else '├â┬ó├é┬¥├àΓÇÖ'} Tests | "
        f"{'├â┬ó├àΓÇ£├óΓé¼┬ª' if has_ci else '├â┬ó├é┬¥├àΓÇÖ'} CI | {'├â┬ó├àΓÇ£├óΓé¼┬ª' if has_docker else '├â┬ó├é┬¥├àΓÇÖ'} Docker\n\n"
        f"{ai_response[:2000]}"
    )
    await audit(uid, "/analyze", "ok", full_repo)


@dp.message(Command("review"))
async def cmd_review(m: types.Message):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.answer("Usage: /review repo_name\nExample: /review my-project")
    repo = parts[1].strip()
    uid = m.from_user.id
    gh_row = await _pg_val(f"SELECT gh_value FROM user_github WHERE user_id={uid} AND gh_type='user' LIMIT 1")
    full_repo = f"{gh_row.strip()}/{repo}" if gh_row and gh_row.strip() else repo
    if "/" not in full_repo:
        return await m.answer("├â┬ó├é┬¥├àΓÇÖ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬¥: /connect_github username")
    msg = await m.answer(f"├â┬░├à┬╕├óΓé¼┼ô├é┬¥ <b>├ù┬í├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô ├âΓÇö├óΓé¼╦£-{full_repo}...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.github.com/repos/{full_repo}/commits?per_page=5", timeout=10) as r:
                commits = await r.json() if r.status == 200 else []
            async with s.get(f"https://api.github.com/repos/{full_repo}/pulls?state=open&per_page=5", timeout=10) as r:
                prs = await r.json() if r.status == 200 else []
            async with s.get(f"https://api.github.com/repos/{full_repo}/issues?state=open&per_page=5", timeout=10) as r:
                issues = await r.json() if r.status == 200 else []
    except:
        return await msg.edit_text("├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-GitHub API")
    text = f"<b>├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├ù┬í├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô: {full_repo}</b>\n├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
    if commits and isinstance(commits, list):
        text += "<b>├â┬░├à┬╕├óΓé¼┼ô├àΓÇÖ commits ├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        for c in commits[:5]:
            msg_text = c.get("commit", {}).get("message", "?")[:50]
            author = c.get("commit", {}).get("author", {}).get("name", "?")
            text += f"  ├â┬ó├óΓÇÜ┬¼├é┬ó {msg_text} ({author})\n"
    if prs and isinstance(prs, list):
        text += f"\n<b>├â┬░├à┬╕├óΓé¼┬¥├óΓÇÜ┬¼ {len(prs)} PRs ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        for pr in prs[:5]:
            text += f"  ├â┬ó├óΓÇÜ┬¼├é┬ó #{pr.get('number',0)} {pr.get('title','?')[:40]}\n"
    if issues and isinstance(issues, list):
        real_issues = [i for i in issues if not i.get("pull_request")]
        if real_issues:
            text += f"\n<b>├â┬░├à┬╕├é┬É├óΓé¼┬║ {len(real_issues)} issues ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
            for i in real_issues[:5]:
                labels = " ".join(f"[{l['name']}]" for l in i.get("labels", [])[:3])
                text += f"  ├â┬ó├óΓÇÜ┬¼├é┬ó #{i.get('number',0)} {i.get('title','?')[:40]} {labels}\n"
    text += "\n├â┬░├à┬╕├óΓé¼Γäó├é┬í ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├ù┬¬ ├âΓÇö├ï┼ô├ù┬º├ù┬í├âΓÇö├ï┼ô ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬ñ├ù┬⌐├âΓÇö├óΓÇ₧┬ó ├ù┬ó├ù┬¥ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├ù┬í├ù┬ñ├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó├ù┬¬ ├ù┬ó├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô."
    await msg.edit_text(text[:4000])
    await audit(uid, "/review", "ok", full_repo)


@dp.message(Command("invite"))
async def cmd_invite(m: types.Message):
    uid = m.from_user.id
    code = hashlib.md5(f"slh_{uid}".encode()).hexdigest()[:8]
    link = f"https://t.me/MY_SUPER_ADMIN_bot?start=ref_{code}"
    ok = await _pg_ok(
        f"INSERT INTO referrals (user_id, ref_code) VALUES ({uid}, '{code}') "
        f"ON CONFLICT (user_id) DO NOTHING"
    )
    count = await _pg_val(f"SELECT count(*) FROM referrals WHERE referred_by={uid}")
    await m.answer(
        f"<b>├â┬░├à┬╕├à┬╜├óΓé¼┬░ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├à┬╕ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬!</b>\n"
        f"├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        f"├â┬░├à┬╕├óΓé¼┬¥├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬º ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í:\n<code>{link}</code>\n\n"
        f"├â┬░├à┬╕├óΓé¼╦£├é┬Ñ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├ù┬á├ù┬¬ ├ù┬ó├âΓÇö├óΓé¼┼ô ├ù┬ó├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó: <b>{(count or '0').strip()}</b> ├ù┬É├ù┬á├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥\n\n"
        f"<b>├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬¥ ├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        f"├â┬ó├óΓÇÜ┬¼├é┬ó ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬\n"
        f"├â┬ó├óΓÇÜ┬¼├é┬ó ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ AI ├âΓÇö├àΓÇ£├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├ù┬¥\n"
        f"├â┬ó├óΓÇÜ┬¼├é┬ó ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó\n"
        f"├â┬ó├óΓÇÜ┬¼├é┬ó ├ù┬í├ù┬º├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬\n\n"
        f"<b>├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├ù┬É├ù┬¬├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£:</b>\n"
        f"├â┬ó├óΓÇÜ┬¼├é┬ó ├ù┬⌐├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó trust level ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥\n"
        f"├â┬ó├óΓÇÜ┬¼├é┬ó ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬¬├ù┬º├âΓÇö├óΓé¼┼ô├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬¥\n\n"
        f"├ù┬⌐├ù┬¬├ù┬ú ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬º ├âΓÇö├óΓé¼╦£├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├ù┬¬├âΓÇö├óΓé¼┬║├ù┬á├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥! ├â┬░├à┬╕├à┬í├óΓÇÜ┬¼"
    )
    await audit(uid, "/invite", "ok", code)


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  19. AI CHAT ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Smart Free-Text Responses             ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

OPENAI_KEY = os.getenv("GROQ_API_KEY", "")

SYSTEM_PROMPT = """├ù┬É├ù┬¬├âΓÇö├óΓé¼┬¥ SLH Admin Bot ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô ├ù┬á├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ SLH Spark.
├ù┬É├ù┬¬├âΓÇö├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├ù┬¿ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ ├ù┬ó├ù┬¥ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬, ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬¥, ├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô├ù┬ó.
├ù┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¬ ├ù┬É├âΓÇö├àΓÇ£├ù┬É ├ù┬É├ù┬¥ ├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó ├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├à┬í ├âΓÇö├óΓé¼╦£├ù┬É├ù┬á├âΓÇö├óΓé¼Γäó├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¬.
├ù┬¬├âΓÇö├à┬╕ ├ù┬¬├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬º├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬º├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬.

├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├ù┬É├ù┬ñ├ù┬⌐├ù┬¿ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╕:
- /tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó
- /task_new ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐├âΓÇö├óΓé¼┬¥
- /my_access ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├ù┬á├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├àΓÇ£├âΓÇö├à┬í
- /guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É
- /esp_guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ESP32
- /agent_guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥
- /maximize ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬º├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥
- /status ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓé¼╦£ Docker
- /health ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬º├ù┬¬ ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬
- /morning ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿
- /daily_report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó

├ù┬É├ù┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├ù┬É├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥, ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬á├âΓÇö├óΓé¼┬¥ ├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼╦£-/my_access ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó ├âΓÇö├àΓÇ£├ù┬¿├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó,
├ù┬É├âΓÇö├óΓé¼┬ó ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ (├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬º├ù┬⌐├âΓÇö├óΓé¼┬¥ ├ù┬á├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¬).
"""

async def ai_chat(user_msg: str, user_name: str = "") -> str:
    if not OPENAI_KEY:
        return (
            "├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ ├âΓÇö├à┬╛├ù┬ª├âΓÇö├ï┼ô├ù┬ó├ù┬¿, AI ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┼ô├ù┬¿ ├ù┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕.\n\n"
            "├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¬├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬¥, ├ù┬á├ù┬í├âΓÇö├óΓé¼┬¥:\n"
            "/guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É\n"
            "/tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬\n"
            "/my_access ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í"
        )
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"[{user_name}]: {user_msg}"}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                timeout=15
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    return data["choices"][0]["message"]["content"]
                return f"├â┬ó├é┬¥├àΓÇÖ AI error ({r.status})"
    except Exception as e:
        return f"├â┬ó├é┬¥├àΓÇÖ AI unavailable: {str(e)[:100]}"


@dp.message(lambda m: m.text and not m.text.startswith("/") and m.chat.type == "private")
async def handle_free_text(m: types.Message):
    uid = m.from_user.id
    name = m.from_user.full_name or str(uid)
    ua = await get_user_attrs(uid)
    if not ua:
        return await m.answer(
            "├â┬░├à┬╕├óΓé¼╦£├óΓé¼┬╣ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥! ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô, ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬¥ ├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕:\n/create_me\n\n"
            "├ù┬É├âΓÇö├óΓé¼ΓÇ¥├ù┬¿├âΓÇö├óΓÇ₧┬ó ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬¥ ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├àΓÇ£├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬, ├âΓÇö├àΓÇ£├ù┬ª├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼┬ó├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô."
        )
    typing_msg = await m.answer("├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├óΓé¼╦£...")
    response = await ai_chat(m.text, name)
    try:
        await typing_msg.edit_text(response)
    except:
        await typing_msg.edit_text(response)
    await _pg_ok(
        f"INSERT INTO chat_messages (user_id,user_name,message,response) "
        f"VALUES ({uid},'{name.replace(chr(39),'')}','{m.text[:500].replace(chr(39),'')}','{response[:500].replace(chr(39),'')}') "
    )


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  20. PHOTO/SCREENSHOT HANDLER ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ AI Vision             ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

@dp.message(lambda m: m.photo and m.chat.type == "private")
async def handle_photo(m: types.Message):
    uid = m.from_user.id
    name = m.from_user.full_name or str(uid)
    ua = await get_user_attrs(uid)
    if not ua:
        return await m.answer("├â┬░├à┬╕├óΓé¼╦£├óΓé¼┬╣ ├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬¥: /create_me")
    caption = m.caption or ""
    typing_msg = await m.answer("├â┬░├à┬╕├óΓé¼┬¥├é┬ì ├âΓÇö├à┬╛├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥...")
    try:
        photo = m.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        async with aiohttp.ClientSession() as s:
            async with s.get(file_url) as r:
                img_bytes = await r.read()
        import base64
        img_b64 = base64.b64encode(img_bytes).decode()
        if not OPENAI_KEY:
            return await typing_msg.edit_text("├â┬ó├é┬¥├àΓÇÖ AI ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼Γäó├âΓÇö├óΓé¼┼ô├ù┬¿ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬")
        async with aiohttp.ClientSession() as s:
            async with s.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": (
                            "├ù┬É├ù┬¬├âΓÇö├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├ù┬¿ ├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó ├ù┬⌐├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ SLH Spark. "
                            "├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐ ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├ù┬⌐├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬É ├ù┬¬├ù┬º├âΓÇö├óΓé¼┬ó├ù┬ó ├ù┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥. "
                            "├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥, ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬¥ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥, ├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├à┬╕ ├ù┬ñ├ù┬¬├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├à┬╛├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬º├âΓÇö├óΓé¼┼ô ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¬. "
                            "├ù┬É├ù┬¥ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├ù┬¬ ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ª├ù┬ó ├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕. ├ù┬É├ù┬¥ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬¥ UI ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ª├ù┬ó ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├ù┬¿. "
                            "├ù┬É├ù┬¥ ├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¿ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬º├âΓÇö├óΓé¼┼ô├ù┬¬."
                        )},
                        {"role": "user", "content": [
                            {"type": "text", "text": caption or "├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓé¼┬ó?"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}", "detail": "high"}}
                        ]}
                    ],
                    "max_tokens": 800,
                    "temperature": 0.5
                },
                timeout=30
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    response = data["choices"][0]["message"]["content"]
                else:
                    err = await r.text()
                    response = f"├â┬ó├é┬¥├àΓÇÖ AI error ({r.status})"
        try:
            await typing_msg.edit_text(f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì <b>├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥</b>\n├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n{response}")
        except:
            await typing_msg.edit_text(f"├â┬░├à┬╕├óΓé¼┬¥├é┬ì ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥\n\n{response}")
        await _pg_ok(
            f"INSERT INTO chat_messages (user_id,user_name,message,response) "
            f"VALUES ({uid},'{name.replace(chr(39),'')}','[PHOTO] {caption[:200].replace(chr(39),'')}','{response[:500].replace(chr(39),'')}') "
        )
        if uid != OWNER_ID:
            try:
                await bot.send_message(OWNER_ID, f"├â┬░├à┬╕├óΓé¼┼ô├é┬╕ {name} ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í:\n{caption[:200]}")
            except: pass
    except Exception as e:
        logging.error(f"Photo handler error: {e}")
        await typing_msg.edit_text(f"├â┬ó├é┬¥├àΓÇÖ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥: {str(e)[:200]}\n\n├ù┬á├ù┬í├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├ù┬É├âΓÇö├óΓé¼┬ó ├ù┬¬├ù┬É├ù┬¿ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├ï┼ô├ù┬º├ù┬í├âΓÇö├ï┼ô.")


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  21. COMPREHENSIVE REPORTS                            ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

@dp.message(Command("full_report"))
async def cmd_full_report(m: types.Message):
    msg = await m.answer("├â┬░├à┬╕├óΓé¼┼ô├à┬á <b>├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É...</b>")
    lines = [f"├â┬░├à┬╕├óΓé¼┼ô├à┬á SLH Full System Report", f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    lines.append("├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É INFRASTRUCTURE ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É")
    if dc:
        containers = dc.containers.list(all=True)
        running = [c for c in containers if c.status == "running"]
        stopped = [c for c in containers if c.status != "running"]
        lines.append(f"Docker: {len(running)} running / {len(stopped)} stopped")
        for c in sorted(containers, key=lambda x: x.name):
            icon = "OK" if c.status == "running" else "DOWN"
            restarts = c.attrs.get("RestartCount", 0)
            lines.append(f"  [{icon}] {c.name} (restarts: {restarts})")
    bridge = await http_get(f"{LOCAL_BRIDGE}/api/health")
    lines.append(f"Local Bridge: {'OK' if bridge else 'DOWN'}")
    railway = await http_get(f"{RAILWAY_API}/api/health")
    lines.append(f"Railway API: {'OK' if railway and railway.get('status')=='ok' else 'DOWN'}")

    lines.append("")
    lines.append("├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É ESP32 DEVICES ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É")
    esp = await http_get(f"{LOCAL_BRIDGE}/api/esp/status")
    if esp and esp.get("devices"):
        for d in esp["devices"]:
            lines.append(f"  {d['device_id']}: {d.get('status')} (IP: {d.get('ip','?')}, RSSI: {d.get('rssi','?')})")
    serial = await http_get(f"{LOCAL_BRIDGE}/api/serial/status")
    if serial:
        lines.append(f"Serial: {'Connected' if serial.get('connected') else 'Disconnected'} ({serial.get('port','?')})")

    lines.append("")
    lines.append("├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É TASK BOARD ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É")
    for status_name, icon in TASK_STATUSES.items():
        cnt = await _pg_val(f"SELECT count(*) FROM task_board WHERE status='{status_name}'")
        lines.append(f"  {icon} {status_name}: {(cnt or '0').strip()}")
    recent_tasks = await _pg_val(
        "SELECT id,title,status,assigned_name FROM task_board WHERE status!='done' ORDER BY "
        "CASE priority WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 WHEN 'normal' THEN 2 ELSE 3 END LIMIT 10"
    )
    if recent_tasks and recent_tasks.strip():
        lines.append("  Active tasks:")
        for line in recent_tasks.strip().split("\n"):
            cols = line.split("|")
            if len(cols) >= 4:
                lines.append(f"    #{cols[0].strip()} {cols[1].strip()[:30]} [{cols[2].strip()}] -> {cols[3].strip() or 'unassigned'}")

    lines.append("")
    lines.append("├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É USERS & ACCESS ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É")
    users = await _pg_val("SELECT user_id,full_name,role,team,trust_level,is_active FROM abac_users ORDER BY user_id")
    if users:
        for line in users.strip().split("\n"):
            cols = line.split("|")
            if len(cols) >= 6:
                active = "ACTIVE" if cols[5].strip() == "t" else "INACTIVE"
                lines.append(f"  {cols[1].strip()} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {cols[2].strip()} | team:{cols[3].strip()} | trust:{cols[4].strip()} | {active}")
    policies = await _pg_val("SELECT count(*) FROM abac_policies WHERE is_active=true")
    lines.append(f"Active Policies: {(policies or '0').strip()}")
    cmds = await _pg_val("SELECT count(*) FROM command_attrs")
    lines.append(f"Commands Defined: {(cmds or '0').strip()}")

    lines.append("")
    lines.append("├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É GITHUB CONNECTIONS ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É")
    gh = await _pg_val("SELECT user_name,gh_type,gh_value FROM user_github ORDER BY created_at DESC LIMIT 10")
    if gh and gh.strip():
        for line in gh.strip().split("\n"):
            cols = line.split("|")
            if len(cols) >= 3:
                lines.append(f"  {cols[0].strip()} -> {cols[1].strip()}: {cols[2].strip()}")
    else:
        lines.append("  No GitHub connections yet")

    lines.append("")
    lines.append("├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É AI CHAT STATS ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É")
    chat_cnt = await _pg_val("SELECT count(*) FROM chat_messages")
    chat_today = await _pg_val("SELECT count(*) FROM chat_messages WHERE created_at >= CURRENT_DATE")
    lines.append(f"Total messages: {(chat_cnt or '0').strip()} | Today: {(chat_today or '0').strip()}")

    full_text = "\n".join(lines)
    doc = BufferedInputFile(full_text.encode("utf-8"), filename=f"full_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt")
    await m.answer_document(doc, caption="├â┬░├à┬╕├óΓé¼┼ô├à┬á Full System Report")
    try:
        await msg.delete()
    except: pass
    await audit(m.from_user.id, "/full_report", "ok")


@dp.message(Command("evening_report"))
async def cmd_evening_report(m: types.Message):
    text = f"<b>├â┬░├à┬╕├àΓÇÖ├óΓÇ₧┬ó ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ó├ù┬¿├âΓÇö├óΓé¼╦£ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</b>\n"
    text += "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
    done_today = await _pg_val("SELECT count(*) FROM task_board WHERE status='done' AND completed_at >= CURRENT_DATE")
    new_today = await _pg_val("SELECT count(*) FROM task_board WHERE created_at >= CURRENT_DATE")
    open_tasks = await _pg_val("SELECT count(*) FROM task_board WHERE status='open'")
    progress = await _pg_val("SELECT count(*) FROM task_board WHERE status='in_progress'")
    blocked = await _pg_val("SELECT count(*) FROM task_board WHERE status='blocked'")
    text += f"<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥:</b>\n"
    text += f"  ├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥: {(done_today or '0').strip()}\n"
    text += f"  ├â┬░├à┬╕├óΓé¼┼ô├é┬¥ ├ù┬á├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥: {(new_today or '0').strip()}\n"
    text += f"  ├â┬░├à┬╕├à┬╕├é┬ó ├ù┬ñ├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬: {(open_tasks or '0').strip()}\n"
    text += f"  ├â┬░├à┬╕├óΓé¼┬¥├é┬╡ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥: {(progress or '0').strip()}\n"
    text += f"  ├â┬░├à┬╕├óΓé¼┬¥├é┬┤ ├âΓÇö├óΓé¼ΓÇ¥├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬: {(blocked or '0').strip()}\n\n"
    completed = await _pg_val(
        "SELECT id,title,assigned_name FROM task_board WHERE status='done' AND completed_at >= CURRENT_DATE"
    )
    if completed and completed.strip():
        text += "<b>├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥:</b>\n"
        for line in completed.strip().split("\n"):
            cols = line.split("|")
            if len(cols) >= 3:
                text += f"  ├â┬ó├óΓÇÜ┬¼├é┬ó #{cols[0].strip()} {cols[1].strip()[:30]} ({cols[2].strip() or '?'})\n"
    chat_today = await _pg_val("SELECT count(*) FROM chat_messages WHERE created_at >= CURRENT_DATE")
    text += f"\n<b>├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£ AI:</b> {(chat_today or '0').strip()} ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬¥\n"
    if dc:
        containers = dc.containers.list(all=True)
        stopped = [c for c in containers if c.status != "running"]
        if stopped:
            text += f"\n<b>├â┬ó├à┬í├é┬á├»┬╕┬Å ├ù┬º├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├ù┬⌐├ù┬á├ù┬ñ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó:</b> {', '.join(c.name for c in stopped[:5])}\n"
    text += f"\n├â┬░├à┬╕├àΓÇÖ├óΓé¼┬ª ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├ù┬¿: /morning | /tasks"
    await m.answer(text[:4000])


# ├â┬ó├óΓé¼┬ó├óΓé¼┬¥├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├óΓé¼ΓÇ¥
# ├â┬ó├óΓé¼┬ó├óΓé¼╦£  22. GUIDES ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Welcome, Agents, Parallel Work          ├â┬ó├óΓé¼┬ó├óΓé¼╦£
# ├â┬ó├óΓé¼┬ó├à┬í├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬¥

@dp.message(Command("welcome"))
async def cmd_welcome(m: types.Message):
    await m.answer(
        "<b>├â┬░├à┬╕├óΓé¼╦£├óΓé¼┬╣ ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├à┬í ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬É ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ SLH Spark!</b>\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        "<b>├â┬░├à┬╕├à┬í├óΓÇÜ┬¼ ├âΓÇö├óΓé¼┬¥├ù┬¬├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 5 ├âΓÇö├óΓé¼┼ô├ù┬º├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n\n"
        "<b>1├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ /create_me</b>\n"
        "├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿ ├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├óΓé¼ΓÇ¥├ù┬⌐├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ ├ù┬ó├ù┬¥ ├âΓÇö├óΓé¼┬¥├ù┬¿├ù┬⌐├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬ª├ù┬ñ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥.\n\n"
        "<b>2├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥-GitHub ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í:</b>\n"
        "<code>/connect_github YOUR_USERNAME</code>\n"
        "├ù┬É├âΓÇö├óΓé¼┬ó: <code>/connect_github https://github.com/user/repo</code>\n\n"
        "<b>3├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú ├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô:</b>\n"
        "<code>/analyze repo-name</code>\n"
        "├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬¬├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕ ├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬ + 5 ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¬ AI\n\n"
        "<b>4├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú ├ù┬¿├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬:</b>\n"
        "/tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó\n"
        "/task_new ├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¬├ù┬¿├ù┬¬ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓÇ₧┬ó├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬¿├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥\n"
        "/task_pick ID ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬º├âΓÇö├óΓé¼ΓÇ¥├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥\n\n"
        "<b>5├»┬╕┬Å├â┬ó├åΓÇÖ├é┬ú ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥:</b>\n"
        "├ù┬ñ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├ù┬¬ ├âΓÇö├ï┼ô├ù┬º├ù┬í├âΓÇö├ï┼ô ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬ó├ù┬ñ├ù┬⌐├âΓÇö├óΓÇ₧┬ó ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ AI ├âΓÇö├óΓÇ₧┬ó├ù┬ó├ù┬á├âΓÇö├óΓé¼┬¥!\n"
        "├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼Γäó├ù┬¥ ├âΓÇö├àΓÇ£├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ <b>├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í</b> ├ù┬⌐├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥ ├â┬░├à┬╕├óΓé¼┼ô├é┬╕\n\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í:</b>\n"
        "/my_access ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬¿├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╕ ├âΓÇö├àΓÇ£├âΓÇö├à┬í\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬í ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        "/guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É\n"
        "/esp_guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ESP32\n"
        "/agent_guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/parallel_guide ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¬ ├ù┬ó├ù┬¥ AI\n"
        "/maximize ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬º├ù┬í├âΓÇö├óΓé¼┬ó├ù┬¥\n\n"
        "<b>├â┬░├à┬╕├à┬╜├óΓé¼┬░ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├âΓÇö├à┬╕ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥:</b>\n"
        "/invite ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£ ├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬º ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼ΓÇ£├âΓÇö├à┬╛├ù┬á├âΓÇö├óΓé¼┬¥ ├ù┬É├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓÇ₧┬ó\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬╛ ├ù┬ª├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├ù┬ó├âΓÇö├óΓé¼ΓÇ£├ù┬¿├âΓÇö├óΓé¼┬¥?</b>\n"
        "├ù┬ñ├ù┬⌐├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô ├âΓÇö├óΓé¼┬║├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬¥├ù┬⌐├ù┬É├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í ├âΓÇö├óΓé¼┬║├ù┬É├âΓÇö├à┬╕ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬É├ù┬á├âΓÇö├óΓÇ₧┬ó ├ù┬É├ù┬ó├ù┬á├âΓÇö├óΓé¼┬¥! ├â┬░├à┬╕├é┬ñ├óΓé¼ΓÇ£"
    )


@dp.message(Command("parallel_guide"))
async def cmd_parallel_guide(m: types.Message):
    await m.answer(
        "<b>├â┬ó├à┬í├é┬í ├ù┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¬ ├ù┬ó├ù┬¥ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó AI</b>\n"
        "├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü├â┬ó├óΓé¼┬¥├é┬ü\n\n"
        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬╣ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í 1 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó:</b>\n"
        "├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬º├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼╦£├âΓÇö├à┬╛├ù┬º├âΓÇö├óΓé¼╦£├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£\n"
        "<code>/task_new Fix auth bug | Login fails | auth | urgent\n"
        "/task_new Add dark mode | UI feature | frontend | normal\n"
        "/task_new Write tests | Coverage low | testing | high</code>\n"
        "├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├âΓÇö├à┬╕: /task_pick ID ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô ├â┬ó├óΓé¼┬á├óΓé¼Γäó /task_done ID\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬╣ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í 2 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Agent Hub:</b>\n"
        "├ù┬¿├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¥ ├ù┬í├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┬║├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├óΓé¼┬ó├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├ù┬⌐├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬:\n"
        "<code>/register_agent CodeBot worker\n"
        "/register_agent TestBot tester\n"
        "/register_agent DocBot documenter\n"
        "/dispatch_task CodeBot Fix the payment module\n"
        "/dispatch_task TestBot Write integration tests\n"
        "/dispatch_task DocBot Update API docs</code>\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬╣ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í 3 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ GitHub Analysis Pipeline:</b>\n"
        "├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ£├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├â┬ó├óΓé¼┬á├óΓé¼Γäó AI ├âΓÇö├à┬╛├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├ù┬ª├ù┬¿ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¬:\n"
        "<code>/connect_github my-username\n"
        "/analyze broken-project\n"
        "/review broken-project</code>\n"
        "├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├àΓÇ£├ù┬ñ├âΓÇö├óΓÇ₧┬ó ├âΓÇö├óΓé¼┬¥├âΓÇö├à┬╛├âΓÇö├à┬╛├ù┬ª├ù┬É├âΓÇö├óΓÇ₧┬ó├ù┬¥, ├ù┬ª├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├âΓÇö├óΓé¼╦£-/task_new\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬╣ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í 4 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í + AI:</b>\n"
        "├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├ù┬⌐├âΓÇö├àΓÇ£ ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓé¼┬á├óΓé¼Γäó AI ├âΓÇö├à┬╛├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├ù┬ª├âΓÇö├óΓÇ₧┬ó├ù┬ó ├ù┬ñ├ù┬¬├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╕\n"
        "├ù┬É├ù┬ñ├ù┬⌐├ù┬¿ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├ù┬í├âΓÇö├óΓÇ₧┬ó├ù┬ú ├âΓÇö├óΓé¼┬║├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ ├âΓÇö├àΓÇ£├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓé¼┬ó├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¿ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬ó├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬¥\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬╣ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í 5 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ Docker Orchestration:</b>\n"
        "├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ ├ù┬É├ù┬¬ ├âΓÇö├óΓé¼┬║├âΓÇö├àΓÇ£ ├âΓÇö├óΓé¼┬¥├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓé¼┬ó├ù┬¬├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô:\n"
        "<code>/status ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬¿├ù┬É├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├ù┬¿├ù┬Ñ\n"
        "/restart service ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬ó├âΓÇö├àΓÇ£ ├âΓÇö├à┬╛├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┼ô├ù┬⌐\n"
        "/logs service 50 ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬º ├ù┬⌐├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬É├âΓÇö├óΓé¼┬ó├ù┬¬\n"
        "/heal ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬¬├ù┬º├âΓÇö├à┬╕ ├ù┬É├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├óΓÇ₧┬ó├ù┬¬</code>\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┬¥├é┬╣ ├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├à┬í 6 ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ESP32 Fleet:</b>\n"
        "├ù┬á├âΓÇö├óΓé¼┬¥├âΓÇö├àΓÇ£ 100 ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├âΓÇö├ï┼ô:\n"
        "<code>/esp_ports ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├à┬╛├ù┬ª├ù┬É ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬║├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬¥\n"
        "/esp_flash COM5 ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬ª├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£ firmware\n"
        "/esp_serial PING ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬º ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬¿\n"
        "/esp_pair DEVICE ├â┬ó├óΓé¼┬á├óΓé¼Γäó ├ù┬ª├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬⌐├ù┬¬├âΓÇö├à┬╛├ù┬⌐</code>\n\n"

        "<b>├â┬░├à┬╕├óΓé¼┼ô├à┬á ├ù┬¬├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┼ô ├ù┬¬├ù┬ó├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£:</b>\n"
        "/morning ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┬ó├ù┬º├ù┬¿\n"
        "/daily_report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├à┬╛├âΓÇö├óΓÇ₧┬ó\n"
        "/evening_report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ ├ù┬ó├ù┬¿├âΓÇö├óΓé¼╦£\n"
        "/full_report ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó\"├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É ├âΓÇö├óΓé¼┬║├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├ù┬Ñ\n"
        "/audit ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬í├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼┬║├âΓÇö├óΓé¼┬ó├ù┬¥ Agent Hub"
    )


WELCOME_MESSAGE = (
    "├â┬░├à┬╕├óΓé¼╦£├óΓé¼┬╣ <b>├âΓÇö├óΓé¼╦£├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├à┬í ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼╦£├ù┬É ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬ SLH Spark!</b>\n\n"
    "├ù┬º├âΓÇö├óΓÇ₧┬ó├âΓÇö├óΓé¼╦£├âΓÇö├àΓÇ£├ù┬¬ ├âΓÇö├óΓé¼Γäó├âΓÇö├óΓÇ₧┬ó├ù┬⌐├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├à┬╛├ù┬ó├ù┬¿├âΓÇö├óΓé¼┬║├ù┬¬. ├âΓÇö├óΓé¼┬¥├ù┬á├âΓÇö├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┬¥ ├ù┬⌐├ù┬É├ù┬ñ├ù┬⌐├ù┬¿ ├âΓÇö├àΓÇ£├ù┬ó├ù┬⌐├âΓÇö├óΓé¼┬ó├ù┬¬:\n\n"
    "├â┬░├à┬╕├óΓé¼┼ô├óΓé¼┬╣ /tasks ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├à┬╛├âΓÇö├ï┼ô├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├ù┬ñ├âΓÇö├óΓÇ₧┬ó\n"
    "├â┬░├à┬╕├óΓé¼┬¥├óΓé¼ΓÇ¥ /connect_github ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼╦£├ù┬¿ ├ù┬¿├âΓÇö├óΓÇ₧┬ó├ù┬ñ├âΓÇö├óΓé¼┬ó\n"
    "├â┬░├à┬╕├óΓé¼┬¥├é┬ì /analyze ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├ù┬á├âΓÇö├óΓÇ₧┬ó├ù┬¬├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼ΓÇ¥ AI ├âΓÇö├àΓÇ£├ù┬ñ├ù┬¿├âΓÇö├óΓé¼┬ó├âΓÇö├óΓÇ₧┬ó├ù┬º├âΓÇö├ï┼ô\n"
    "├â┬░├à┬╕├óΓé¼┼ô├é┬╕ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├ù┬ª├âΓÇö├óΓÇ₧┬ó├âΓÇö├àΓÇ£├âΓÇö├óΓé¼┬ó├ù┬¥ ├âΓÇö├à┬╛├ù┬í├âΓÇö├à┬í ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ AI ├âΓÇö├óΓÇ₧┬ó├ù┬á├ù┬¬├âΓÇö├óΓé¼ΓÇ¥\n"
    "├â┬░├à┬╕├óΓé¼Γäó├é┬¼ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥ ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├âΓÇö├óΓé¼┬¥ ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ AI ├âΓÇö├óΓÇ₧┬ó├ù┬ó├ù┬á├âΓÇö├óΓé¼┬¥\n\n"
    "/welcome ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├à┬╛├âΓÇö├óΓé¼┼ô├ù┬¿├âΓÇö├óΓÇ₧┬ó├âΓÇö├à┬í ├âΓÇö├à┬╛├âΓÇö├àΓÇ£├ù┬É\n"
    "/my_access ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ ├âΓÇö├óΓé¼┬¥├ù┬ñ├ù┬º├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├âΓÇö├óΓé¼┬ó├ù┬¬ ├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├à┬í"
)


@dp.message(Command("send_welcome"))
async def cmd_send_welcome(m: types.Message):
    if m.from_user.id != OWNER_ID:
        return
    parts = m.text.split()
    if len(parts) < 2:
        return await m.answer("Usage: /send_welcome USER_ID")
    target = int(parts[1])
    try:
        await bot.send_message(target, WELCOME_MESSAGE)
        await m.answer(f"├â┬ó├àΓÇ£├óΓé¼┬ª ├âΓÇö├óΓé¼┬¥├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼┼ô├ù┬ó├ù┬¬ Welcome ├ù┬á├ù┬⌐├âΓÇö├àΓÇ£├âΓÇö├óΓé¼ΓÇ¥├âΓÇö├óΓé¼┬¥ ├âΓÇö├àΓÇ£-{target}")
    except Exception as e:
        await m.answer(f"├â┬ó├é┬¥├àΓÇÖ {str(e)[:200]}")


# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
#  MAIN ENTRY POINT
# ├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É├â┬ó├óΓé¼┬ó├é┬É
async def main():
    global BOT_USERNAME
    me = await bot.get_me()
    BOT_USERNAME = me.username or ""
    logging.info(f"SLH Admin Bot v53 Task+AI starting as @{BOT_USERNAME} ├â┬ó├óΓÇÜ┬¼├óΓé¼┬¥ 90+ commands")
    await _pg_ok(
        "CREATE TABLE IF NOT EXISTS task_board ("
        "  id SERIAL PRIMARY KEY, title TEXT NOT NULL, description TEXT DEFAULT '',"
        "  status TEXT DEFAULT 'open', priority TEXT DEFAULT 'normal',"
        "  project TEXT DEFAULT 'general', assigned_to BIGINT, assigned_name TEXT DEFAULT '',"
        "  created_by BIGINT, created_by_name TEXT DEFAULT '',"
        "  created_at TIMESTAMP DEFAULT NOW(), updated_at TIMESTAMP DEFAULT NOW(),"
        "  completed_at TIMESTAMP, notes TEXT DEFAULT ''"
        ");"
        "CREATE TABLE IF NOT EXISTS chat_messages ("
        "  id SERIAL PRIMARY KEY, user_id BIGINT, user_name TEXT,"
        "  message TEXT, response TEXT, created_at TIMESTAMP DEFAULT NOW()"
        ")"
    )
    await dp.start_polling(bot, drop_pending_updates=True)
import datetime
import aiohttp
import os

# ====================== SYSTEM DOCTOR + REMOTE CONTROL ======================
@dp.message(Command('system_doctor', 'doctor', 'diagnose', 'status'))
async def cmd_system_doctor(message: types.Message):
    report = ["├â┬░├à┬╕├é┬⌐├é┬║ **SLH System Doctor**", f"├â┬░├à┬╕├óΓé¼┬ó├óΓé¼Γäó {datetime.datetime.datetime.now().strftime('%H:%M:%S')}"]

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(6)) as session:
            async with session.get("http://10.0.0.7:8765/status") as resp:
                data = await resp.json()
                report.append(f"├â┬ó├àΓÇ£├óΓé¼┬ª Bridge: **├ù┬ó├âΓÇö├óΓé¼┬ó├âΓÇö├óΓé¼╦£├âΓÇö├óΓé¼┼ô**")
    except:
        report.append("├â┬ó├é┬¥├àΓÇÖ Bridge: Not reachable")

    report.append("├â┬░├à┬╕├óΓé¼╦£├é┬ª Junior-Explorer: Registered & Ready")
    report.append("├â┬░├à┬╕├à┬╜├óΓé¼┼í Tamagotchi-Nexus: Birthday Mode Activated")

    await message.reply_text("\n".join(report))


@dp.message(Command('restart_system', 'reboot', 'power_restart'))
async def cmd_restart_system(message: types.Message):
    if message.from_user.id != 224223270:
        return await message.reply_text("├â┬ó├é┬¥├àΓÇÖ Only owner allowed")
    await message.reply_text("├â┬░├à┬╕├óΓé¼┬¥├óΓé¼┼╛ Restarting full SLH system...")
    os.system('powershell -ExecutionPolicy Bypass -File "D:\\SLH_ECOSYSTEM\\power-restart.ps1"')
    await message.reply_text("├â┬ó├àΓÇ£├óΓé¼┬ª Restart command sent")
if __name__ == "__main__":
    asyncio.run(main())


