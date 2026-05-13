# === SLH MASTER BOT v3.14 FINAL  RAILWAY READY + FULL FEATURES ===
import asyncio, logging, os, subprocess, json, functools, datetime, csv
import httpx
from dotenv import load_dotenv; from bsc_client import get_token_price; from bsc_client import get_token_price
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import redis as redis_lib

load_dotenv()

TOKEN = os.getenv("MASTER_BOT_TOKEN", "").strip()
ALLOWED_IDS = [int(x.strip()) for x in os.getenv("ALLOWED_IDS", "224223270,8789977826,1087968824").split(",") if x.strip()]
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
REDIS_URL = os.getenv("REDIS_URL", "redis://slh-redis-v3:6379")
FASTAPI_URL = os.getenv("RAILWAY_FASTAPI_URL", "https://slh-fastapi-production.up.railway.app")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_PATH = "/webhook"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Redis
r = None
try:
    r = redis_lib.Redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=5)
    r.ping()
    log.info("✅ Redis Connected")
except:
    log.warning("Redis not available")

# ====================== Helpers ======================
async def get_user_osif(uid):
    if not r: return 0
    return float(r.get(f"user:{uid}:osif") or 0)

async def get_user_work_today(uid):
    if not r: return 0
    today = datetime.date.today().isoformat()
    return float(r.get(f"user:{uid}:work:{today}") or 0)

async def call_fastapi(endpoint, method="GET", json_data=None):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            url = f"{FASTAPI_URL}{endpoint}"
            if method == "POST":
                resp = await client.post(url, json=json_data)
            else:
                resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        return {"error": str(e)}

def auth():
    def deco(func):
        @functools.wraps(func)
        async def wrap(msg: Message, **kwargs):
            if msg.from_user.id not in ALLOWED_IDS:
                await msg.answer("🔒 גישה חסומה")
                return
            return await func(msg, **kwargs)
        return wrap
    return deco

