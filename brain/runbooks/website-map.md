# runbook — Website Map (top-of-funnel)

- Repo `liam-kp/kpih-website` · branch `main` · `~/Business/01_Real-Estate-Leads/kpih-website`
- Stack: Next.js 16 + Tailwind v4 + TS strict + Framer Motion
- **Pulls `/Projects_Public` at BUILD-TIME** → must redeploy to reflect Firebase changes (not live-read).

## Slugs
- Pattern: `kohphanganinvestmenthub.com/projects/{slug}`
- Known live: `red-sunset-beachfront` · `maduwan-zennith` · `srithanu-villas` · `villa-nai-wok` (+ more — verify full set against live `/Projects_Public`).
- `/tour` = canonical project-page template → **clone it for new projects** (onboarding Stage 2).
- Maya can send slugs directly; never tell a lead "search the site."

## Open gap
Deep-link with `project_id` context from site → WhatsApp is not always passed → Maya may miss the project. Track as a flow fix.
