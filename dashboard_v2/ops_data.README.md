# `ops_data.json` — Ops tab snapshot

The Ops tab reads **live** `/Leads` and `/Follow_Ups` from Firebase in the browser.
This file carries only the four things a public, tokenless page cannot read live:

| Block | Why it is not live |
|---|---|
| `tickets` | Linear needs an API token. It cannot ship on a public page. |
| `waves[].replies` / `reply_rate` | Replies are counted by matching real message **content + timing** in Postgres threads. `Follow_Ups.status` and Postgres `status`/`sentAt`/`deliveredAt` are unusable — see **KPR-331**. |
| `ghosts` | Derived from the local iPhone WhatsApp backup, which never leaves the Mac. |
| `backup` | Local `Status.plist`. |

Everything here is **aggregate only — zero PII**. Never add a name, phone number,
`@lid`, Firebase lead id, or conversation UUID. Ticket *descriptions* contain
conversation UUIDs, so only id/title/status/priority/dates are carried across.

Every value sourced from this file is labelled "as of `meta.generated_at`" in the UI.

## Refreshing

### 1. Tickets (Linear MCP, in a Claude Code session)

For each id in `tickets[]`:

- `get_issue` → `status`, `statusType`, `priority.name`
- `list_comments` → newest comment whose `author.id` is Adam
  (`096b2fe1-b557-4d6d-83bd-f81793b21eb2`) → `adam_last_comment_at`.
  No such comment → `null`, which the UI renders as a red **never**.

`days since` is computed in the browser from the ISO timestamp, so the figure
never goes stale between refreshes — only the timestamp itself does.

### 2. Backup

```bash
/usr/libexec/PlistBuddy -c Print \
  ~/Library/Application\ Support/MobileSync/Backup/*/Status.plist
```

Take `Date` and `SnapshotState`. **Read `Status.plist`, never `Info.plist`** — a
failed backup run still bumps `Info.plist`'s date, so it will lie to you.

### 3. Ghosts

Re-run `_marketing_brain/data/fresh_<date>/ghost_recheck_truefresh.py` against a
freshly extracted `AppDomainGroup-group.net.whatsapp.WhatsAppSMB.shared` domain
(the Business app — the plain `WhatsApp.shared` domain loads cleanly but silently
drops most matched leads). Copy `ghosts_in_window` / `ghosts_all_time`, and set
`as_of` and `backup_used` to the backup you actually used.

Set `stale_vs_latest_backup: true` whenever `ghosts.as_of` is older than
`backup.date` — the UI then prints a ⚠ next to the count instead of implying the
number came from the latest backup.

### 4. Waves

`armed` / `sent` need no maintenance — the browser computes them live from
`/Follow_Ups.wave_id`. Only add `delivered` / `replies` / `reply_rate` once a wave
has been verified by content-matching. A live `wave_id` with no entry here still
appears in the table, marked `— (not in snapshot)` with `not measured`.

Rows in `wave_combined` and `baselines` are carried in verbatim and render as
italic rows below the table — they are not separate waves.

## After editing

```bash
python3 -m json.tool dashboard_v2/ops_data.json > /dev/null && echo OK
```

Then commit `ops_data.json` on `gh-pages`. No rebuild step — the page fetches it
with `cache: 'no-store'`.