# ====================== Main Menu ======================
def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📦 Containers", callback_data="cat_containers"),
        InlineKeyboardButton(text="📊 Dashboard", callback_data="cat_dashboard")
    )
    builder.row(
        InlineKeyboardButton(text="🧠 Memory & Journal", callback_data="cat_memory"),
        InlineKeyboardButton(text="👥 Users & Admin", callback_data="cat_users")
    )
    builder.row(
        InlineKeyboardButton(text="🛠️ System Ops", callback_data="cat_ops"),
        InlineKeyboardButton(text="🪙 OSIF (Time Coin)", callback_data="cat_osif")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Leaderboard", callback_data="cat_leaderboard"),
        InlineKeyboardButton(text="🛡️ Invest Check", callback_data="cat_invest")
    )
    builder.row(
        InlineKeyboardButton(text="🔧 Contribute", callback_data="cat_contribute"),
        InlineKeyboardButton(text="📘 Full Guide", callback_data="cat_guide")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(
        "🔥 <b>SLH Master Bot v3.14</b>\n\n"
        "בחר קטגוריה:",
        reply_markup=main_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("menu"))
async def cmd_menu(msg: Message):
    await cmd_start(msg)

@dp.callback_query()
async def process_callback(call: CallbackQuery):
    if call.data == "cat_containers":
        try:
            result = subprocess.run(["docker","ps","-a","--format","{{.Names}} | {{.Status}}"], capture_output=True, text=True, timeout=10)
            await call.message.answer(f"📦 <b>Containers:</b>\n{result.stdout or 'אין'}")
        except Exception as e:
            await call.message.answer(f"שגיאה: {e}")
    elif call.data == "cat_dashboard":
        try:
            result = subprocess.run(["docker","ps","-a","--format","{{.Names}} {{.Status}}"], capture_output=True, text=True, timeout=5)
            containers = result.stdout.strip().splitlines()
            running = sum(1 for c in containers if "Up" in c)
            uid = str(call.from_user.id)
            osif = await get_user_osif(uid)
            today = await get_user_work_today(uid)
            await call.message.answer(f"📊 <b>Dashboard</b>\n🐳 Containers: {running}/{len(containers)}\n🪙 OSIF: {osif} total / {today} today")
        except Exception as e:
            await call.message.answer(f"Error: {e}")
    elif call.data == "cat_memory":
        await call.message.answer("🧠 <b>Memory & Journal</b>\n\n/remember &lt;fact&gt;\n/facts\n/forget &lt;fact&gt;\n/journal\n/myday\n/summary")
    elif call.data == "cat_users":
        await call.message.answer("👥 <b>Users & Admin</b>\n\n/id\n/request &lt;role&gt;\n/requests\n/approve &lt;id&gt;\n/reject &lt;id&gt;\n/adduser &lt;id&gt; &lt;role&gt;\n/deluser &lt;id&gt;\n/listusers\n/broadcast &lt;msg&gt;")
    elif call.data == "cat_ops":
        await call.message.answer("🛠️ <b>System Ops</b>\n\n/status\n/health\n/ps\n/logs &lt;name&gt;\n/restart &lt;name&gt;\n/exec &lt;container&gt; &lt;cmd&gt;\n/deploy\n/discover\n/fix &lt;container&gt;")
    elif call.data == "cat_osif":
        await call.message.answer("🪙 <b>OSIF (Time Coin)</b>\n\n/startwork\n/stopwork\n/mytime\n/osifrate")
    elif call.data == "cat_leaderboard":
        if r:
            keys = r.keys("user:*:osif")
            scores = []
            for k in keys:
                uid = k.split(":")[1]
                osif = float(r.get(k) or 0)
                scores.append((uid, osif))
            scores.sort(key=lambda x: x[1], reverse=True)
            board = "\n".join(f"• {uid}: {osif} OSIF" for uid, osif in scores[:5])
            await call.message.answer(f"🏆 <b>Leaderboard (OSIF):</b>\n{board}" if board else "אין נתונים")
        else:
            await call.message.answer("Redis not available")
    elif call.data == "cat_invest":
        await call.message.answer(
            "🛡️ <b>שאלות ההשקעה שלי</b>\n\n"
            "1. <b>כמה תרצה להשקיע?</b> (סכום)\n"
            "2. <b>כמה זה מתוך התיק הכללי שלך?</b> (%)\n"
            "3. <b>לכמה זמן תרצה להשקיע?</b>\n"
            "4. <b>מה צפי הרווח שלך מהמדד בו אתה משקיע לתקופה זו?</b>\n"
            "5. <b>אילו הצעות השקעה דומות ראית/קיבלת?</b>\n"
            "6. <b>מה משך אותך בהן?</b>\n\n"
            "🎯 <b>ניתוח:</b> אבדוק את ההשקעות שלך או של הסוכן, ואציע הצעה ריאלית נגדית מוצלחת יותר.",
            parse_mode=ParseMode.HTML
        )
    elif call.data == "cat_contribute":
        await call.message.answer("🔧 <b>Contribute</b>\n\n/contribute &lt;project_name&gt; &lt;description&gt;")
    elif call.data == "cat_guide":
        await call.message.answer("📘 <b>Full Guide</b>\n\nהכל מופיע בתפריט הראשי (/menu).")
    await call.answer()

# ====================== Transparency Commands ======================
@dp.message(Command("ido"))
async def cmd_ido(msg: Message):
    await msg.answer(
        "<b>🪙 SLH IDO  סיכום השקעה</b>\n\n"
        "• <b>טוקן:</b> SLH\n"
        "• <b>רשת:</b> BSC (Binance Smart Chain)\n"
        "• <b>כתובת חוזה:</b> <code>0xACb0A09414CEA1C879c67bB7A877E4e19480f022</code>\n"
        "• <b>פלטפורמה:</b> PinkSale\n"
        "• <b>מחיר IDO:</b> 0.000004 BNB (~0.05)\n"
        "• <b>מחיר Listing:</b> 0.000005 BNB (~0.066)\n"
        "• <b>Soft Cap:</b> 20 BNB (~50,000)\n"
        "• <b>Hard Cap:</b> 150 BNB (~370,000)\n"
        "• <b>מינימום/מקסימום לארנק:</b> 0.05  5 BNB\n"
        "• <b>Vesting:</b> 20% TGE + 20% כל חודש למשך 4 חודשים\n"
        "• <b>נעילת נזילות:</b> 365 ימים ב-PinkLock\n"
        "• <b>אודיט:</b> SolidProof (יפורסם)\n"
        "• <b>ישות משפטית:</b> Marshall Islands DAO LLC\n\n"
        "<a href='https://slh-nft.com/ido.html'>למדריך המלא באתר</a>",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("vesting"))
async def cmd_vesting(msg: Message):
    await msg.answer(
        "<b>📅 לוח שחרור SLH (Vesting)</b>\n\n"
        "השקעת 1 BNB → 250,000 SLH:\n\n"
        "• TGE (יום 14): 50,000 SLH (20%)\n"
        "• TGE + 30 יום: 50,000 SLH (40%)\n"
        "• TGE + 60 יום: 50,000 SLH (60%)\n"
        "• TGE + 90 יום: 50,000 SLH (80%)\n"
        "• TGE + 120 יום: 50,000 SLH (100%  חופשי)\n\n"
        "השחרור אוטומטי דרך החוזה. אין צורך בפעולה מצידך.",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("risks"))
async def cmd_risks(msg: Message):
    await msg.answer(
        "<b>⚠️ 10 סיכונים שחובה להכיר</b>\n\n"
        "1. אובדן הון מלא  ערך SLH עלול לרדת לאפס.\n"
        "2. סיכון חוזה חכם  גם אודיט לא מונע באגים.\n"
        "3. סיכון רגולטורי בישראל  רשות ני\"ע עלולה להתערב.\n"
        "4. סיכון רגולטורי בינ\"ל  SEC/Treasury עלולים לפעול.\n"
        "5. תנודתיות  50%+ ירידה תוך שבוע אפשרית.\n"
        "6. Vesting  80% מה-SLH נעולים ל-4 חודשים.\n"
        "7. Soft Cap לא נסגר  החזר אוטומטי, אבל בינתיים BNB נעול.\n"
        "8. Phishing  לעולם לא נבקש seed. זהירות מהתחזות.\n"
        "9. בחירת רשת שגויה  שליחת BNB ב-ERC20 במקום BEP20 = אובדן.\n"
        "10. ספקים חיצוניים  AI, Telegram, PinkSale  תלות בצד ג'.\n\n"
        "<b>אנחנו לא מבטיחים רווח. השקיעו רק מה שאתם מוכנים להפסיד.</b>",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("verify"))
async def cmd_verify(msg: Message):
    await msg.answer(
        "<b>🔍 אימות עצמאי  8 צעדים</b>\n\n"
        "1. <a href='https://bscscan.com/token/0xACb0A09414CEA1C879c67bB7A877E4e19480f022'>בדוק את כתובת הטוקן ב-BscScan</a>\n"
        "2. בדוק Holders  אסור שיהיה ארנק אחד >50%.\n"
        "3. <a href='https://gnosis-safe.io/app/bnb:0x9DD8aF7Ac0f601CD473422311b2942DAE9D0BD09'>בדוק Treasury Safe</a>  signers ≥ 2/3.\n"
        "4. בדוק Audit (יום 12)  חפש SolidProof.\n"
        "5. בדוק LP Lock (יום 14)  PinkLock, duration ≥ 365.\n"
        "6. בדוק MIDAO Certificate  midao.org, status = Active.\n"
        "7. בדוק PinkSale Profile  KYC badge.\n"
        "8. בדוק קוד החוזה ב-BscScan  חייב להיות Verified.\n\n"
        "אם משהו לא תואם  צור קשר מיידית.",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("faq"))
async def cmd_faq(msg: Message):
    await msg.answer(
        "<b>❓ שאלות נפוצות</b>\n\n"
        "• מה זה SLH?  טוקן של מערכת SLH Ecosystem.\n"
        "• איזה ארנק?  MetaMask (BSC).\n"
        "• איך קונים BNB?  Bit2C / Binance.\n"
        "• מס בישראל?  25% על רווחי הון במכירה.\n"
        "• חייב KYC?  לא ברמת הפרוטוקול. הבורסות דורשות.\n"
        "• מה אם Soft Cap לא נסגר?  החזר אוטומטי.\n"
        "• איך מוכרים SLH?  PancakeSwap אחרי TGE.\n"
        "• איך רואים את ה-SLH שלי?  MetaMask, Import Token.\n\n"
        "לשאלות נוספות: @SLH_AIR_bot או באתר.",
        parse_mode=ParseMode.HTML
    )

# ====================== FastAPI Status ======================
@dp.message(Command("fastapi"))
@auth()
async def cmd_fastapi(msg: Message):
    data = await call_fastapi("/health")
    await msg.answer(f"🌐 <b>FastAPI Status:</b>\n{json.dumps(data, indent=2, ensure_ascii=False)}")

# ====================== Core Commands ======================
@dp.message(Command("proj"))
@auth()
async def cmd_proj(msg: Message):
    try:
        result = subprocess.run(["docker","ps","-a","--format","{{.Names}} | {{.Status}}"], capture_output=True, text=True, timeout=10)
        await msg.answer(f"📦 Containers:\n{result.stdout or 'אין'}")
    except Exception as e:
        await msg.answer(f"שגיאה: {e}")

@dp.message(Command("status"))
@auth()
async def cmd_status(msg: Message):
    await msg.answer("🟢 SLH Ecosystem v3.14 — Online")

@dp.message(Command("health"))
async def cmd_health(msg: Message):
    await msg.answer("✅ Bot healthy")

@dp.message(Command("ps"))
@auth()
async def cmd_ps(msg: Message):
    await cmd_proj(msg)

@dp.message(Command("logs"))
@auth()
async def cmd_logs(msg: Message):
    name = msg.text.split()[-1] if len(msg.text.split()) > 1 else None
    if not name: await msg.answer("Usage: /logs <container>"); return
    out = subprocess.run(["docker","logs","--tail","30",name], capture_output=True, text=True)
    await msg.answer((out.stdout or out.stderr)[-2000:] or "אין לוגים")

@dp.message(Command("restart"))
@auth()
async def cmd_restart(msg: Message):
    name = msg.text.split()[-1] if len(msg.text.split()) > 1 else None
    if not name: await msg.answer("Usage: /restart <container>"); return
    subprocess.run(["docker","restart",name])
    await msg.answer(f"✅ {name} restarted")

@dp.message(Command("exec"))
@auth()
async def cmd_exec(msg: Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 3: await msg.answer("Usage: /exec <container> <cmd>"); return
    container, cmd = parts[1], parts[2]
    out = subprocess.run(["docker","exec",container] + cmd.split(), capture_output=True, text=True)
    await msg.answer((out.stdout or out.stderr)[:1900] or "OK")

@dp.message(Command("discover"))
@auth()
async def cmd_discover(msg: Message):
    try:
        with open("/app/data/ecosystem_dna.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()[:30]
        projects = {}
        for l in lines[1:]:
            p = l.split(",")[0].strip('"')
            projects[p] = projects.get(p, 0) + 1
        summary = "\n".join(f"• {k}: {v} files" for k, v in projects.items())
        await msg.answer(f"🧬 <b>Ecosystem DNA:</b>\n{summary[:3800]}")
    except Exception as e:
        await msg.answer(f"Error: {e}")

@dp.message(Command("fix"))
@auth()
async def cmd_fix(msg: Message):
    await msg.answer("🔧 Auto-fix (stub)")

@dp.message(Command("task"))
@auth()
async def cmd_task(msg: Message):
    if not r: await msg.answer("Redis not available"); return
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 2:
        tasks = r.lrange("tasks:open", 0, -1)
        await msg.answer("📋 <b>Open Tasks:</b>\n" + "\n".join(f"• {t}" for t in tasks) if tasks else "אין משימות")
        return
    action = parts[1]
    if action == "add" and len(parts) == 3:
        r.lpush("tasks:open", parts[2])
        await msg.answer("✅ משימה נוספה")
    elif action == "done" and len(parts) == 3:
        r.lrem("tasks:open", 0, parts[2])
        r.lpush("tasks:done", parts[2])
        await msg.answer("✅ משימה הושלמה")
    else:
        await msg.answer("Usage: /task add <desc> | /task list | /task done <desc>")

@dp.message(Command("dashboard"))
@auth()
async def cmd_dashboard(msg: Message):
    try:
        result = subprocess.run(["docker","ps","-a","--format","{{.Names}} {{.Status}}"], capture_output=True, text=True, timeout=5)
        containers = result.stdout.strip().splitlines()
        running = sum(1 for c in containers if "Up" in c)
        uid = str(msg.from_user.id)
        osif = await get_user_osif(uid)
        today = await get_user_work_today(uid)
        await msg.answer(f"📊 <b>Dashboard</b>\n🐳 Containers: {running}/{len(containers)}\n🪙 OSIF: {osif} total / {today} today")
    except Exception as e:
        await msg.answer(f"Error: {e}")

@dp.message(Command("guide"))
async def cmd_guide(msg: Message):
    await msg.answer("📘 Guide: All commands in /start")

@dp.message(Command("remember"))
@auth()
async def cmd_remember(msg: Message):
    if not r: await msg.answer("Redis not available"); return
    fact = msg.text.replace("/remember","",1).strip()
    if fact: r.sadd(f"user:{msg.from_user.id}:facts", fact); await msg.answer("🧠 Remembered!")
    else: await msg.answer("Usage: /remember <fact>")

@dp.message(Command("facts"))
@auth()
async def cmd_facts(msg: Message):
    if not r: await msg.answer("Redis not available"); return
    facts = r.smembers(f"user:{msg.from_user.id}:facts")
    await msg.answer("🧠 Facts:\n" + "\n".join(facts) if facts else "No facts")

@dp.message(Command("journal"))
@auth()
async def cmd_journal(msg: Message):
    if not r: await msg.answer("Redis not available"); return
    entries = r.lrange(f"user:{msg.from_user.id}:journal", 0, -1)
    if entries:
        await msg.answer("📔 <b>יומן העבודה שלי:</b>\n" + "\n".join(entries))
    else:
        await msg.answer("אין עדיין רשומות ביומן. כתוב /myday <טקסט> להוספה.")

@dp.message(Command("myday"))
@auth()
async def cmd_myday(msg: Message):
    if not r: await msg.answer("Redis not available"); return
    text = msg.text.replace("/myday","",1).strip()
    if text:
        r.lpush(f"user:{msg.from_user.id}:journal", f"{datetime.date.today()}: {text}")
        r.hincrby(f"baffo:pet:{msg.from_user.id}", "xp", 5)
        await msg.answer("📝 <b>יום העבודה נרשם</b> (+5 XP)")
    else:
        await msg.answer("שימוש: /myday <טקסט>")

@dp.message(Command("leaderboard"))
async def cmd_leaderboard(msg: Message):
    if r:
        keys = r.keys("user:*:osif")
        scores = []
        for k in keys:
            uid = k.split(":")[1]
            osif = float(r.get(k) or 0)
            scores.append((uid, osif))
        scores.sort(key=lambda x: x[1], reverse=True)
        board = "\n".join(f"• {uid}: {osif} OSIF" for uid, osif in scores[:5])
        await msg.answer(f"🏆 <b>Leaderboard (OSIF):</b>\n{board}" if board else "אין נתונים")
    else:
        await msg.answer("Redis not available")

@dp.message(Command("invest"))
async def cmd_invest(msg: Message):
    await msg.answer(
        "🛡️ <b>שאלות ההשקעה שלי</b>\n\n"
        "1. <b>כמה תרצה להשקיע?</b> (סכום)\n"
        "2. <b>כמה זה מתוך התיק הכללי שלך?</b> (%)\n"
        "3. <b>לכמה זמן תרצה להשקיע?</b>\n"
        "4. <b>מה צפי הרווח שלך מהמדד בו אתה משקיע לתקופה זו?</b>\n"
        "5. <b>אילו הצעות השקעה דומות ראית/קיבלת?</b>\n"
        "6. <b>מה משך אותך בהן?</b>\n\n"
        "🎯 <b>ניתוח:</b> אבדוק את ההשקעות שלך או של הסוכן, ואציע הצעה ריאלית נגדית מוצלחת יותר.",
        parse_mode=ParseMode.HTML
    )
    if r:
        r.lpush(f"user:{msg.from_user.id}:investment_checks", str(datetime.datetime.now()))

@dp.message(Command("contribute"))
@auth()
async def cmd_contribute(msg: Message):
    if not r: await msg.answer("Redis not available"); return
    parts = msg.text.split(maxsplit=2)
    if len(parts) == 3:
        r.lpush("contributions:pending", f"{msg.from_user.id}:{parts[1]} - {parts[2]}")
        await msg.answer("✅ תרומה נשלחה לאישור")
    else:
        await msg.answer("Usage: /contribute <project_name> <description>")

# ====================== OSIF ======================
@dp.message(Command("startwork"))
@auth()
async def cmd_startwork(msg: Message):
    if r:
        r.set(f"user:{msg.from_user.id}:session", datetime.datetime.utcnow().isoformat())
        await msg.answer("🟢 Session started!")
    else: await msg.answer("Redis not available")

@dp.message(Command("stopwork"))
@auth()
async def cmd_stopwork(msg: Message):
    if r:
        uid = msg.from_user.id
        start_str = r.get(f"user:{uid}:session")
        if start_str:
            start = datetime.datetime.fromisoformat(start_str)
            delta = (datetime.datetime.utcnow() - start).total_seconds()
            osif_rate = float(r.get("osif_rate") or 10)
            earned = round(delta / 60 * osif_rate, 4)
            r.incrbyfloat(f"user:{uid}:osif", earned)
            r.incrbyfloat(f"user:{uid}:work:{datetime.date.today().isoformat()}", earned)
            r.delete(f"user:{uid}:session")
            await msg.answer(f"⏹️ Session ended. OSIF: +{earned}")
        else: await msg.answer("No active session.")
    else: await msg.answer("Redis not available")

@dp.message(Command("mytime"))
@auth()
async def cmd_mytime(msg: Message):
    uid = msg.from_user.id
    osif = await get_user_osif(uid)
    today = await get_user_work_today(uid)
    await msg.answer(f"🪙 OSIF: {osif} total / {today} today")

@dp.message(Command("osifrate"))
async def cmd_osifrate(msg: Message):
    rate = float(r.get("osif_rate") or 10) if r else 10
    await msg.answer(f"💰 Rate: {rate} OSIF/min")

@dp.message(Command("id"))
async def cmd_id(msg: Message):
    await msg.answer(f"Your ID: {msg.from_user.id}")

@dp.message(Command("backup"))
@auth()
async def cmd_backup(msg: Message):
    await msg.answer("💾 Backup (stub)")


@dp.message(Command("price"))
async def cmd_price(msg: Message):
    data = await get_token_price()
    if data:
        await msg.answer(
            f"<b>💲 SLH Price (Live)</b>\n\n"
            f"• SLH/BNB: {data['slh_bnb']} BNB\n"
            f"• BNB/USD: ${data['bnb_usd']}\n"
            f"• SLH/USD: ${data['slh_usd']}\n\n"
            f"<i>Source: CoinGecko (BNB) + IDO listing price</i>",
            parse_mode=ParseMode.HTML
        )
    else:
        await msg.answer("⚠️ Could not fetch price. Try again later.")


@dp.message(Command("price"))
async def cmd_price(msg: Message):
    data = await get_token_price()
    if data:
        await msg.answer(
            f"<b>💲 SLH Price (Live)</b>\n\n"
            f"• SLH/BNB: {data['slh_bnb']} BNB\n"
            f"• BNB/USD: ${data['bnb_usd']}\n"
            f"• SLH/USD: ${data['slh_usd']}\n\n"
            f"<i>Source: CoinGecko (BNB) + IDO listing price</i>",
            parse_mode=ParseMode.HTML
        )
    else:
        await msg.answer("⚠️ Could not fetch price. Try again later.")

# ====================== AI Chat ======================
@dp.message(F.text & ~F.text.startswith("/"))
async def on_text(msg: Message):
    if msg.chat.type == "private":
        prompt = msg.text
    else:
        user_text = msg.text or ""
        mentioned = (await bot.get_me()).username.lower() in user_text.lower()
        has_question = "?" in user_text
        direct_call = any(word in user_text.lower() for word in ["בוט", "slh", "קלוד", "claude"])
        if not mentioned and not has_question and not direct_call:
            return
        prompt = f"המשתמש {msg.from_user.first_name} שואל בקבוצה: {user_text}\n\nענה בקצרה, בעברית, תוך התמקדות בפרויקט SLH (בלוקצ'יין, NFT, בוטים, השקעות)."
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]},
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
            )
            answer = resp.json()["choices"][0]["message"]["content"]
            escaped = answer.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            await msg.answer(escaped, parse_mode=ParseMode.HTML)
    except:
        await msg.answer("✅ הבוט עובד.")

# ====================== Railway Webhook Setup ======================
async def on_startup():
    if WEBHOOK_URL:
        await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
        log.info(f"Webhook set to {WEBHOOK_URL}{WEBHOOK_PATH}")

async def on_shutdown():
    await bot.delete_webhook()

async def main():
    log.info("🚀 SLH Master Bot v3.14 FINAL")
    if WEBHOOK_URL:
        app = web.Application()
        webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        webhook_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        await on_startup()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
        await site.start()
        await asyncio.Event().wait()
    else:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


