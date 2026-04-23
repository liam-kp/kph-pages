# Image Classification — resale (general)

For resale properties without a specific USP focus (not specifically sea_view, not beachfront).

Same workflow as `image_classification_seaview.md` — separate target villa from other content, build manifest, choose 4 PING1.

## Visual criteria

A photo BELONGS in `{project_name}/` if it shows:

1. **The actual villa being sold** — exterior, interior, amenities
2. **Recent / current state** — not "before renovation" historical photos
3. **Professional listing-quality** — well-lit, composed, no people
4. **Consistent style** — matches the listing's overall aesthetic

A photo does NOT belong if:

1. **Different property** — different style, different location signals
2. **Render / 3D** — digital, not photo
3. **Old "before" photos** — unless marked specifically as the target
4. **Documents / brochures / floor plans** — these go to `docs/`
5. **Personal / event photos** — selfies, family

## Categories

For general resale:
- `hero_exterior`
- `hero_main_feature` (whatever is the strongest selling point — pool / view / location / size)
- `living_room`
- `kitchen`
- `dining`
- `bedroom_master` / `bedroom_2` / `bedroom_3` / `bedroom_4`
- `bathroom_master` / `bathroom_guest`
- `outdoor_pool` / `outdoor_garden` / `outdoor_terrace`
- `view`
- `aerial_drone`
- `detail`

## PING1 selection

For general resale:

1. **#1** — `hero_exterior` (best wide shot)
2. **#2** — `hero_main_feature` (strongest USP visualization)
3. **#3** — `bedroom_master` (intimate, aspirational)
4. **#4** — `living_room` OR `kitchen` (lifestyle interior)

Adjust based on what makes THIS property special. Ask Liam if unsure: "מה הכי חזק במכר של הוילה הזאת — נוף / בריכה / מיקום / מטבח / שטח?"
