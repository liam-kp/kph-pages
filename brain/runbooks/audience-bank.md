# runbook — Audience Bank

Presets library, per project. Campaign Strategist maintains; refine continuously from `ads_insights_*`. **Moat — keep living.**

## Rules
- 6-8 presets per project, on 3 axes: **intent × geo × language**.
- Every entry labelled **PROVEN / TESTING / DEPRECATED**.
- PROVEN only after **30 days positive ROAS**.
- Intent-first, never dogmatic geo. Never invent Interest IDs — `ads_targeting_search` first.

## Entry shape
`project_id · name · geo · age · languages · interests · exclusions · label`

## Seed bank (TESTING until 30-day ROAS; verify project list vs /Projects_Public)
| project_id | preset | geo | age | lang | interests (seed) | label |
|---|---|---|---|---|---|---|
| KP-BCH-011 | Beachfront-HE | IL | 35-65 | HE | real estate investing, overseas property, Thailand travel | TESTING |
| KP-BCH-011 | Beachfront-EN | EU/UK | 35-65 | EN | property investment, expat, Koh Phangan | TESTING |
| KP-ZEN-012 | Maduwan-HE | IL | 35-60 | HE | wellness, yoga, investment property | TESTING |
| KP-SRI-013 | Srithanu-EN | EU/UK/US | 30-60 | EN | digital nomad, yoga, Koh Phangan | TESTING |
| KP-NAI-014 | NaiWok-HE | IL | 35-65 | HE | real estate, beachfront, Thailand | TESTING |
| KP-LND-015 | RedSunsetLand-HE | IL | 40-65 | HE | land investment, development, Chanote | TESTING |
| KP-BNS | BanNaiSuan-HE | IL | 35-60 | HE | investment property, Koh Phangan | TESTING |

Trigger for KP-LND-015 = סאנסט / Sunset (see `meta-ads-mcp.md` map).
