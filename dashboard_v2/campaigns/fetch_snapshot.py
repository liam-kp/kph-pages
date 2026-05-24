#!/usr/bin/env python3
"""
fetch_snapshot.py — KPH Marketing Brain
Pulls last_30d snapshot from Meta Marketing API and writes data.json.

Usage:
    python3 fetch_snapshot.py

Requirements:
    - ~/.meta/token.txt containing a valid Meta Marketing API access token
    - Token needs permissions: ads_read, ads_management

Output:
    data.json (overwrites existing)

Architecture note (KPR-170):
    v1: Runs locally, writes to repo, git push manually triggers GitHub Pages.
    v2: Will move to api.aiagentpro.online cron, frontend won't change.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────
AD_ACCOUNT_ID = "820757680962871"
ACCOUNT_NAME = "KP Hub – Koh Phangan Real Estate (AgentOS)"
TOKEN_PATH = Path.home() / ".meta" / "token.txt"
OUTPUT_PATH = Path(__file__).parent / "data.json"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Health thresholds (from 06_KPI_DEFINITIONS_v1.md)
COST_PER_CONV_EXCELLENT = 8.0
COST_PER_CONV_GOOD = 12.0
COST_PER_CONV_ACCEPTABLE = 18.0
COST_PER_CONV_WARNING = 25.0

# ─── Helpers ──────────────────────────────────────────────────────────────
def load_token():
    if not TOKEN_PATH.exists():
        sys.exit(f"❌ Token not found at {TOKEN_PATH}\n"
                 f"   Create it with:\n"
                 f"     mkdir -p ~/.meta && echo 'YOUR_TOKEN' > {TOKEN_PATH}\n"
                 f"     chmod 600 {TOKEN_PATH}")
    return TOKEN_PATH.read_text().strip()

def fetch_graph(path, params, token):
    params["access_token"] = token
    url = f"{BASE_URL}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "kph-marketing-brain/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"❌ Meta API HTTP {e.code} on {path}\n   Body: {body[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"❌ Network error: {e.reason}")

def extract_conversations(actions):
    """Pull WhatsApp/Messenger conversation count from insights actions array."""
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == "onsite_conversion.messaging_conversation_started_7d":
            try:
                return int(float(a.get("value", 0)))
            except (ValueError, TypeError):
                return 0
    return 0

def classify_health(cost_per_conv, frequency):
    """Returns ('excellent'|'good'|'warning'|'kill', verdict_string)."""
    if cost_per_conv is None or cost_per_conv == 0:
        return ("warning", "no_conversations")
    if frequency and frequency > 3.5:
        return ("warning", "creative_fatigue")
    if cost_per_conv < COST_PER_CONV_EXCELLENT:
        return ("excellent", "scale")
    if cost_per_conv < COST_PER_CONV_GOOD:
        return ("good", "hold")
    if cost_per_conv < COST_PER_CONV_ACCEPTABLE:
        return ("warning", "monitor")
    if cost_per_conv < COST_PER_CONV_WARNING:
        return ("warning", "investigate")
    return ("kill", "kill_immediately")

def safe_float(v, default=0.0):
    try:
        return float(v) if v is not None else default
    except (ValueError, TypeError):
        return default

# ─── Main ─────────────────────────────────────────────────────────────────
def main():
    print(f"🔑 Loading token from {TOKEN_PATH}")
    token = load_token()

    print(f"📡 Fetching campaigns from Ad Account {AD_ACCOUNT_ID} (last 30d)...")

    # Campaign-level insights for last_30d
    insights = fetch_graph(
        f"act_{AD_ACCOUNT_ID}/insights",
        {
            "level": "campaign",
            "date_preset": "last_30d",
            "fields": "campaign_id,campaign_name,spend,impressions,clicks,ctr,cpc,cpm,frequency,reach,actions",
            "limit": "100",
        },
        token,
    )

    # Campaign metadata (status, budget, objective)
    campaigns_meta = fetch_graph(
        f"act_{AD_ACCOUNT_ID}/campaigns",
        {
            "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget",
            "limit": "100",
        },
        token,
    )
    meta_by_id = {c["id"]: c for c in campaigns_meta.get("data", [])}

    campaigns = []
    totals = dict(spend=0.0, impressions=0, clicks=0, conversations=0,
                  active_campaigns=0, paused_campaigns=0)

    for row in insights.get("data", []):
        cid = row.get("campaign_id")
        meta = meta_by_id.get(cid, {})
        spend = safe_float(row.get("spend"))
        impressions = int(safe_float(row.get("impressions")))
        clicks = int(safe_float(row.get("clicks")))
        ctr = safe_float(row.get("ctr"))
        cpc = safe_float(row.get("cpc"))
        cpm = safe_float(row.get("cpm"))
        frequency = safe_float(row.get("frequency"))
        conversations = extract_conversations(row.get("actions"))
        cost_per_conv = (spend / conversations) if conversations > 0 else None
        health, verdict = classify_health(cost_per_conv, frequency)

        status = meta.get("status", "UNKNOWN")
        daily_budget_cents = safe_float(meta.get("daily_budget"))
        daily_budget_usd = round(daily_budget_cents / 100, 2) if daily_budget_cents else None

        campaigns.append({
            "id": cid,
            "name": row.get("campaign_name", meta.get("name", "(unnamed)")),
            "status": status,
            "delivery_status": meta.get("effective_status", "").lower(),
            "objective": meta.get("objective"),
            "daily_budget_usd": daily_budget_usd,
            "spend": round(spend, 2),
            "impressions": impressions,
            "clicks": clicks,
            "conversations": conversations,
            "ctr": round(ctr, 2),
            "cpc": round(cpc, 2),
            "cpm": round(cpm, 2),
            "frequency": round(frequency, 2),
            "cost_per_conversation": round(cost_per_conv, 2) if cost_per_conv else None,
            "health": health,
            "verdict": verdict,
        })

        totals["spend"] += spend
        totals["impressions"] += impressions
        totals["clicks"] += clicks
        totals["conversations"] += conversations
        if status == "ACTIVE":
            totals["active_campaigns"] += 1
        elif status == "PAUSED":
            totals["paused_campaigns"] += 1

    # Sort by spend descending
    campaigns.sort(key=lambda c: c["spend"], reverse=True)

    # Aggregate averages
    avg_ctr = (totals["clicks"] / totals["impressions"] * 100) if totals["impressions"] else 0
    avg_cpc = (totals["spend"] / totals["clicks"]) if totals["clicks"] else 0
    avg_cpm = (totals["spend"] / totals["impressions"] * 1000) if totals["impressions"] else 0
    avg_cpconv = (totals["spend"] / totals["conversations"]) if totals["conversations"] else 0

    output = {
        "meta": {
            "ad_account_id": AD_ACCOUNT_ID,
            "account_name": ACCOUNT_NAME,
            "currency": "USD",
            "snapshot_at": datetime.now(timezone(timedelta(hours=7))).isoformat(),
            "date_range": "last_30d",
            "generator": "fetch_snapshot.py v1.0",
            "is_mock": False,
        },
        "totals": {
            "total_spend": round(totals["spend"], 2),
            "total_impressions": totals["impressions"],
            "total_clicks": totals["clicks"],
            "total_conversations": totals["conversations"],
            "avg_ctr": round(avg_ctr, 2),
            "avg_cpc": round(avg_cpc, 2),
            "avg_cpm": round(avg_cpm, 2),
            "avg_cost_per_conversation": round(avg_cpconv, 2),
            "active_campaigns": totals["active_campaigns"],
            "paused_campaigns": totals["paused_campaigns"],
        },
        "campaigns": campaigns,
    }

    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"✅ Wrote {OUTPUT_PATH}")
    print(f"   Campaigns: {len(campaigns)} ({totals['active_campaigns']} active, {totals['paused_campaigns']} paused)")
    print(f"   Total spend: ${totals['spend']:.2f} | Conversations: {totals['conversations']} | Avg CpC: ${avg_cpconv:.2f}")

if __name__ == "__main__":
    main()
