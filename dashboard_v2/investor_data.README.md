# `investor_data.json` — provenance

Feeds two things: `investor.html` (standalone English pitch page, no token) and
the Reports tab's **REPORT · PHASE 1 / PHASE 2** modes (Hebrew). Both render
through `investor_panel.js`, so a number exists in exactly one place.

**Aggregate only — zero PII.** No lead names, phone tails, client names,
Firebase ids, partner splits, or internal ticket references. The page is on a
public repo and is meant to be read by an outside agency.

## Three layers — never blend them

| Block | Layer | Denominator |
|---|---|---|
| `media`, `funnel`, `engine` | **System-recorded, 2026 pilot** | Meta spend in the aligned window |
| `reported` | **Liam-reported, 2026 pilot** | same spend — but only once filled in |
| `track_record` | **All-time ledger, 2023→2026** | none — pre-2026 media spend is not in this ad account |

`track_record` proves closing ability. It does **not** prove pilot ROI: all 17
first-contacts predate 2026-01-02, the earliest campaign in the account.

## Where each number came from (pulled 2026-09-04)

### `media`
- Meta Ads MCP, ad account `820757680962871`, level `ad_account`.
- `lifetime` = `date_preset: maximum` (account opened 2026-01-02).
- `aligned` = `time_range 2026-03-01 → 2026-09-04` — the CRM pipeline went live
  2026-03-01, so this is the spend that bought the leads actually in Firebase.
  **Use it for every cost-per ratio.**
- `conversations_started` = sum of `results` where the indicator is
  `onsite_conversion.messaging_conversation_started_7d`, campaign level. Two
  wa.me link-click campaigns ($670.37) report link clicks, not conversations —
  excluded from the count, included in spend.
- `campaigns[]` rolls the 15 Meta campaigns up to the 5 project codes by name.

### `funnel`
- `GET /api/firebase-data/Leads` → records with `created_at ≥ 2026-01-01` (n=866).
- `GET /api/messages/all?direction=incoming&limit=20000` (Postgres, 6,139 rows)
  → count inbound per `conversation.contact.id`, joined to `Leads.contact_id`.
  `engaged_Nplus` = leads whose contact sent ≥N inbound messages.
  41 media-origin leads have no `contact_id` and cannot join — they count as not engaged.
- `leads_media_origin` (838) = the 866 minus 28 non-media imports **created in
  2026** (`source` in dormant re-activation, `manual`, reminder-bot backlog).
  Leads recovered from a persistence leak (65, `source: kpr347_leak_recovery`)
  stay in — those are media leads the CRM initially dropped. **Every
  `engaged_*`, `hot_warm` and `on_island_or_arriving` figure is computed on the
  838-lead media-origin set**, so the funnel is monotonic.
- `hot_warm` = Firebase `tier ∈ {HOT, WARM}`; `on_island_or_arriving` =
  `arrival_status ∈ {ON_ISLAND, ARRIVING_SOON}`.

### `engine`
- `/api/messages/all?direction=outgoing&limit=1` → `stats` block (AI vs TEAM).
- `GET /api/firebase-data/Follow_Ups` → `status: SENT` by `trigger_type`.
- `best_week_reply_rate` = week review 2026-08-17→24 (16 genuine replies / 60
  content-verified deliveries).

### `reported` — Liam fills these
Nothing here is in any system: `meeting_status` is null on every lead,
`pipeline_data.meetings` is empty, `next_action = MEETING` on 1 record. Until a
value is set the tile renders **awaiting**; cost per meeting / per closing only
compute once `meetings_held` / `closings` are numbers.

### `track_record`
- `pipeline_data.json → deals`, `status: Closed Won` (17). Gross `deal_price`
  and `gross_commission` only — net figures and partner splits are never
  copied here.
- `show_commission: false` hides the ฿16.19M gross-commission tile from an
  outside reader until Liam explicitly says to show it.
- `campaign_share_*` = deals with `source: קמפיין` (10 of 17).

### `phase2_demo`
Made-up round numbers. The renderer marks every tile ILLUSTRATIVE with a dashed
blue top border. Do not tune them to look like Phase 1.

## Refreshing
Re-run the pulls above, edit the JSON, then:

```bash
python3 -m json.tool dashboard_v2/investor_data.json > /dev/null && echo OK
```

Commit on `gh-pages`. No build step — both pages fetch the JSON with `cache: 'no-store'`.
