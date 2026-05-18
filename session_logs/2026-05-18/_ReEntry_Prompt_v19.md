# ReEntry Prompt — KPH Sales OS

**Version:** v19 — 2026-05-18  
**Replaces:** v18

## 📍 Where We Are

תשתית הפיתוח מושלמת. אתר KPIH בפרודקשן עם 10 פרויקטים. מעבר מוצלח לשלב 4 של התוכנית הראשית.

**מצב נוכחי:**
- Plugin stack פעיל: Impeccable + code-review + security-guidance
- claude-mem v13.2.0 עם זיכרון בין סשנים  
- Production site: https://kohphanganinvestmenthub.com
- 3 launchers: cc-kpih, cc-pages, cc-backend עם בידוד זיכרון

## 🎯 המשימה הפתוחה הבאה

**KPR-156 - Phase 4 Data Cleanup** (High priority)
4 באגי תוכן זוהו אחרי deploy של Site Shell

## ⚡ תיעדוף דחוף

1. **חירום אבטחה**: KPH_API_TOKEN נחשף - סיבוב נדרש מחר
2. עדכון ~/.kph_admin_token (mtime May 14, יכול להכיל U+2028)  
3. עדכון Vercel env vars בכל 3 הסביבות (הקלד ידנית, אל תעתיק)

## 🧠 שיטת עבודה נוכחית

- Claude Code עם cc-kpih launcher למשימות KPIH
- security-guidance hook חוסם eval/innerHTML/exec - opt-out עם ENABLE_SECURITY_REMINDER=0
- code-review plugin בודק PRs אוטומטית
- Cross-session memory בונה פסיבית

## 📦 קבצי פרויקט פעילים

```
~/Business/01_Real-Estate-Leads/kpih-website/
├── components/SiteHeader.tsx (56px sticky, RTL-aware)
├── components/Breadcrumb.tsx (40px bilingual)  
├── components/SiteFooter.tsx (3-col, 5 projects by price desc)
├── lib/whatsapp.ts (bilingual link builder)
├── app/projects/[slug]/page.tsx (shell wrapper)
└── CLAUDE.md (gets edited by claude-mem)

~/.claude-mem/settings.json (chmod 600)
~/bin/cc-* launchers
_KPH_MASTER_KNOWLEDGE/CLAUDE_CODE_STACK.md (v2)
```

## 🎬 אקציה מיידית

1. בדוק אם יש הודעות דחופות מ-Liam
2. אם תעבוד על KPIH - השתמש ב-cc-kpih launcher  
3. לפני כל דבר אחר: **טפל בסיבוב הטוקן** - זה חירום אבטחה
4. אחר כך עבור ל-KPR-156 Data Cleanup

**זכור:** אל תעתיק secrets לתוך Vercel - תמיד הקלד ידנית. U+2028 character גרם לבאג בפרודקשן.