# CHANGELOG DELTA — 2026-05-18

**Version:** v1  
**Sessions:** [kpr-150-plugin-stack-week-1, kpr-151-claude-mem-week-2, kpr-153-site-shell-merged]

## מה נעשה

### תשתית פיתוח
- הותקן סטאק תוספים מלא: Impeccable v3.1.1, code-review, security-guidance
- מערכת זיכרון בין-סשנים פועלת עם claude-mem v13.2.0
- Worker על localhost:37777 עם 12 hooks + 21 MCP tools
- יצירת launchers מבודדים לכל repository

### אתר KPIH בפרודקשן  
- רכיבי Site Shell: SiteHeader (56px sticky), Breadcrumb (40px bilingual), SiteFooter (3-col)
- תמיכה דו-לשונית מלאה עם RTL awareness
- 10 פרויקטים חיים באתר עם ניווט מלא
- ניקוי repository והעברת main כענף ברירת מחדל

## החלטות שהתקבלו

- **עיצוב**: North Star "The Editorial Concierge" עם Hub Coral #E07856
- **ארכיטקטורה**: בידוד זיכרון per-repo במקום shared context  
- **אבטחה**: KPH safety config עם Anthropic provider בלבד
- **ניתוב**: שימוש ב-?lang= query parameter
- **שמות פרויקטים**: project_name_en ?? project_name fallback logic

## משימות שהושלמו

### KPR-150 - Plugin Stack Week 1 ✅
- PR #4 merged → 30e7515 עם 2 באגים שתוקנו
- PRODUCT.md + DESIGN.md + .impeccable/design.json committed
- מערכת עיצוב נעולה עם 8 Named Rules, 7 components

### KPR-151 - claude-mem Week 2 ✅  
- בדיקת זיכרון חוצה סשנים עברה (PHANGAN_VIOLET_TIGER)
- שני נתיבי retrieval פועלים end-to-end
- גיבויים ב-~/_backups/2026-05-18-claude-mem-install/

### KPR-153 - Site Shell merged ✅
- Chrome QA: 12 surfaces כולם PASS  
- באג U+2028 נפתר mid-deploy
- lib/whatsapp.ts עם bilingual link builder

## משימות פתוחות

### דחוף - מחר
1. **סיבוב KPH_API_TOKEN** - נחשף בתמליל 
2. עדכון ~/.kph_admin_token + Vercel env vars (הקלד, אל תעתיק)
3. **KPR-156 Phase 4 Data Cleanup** (High priority) - 4 באגי תוכן

### לא חוסם
- KPR-157: Slug mismatch `/projects/red-sunset-beachfront`
- KPR-158-161: polish items (overflow, mobile wrap, html dir/lang, footer count)
- git author email fix לפתרון Vercel deploy
- סקירת --dangerously-skip-permissions ב-cc-* launchers

## Memory updates needed
- CLAUDE_CODE_STACK.md → v2 uploaded to project knowledge
- Cross-session memory בונה פסיבית - לא נדרשת אקציה
- Phase 1→2 transition infrastructure multiplier מושלם