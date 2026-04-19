# Session Logs

Per-chat logs produced by Claude Chat sessions, organized by date.

## Structure
- `YYYY-MM-DD/chat-[slug].md` — individual session logs from each Claude Chat
- `YYYY-MM-DD/_DAILY_ROLLUP_*.md` — unified summary (auto-generated 23:59 or manually)
- `YYYY-MM-DD/_CHANGELOG_DELTA_*.md` — what changed today
- `YYYY-MM-DD/_ReEntry_Prompt_v*.md` — next session entry point

## Commands (on Liam's Mac)
- `kph-save-session <slug>` — save a session log from stdin
- `kph-rollup-status` — show today's logs + rollup status
- `python3 ~/.local/bin/daily_rollup.py` — trigger rollup manually (auto-runs at 23:59)
