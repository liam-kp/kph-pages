# Image Classification — sea_view segment

When a folder contains photos from multiple sources (e.g., a developer who shared materials for 2 different properties in the same WhatsApp thread), separate them.

## Target sub-folders

- `images/{project_name}/` — confirmed images of THE villa being onboarded
- `images/_other_project/` — images that look like a different property (move them, with a note in `_uncertain.txt`)
- `images/_uncertain/` — can't tell either way

## Visual criteria for sea_view villa

A photo BELONGS in `{project_name}/` if it shows ANY of:

1. **Modern furnished interior** — bohemian-chic / boho / minimalist style. Bright walls, large windows, glass doors opening to terrace.
2. **Infinity pool with ocean horizon visible** — water meets sky line, no fence between pool and view.
3. **Master bedroom with sea-facing window or balcony** — typically king bed, often with mosquito netting or beach decor.
4. **Open-plan living/dining with terrace access** — couch + dining + sliding doors to outside.
5. **Kitchen island in modern style** — usually white / wood / rattan stools.
6. **Aerial / drone shot of the villa from outside** — clearly a single villa with sea behind it.
7. **Terrace / balcony with sea view as the main subject**.

A photo does NOT belong (move to `_other_project/`) if it shows:

1. **Old / unrenovated property** — peeling walls, water damage, mildew, broken fixtures.
2. **Render / 3D visualization** — clearly digital art, not photo. (Unless explicitly stated to be the target villa's planned renovation.)
3. **Different style than the listing** — if Airbnb shows boho-chic and this photo shows industrial / Asian traditional — it's probably another property.
4. **Different location signals** — jungle view when target is sea view, urban backdrop, different neighborhood.
5. **People-centric photos** — selfies, family events, people sitting unrelated to the villa.
6. **Documents / brochures** — these go to `docs/`, not images.

## Tools to use

**If Cowork is available:** Hand it the folder path + this criteria document. Cowork visually inspects each image.

**If Cowork unavailable:** Use macOS `sips` and filename patterns:
```bash
# Check dimensions and size for each image
for f in *.jpg *.jpeg *.png; do
  [ -f "$f" ] || continue
  dim=$(sips -g pixelWidth -g pixelHeight "$f" 2>/dev/null | grep pixel)
  size=$(stat -f%z "$f" 2>/dev/null)
  echo "$f | $dim | $size bytes"
done
```

Heuristics:
- Files larger than 1MB and >2000px wide are usually professional listing photos
- Files <200KB and <1000px are usually thumbnails or chat-screenshot junk
- Sequential timestamps (e.g., 50 photos all within a 1-minute window) = bulk drop, often all from same source

When in doubt — move to `_uncertain/` and ask Liam to spot-check.

## Cross-reference with chat history

Read `_chat_zip*_*.txt` files in `docs/`. Look for:
- Mentions of the target property name vs. other names
- "לפני" / "אחרי" annotations near image attachments — `לפני` often means "before renovation" → render images of a renovation project (NOT the target villa)
- "זה הויזן" / "הדמיות" / "render" → 3D visualizations → almost certainly NOT real photos of the target

In Villa Anne onboarding (April 2026), Eldar shared 50 photos that were ALL of a different Madawan renovation project (mixed with chat about Villa Anne). All 50 went to `_other_project/`. Real Villa Anne photos came from Airbnb listing scrape.

## Output

After classification, generate `images/{project_name}/_manifest.md`:

```markdown
# {Project Name} — Photo Manifest

| # | Filename | Category | תיאור עברי | PING1 |
|---|----------|----------|------------|-------|
| 1 | 01_hero_exterior.jpg | hero_exterior | חזית הבית עם נוף פתוח לים | ⭐ |
| 2 | 02_hero_pool_seaview.jpg | hero_pool_seaview | בריכת אינפיניטי עם נוף ים פנורמי | ⭐ |
| 3 | 03_living_terrace.jpg | living_terrace | סלון פתוח עם דלתות זכוכית למרפסת | |
| 4 | 04_bedroom_master.jpg | bedroom_master | חדר שינה ראשי עם יציאה לבריכה ולים | ⭐ |
...
```

Categories for sea_view:
- `hero_exterior`
- `hero_pool_seaview`
- `living_terrace`
- `kitchen`
- `dining`
- `bedroom_master`
- `bedroom_2` / `bedroom_3` / `bedroom_4`
- `bathroom_master` / `bathroom_2`
- `terrace_view` (if the view is the subject, not the terrace itself)
- `aerial_drone`
- `detail` (decor, accessory)
- `garden` / `outdoor`

## Choose the 4 PING1 hero images

These go into the WhatsApp first-message bubble. Optimal mix:

1. **#1 PING1** — `hero_exterior` (villa + pool + sea visible)
2. **#2 PING1** — `hero_pool_seaview` (infinity edge prominent)
3. **#3 PING1** — `bedroom_master` (sea view from inside, intimate)
4. **#4 PING1** — `living_terrace` OR `kitchen` (interior signature)

Mark with `⭐ PING1` in the manifest.

## File naming convention

Sequential numbering by priority, two-digit padding, lowercase category:

```
01_hero_exterior.jpg
02_hero_pool_seaview.jpg
03_living_terrace.jpg
04_bedroom_master.jpg
05_kitchen.jpg
06_bedroom_2.jpg
07_bathroom_master.jpg
...
20_garden.jpg
```

If converting from another extension (PNG → JPG for compression): keep the original extension to preserve quality. Don't transcode unless filesize is a problem.
