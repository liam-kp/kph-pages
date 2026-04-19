# PROMPT 01 — שינוי שמות תמונות (Cowork)
**שלב:** 2b — Image Renaming
**כלי:** Claude Cowork
**מטרה:** שינוי שמות כל תמונות הפרויקט לקונבנציה הסטנדרטית של KPH Sales OS

---

## הוראות לריצה

העתק והדבק את הפרומפט הבא ל-Claude Cowork.
לפני ריצה — מלא את המשתנים בסעיף INPUT.

---

## INPUT — מלא לפני ריצה

```
PROJECT_ID = [KP-XXX-000]          # לדוגמה: KP-BCH-011 / KP-ZEN-012
PROJECT_CODE = [XXX]               # לדוגמה: BCH / ZEN / HIL
PROJECT_NUM = [000]                # לדוגמה: 011 / 012 / 013
PROJECT_FOLDER = ~/Business/01_Real-Estate-Leads/Campaigns/[FOLDER_NAME]/
RAW_IMAGES_SUBFOLDER = reference/  # ברירת מחדל — שנה אם התמונות במקום אחר
```

---

## פרומפט ל-Cowork

```
אני צריך שתעזור לי לשנות שמות לתמונות של פרויקט נדל"ן חדש.

שלב 1 — סרוק את התיקייה:
[PROJECT_FOLDER][RAW_IMAGES_SUBFOLDER]

רשום את כל הקבצים שמצאת (שם קובץ + סיומת + גודל אם זמין).
קבצים מקובצים לפי סוג:
- renders / תמונות חיצוניות
- תמונות פנים
- תמונות אוויר / drone
- תוכניות קומה (floor plans)
- site plan
- תמונות לוקיישן / lifestyle
- אחר

שלב 2 — הצג טבלת מיפוי מוצעת:

| שם מקורי | שם חדש מוצע | קטגוריה | PING1? |
|-----------|-------------|----------|--------|

קונבנציית שמות:
- Render חיצוני:    KP-[CODE]-[NUM]_Render_Exterior_[01/02/03].jpg
- Render אוויר:     KP-[CODE]-[NUM]_Render_Aerial_[01].jpg
- תמונת פנים:      KP-[CODE]-[NUM]_Render_Interior_[01/02].jpg
- בריכה:           KP-[CODE]-[NUM]_Render_Pool_[01].jpg
- תוכנית קומה:     KP-[CODE]-[NUM]_FloorPlan_[2BR/3BR/4BR/Duplex]_[01].pdf
- Site plan:        KP-[CODE]-[NUM]_SitePlan_[01].jpg
- מפה / לוקיישן:   KP-[CODE]-[NUM]_Location_Map_[01].jpg
- Lifestyle:        KP-[CODE]-[NUM]_Photo_Lifestyle_[01/02].jpg

PING1 images — 3-4 תמונות לוואטסאפ (first contact):
שם: KP-IMG-[CODE]-PING1-01.jpg עד KP-IMG-[CODE]-PING1-04.jpg
קריטריון בחירה: 01=hero exterior, 02=interior/pool, 03=aerial/location, 04=floor plan (אופציונלי)

שלב 3 — המתן לאישור שלי לפני שמשנה כלום.
אני אאשר / אתקן את הטבלה — ורק אז בצע את שינוי השמות.

שלב 4 — אחרי אישור, בצע:
1. צור תיקייה: [PROJECT_FOLDER]IMAGES/
2. צור תת-תיקיות: renders/ , floor_plans/ , PING1/ , lifestyle/
3. העתק (לא הזז) כל קובץ לתת-תיקייה המתאימה עם השם החדש
4. תמונות PING1 — העתק גם ל: IMAGES/PING1/ עם שמות KP-IMG-*
5. הצג סיכום: כמה קבצים שונו + רשימה מלאה של PING1 images

חשוב:
- אל תמחק את הקבצים המקוריים ב-reference/
- אם קובץ לא ברור — שאל לפני שאתה מחליט
- PDF של floor plans — שמור כ-PDF, אל תמיר
```

---

## OUTPUT מצופה

לאחר ריצה מוצלחת:

```
[PROJECT_FOLDER]
├── reference/          ← מקוריים שמורים
└── IMAGES/
    ├── renders/
    │   ├── KP-[CODE]-[NUM]_Render_Exterior_01.jpg
    │   ├── KP-[CODE]-[NUM]_Render_Aerial_01.jpg
    │   └── ...
    ├── floor_plans/
    │   ├── KP-[CODE]-[NUM]_FloorPlan_2BR_01.pdf
    │   └── ...
    ├── PING1/
    │   ├── KP-IMG-[CODE]-PING1-01.jpg
    │   ├── KP-IMG-[CODE]-PING1-02.jpg
    │   └── KP-IMG-[CODE]-PING1-03.jpg
    └── lifestyle/
        └── ...
```

---

## מה עובר לשלב הבא (02)

רשום את הערכים האלה — יהיו נדרשים ב-`02_claudecode_upload_firebase.md`:

```
PING1_IMAGE_1 = KP-IMG-[CODE]-PING1-01.jpg
PING1_IMAGE_2 = KP-IMG-[CODE]-PING1-02.jpg
PING1_IMAGE_3 = KP-IMG-[CODE]-PING1-03.jpg
PING1_IMAGE_4 = [אם קיים]
FLOOR_PLAN_FILES = [רשימת קבצי ה-PDF]
```

---

## הערות

- שלב זה = Cowork בלבד. אין כאן Firebase, אין קוד.
- תמונות PING1 הן קריטיות — בלי שמות נכונים, שלב 02 לא עובד.
- אם אין drone/aerial — אפשר לדלג על PING1-03 ולשים lifestyle במקום.
