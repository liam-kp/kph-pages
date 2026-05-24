# KPH Marketing Brain — Campaigns Dashboard

**KPR:** KPR-171
**Phase:** v1 (Static JSON) → v2 (Backend wrapper) → v3 (AI Brain)
**Live URL:** https://liam-kp.github.io/kph-pages/dashboard_v2/campaigns.html

## Architecture

```
v1 (now):    fetch_snapshot.py → data.json → campaigns.html (read-only)
v2 (next):   api.aiagentpro.online/marketing-brain/snapshot → same HTML (live + actions)
v3 (future): Claude API integration for optimization recommendations
```

The HTML's `fetch('./data.json')` is the **only** line that changes between v1 → v2.
Everything else is migration-free.

## Files

- `campaigns.html` — Dashboard UI (mobile-first, KPIH brand, vanilla JS)
- `fetch_snapshot.py` — Python script: Meta API → data.json
- `data.json` — Snapshot data (currently mock, refresh via Python script)

## Setup (one-time)

```bash
# 1. Store Meta token (if not already)
mkdir -p ~/.meta
echo "YOUR_META_TOKEN" > ~/.meta/token.txt
chmod 600 ~/.meta/token.txt
```

## Daily refresh

```bash
cd <repo>/dashboard_v2/campaigns
python3 fetch_snapshot.py
git add data.json
git commit -m "snapshot: $(date +%Y-%m-%d)"
git push
```

## v2 migration path

When `api.aiagentpro.online/marketing-brain/snapshot` is live, change one line in `campaigns.html`:

```js
// Before:
const res = await fetch('./data.json?_t=' + Date.now());
// After:
const res = await fetch('https://api.aiagentpro.online/marketing-brain/snapshot?cid=...');
```

That's it.
