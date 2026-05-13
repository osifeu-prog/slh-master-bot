# 📋 SLH MASTER TODO  כל המשימות מכל הסוכנים

## 🔴 קריטי  לתקן עכשיו
- [ ] **Redis Authentication**  למצוא את ה‑REDIS_URL המלא מ‑Railway (כולל סיסמה) ולהכניס ל‑candidates.
- [ ] **Deploy bot clean**  להריץ `railway up --service slh-master-bot` ולהבטיח עלייה עם `Redis connected`.
- [ ] **FastAPI Redis**  אותו תיקון נדרש גם ב‑slh-fastapi.

## 🟠 משימות פתוחות (Backlog)
- [ ] HEALTH CHECK: להריץ `st` ולוודא שכל השירותים ב‑Railway `Online`.
- [ ] DATABASE SYNC: לוודא ש‑FastAPI מתחבר ל‑PostgreSQL.
- [ ] CLEAN DEPLOY: לפתור את שגיאת 'os error 32' (יש לגבות ולמחוק קבצים נעולים).
- [ ] FINAL REPORT: להפיק דוח מערכת מלא.

## 🟢 כללי
- [ ] לפנות גיבויים ישנים (`slh_master_bot_backup_*`, `*BROKEN*`).
- [ ] לתעד את מפת הפרויקטים ב‑`/remember` דרך הבוט (כשיעבוד).
- [ ] להגדיר הרשאות מנהל לבוט בקבוצת הטלגרם.
- [ ] לכבות `privacy mode` ( `/setprivacy` ב‑@BotFather).
