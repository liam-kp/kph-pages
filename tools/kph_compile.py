#!/usr/bin/env python3
"""
kph-compile — SSOT engine for KPH Sales OS.

Renders ONE authoring SSOT (data/projects/<KP>/inventory.json + data/fx.json)
to every surface: Firebase payloads, Maya prompt-sections, brochure.

Subcommands:
  validate <KP>   registry + inventory sanity, FX present, every token resolves
  render   <KP>   produce rendered sections + Projects_Public payload + brochure
                  price-table fragment -> /tmp (NEVER live)
  diff     <KP>   GET live, diff vs rendered, print human-readable delta
  apply    <KP>   PWRC writes (GET-before -> PUT -> sleep 3 -> GET-after). GATED.

Baked rules: PWRC on every write · EN=THB+USD+EUR / HE=THB+ILS ·
ensure_ascii for HE/emoji · prompt-section PUT preserves existing sortOrder
(re-GET first) · never PATCH · Cloudflare -> curl only.
"""
import argparse, json, os, re, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CID = "11a3a8c9-d3db-4b32-8c08-35dd7868b959"
BASE = "https://api.aiagentpro.online/api"
TOKEN_FILE = os.path.expanduser("~/.kph_admin_token")
SECTION_KEYS = [
    "17-campaign-red-sunset", "18-campaign-maduwan-zennith",
    "20-catalog-villa-nai-wok", "22-campaign-bns-ban-nai-suan",
    "23-discovery-protocol", "32-bns-one-bedroom-navigation",
]
BAND_KEY = {"1 Bed": "1bed", "2 Bed": "2bed", "3 Bed": "3bed", "4 Bed / Grand": "4bed"}


# ---------- loaders ----------
def proj_dir(kp): return os.path.join(DATA, "projects", kp)
def load_ssot(kp): return json.load(open(os.path.join(proj_dir(kp), "inventory.json")))
def load_fx(): return json.load(open(os.path.join(DATA, "fx.json")))
def load_registry(): return json.load(open(os.path.join(DATA, "registry.json")))


def money(sym, n): return f"{sym}{n:,}"
def millions(n):   return f"{n/1e6:g}"


# ---------- token derivation (SSOT -> display strings) ----------
def derive_tokens(ssot):
    """Every display string is DERIVED from the SSOT, so changing the SSOT
    changes every rendered surface. Returns {token: display_string}."""
    t = {}
    bands = {b["band"]: b for b in ssot["band_pricing"]}
    for name, key in BAND_KEY.items():
        b = bands[name]
        t[f"KP-ZEN-012.{key}.thb"]   = money("฿", b["thb"])
        t[f"KP-ZEN-012.{key}.thb_m"] = f"฿{millions(b['thb'])}M"
        t[f"KP-ZEN-012.{key}.usd"]   = money("$", b["usd"])
        t[f"KP-ZEN-012.{key}.eur"]   = money("€", b["eur"])
        t[f"KP-ZEN-012.{key}.ils"]   = money("₪", b["ils"])
    # premium 2-bed (2BR-BIG config) — surfaced in SS18 prose
    big = next(c for c in ssot["configs"] if c["unit_type"] == "2BR-BIG")
    t["KP-ZEN-012.premium2bed.thb"]   = money("฿", big["price_thb"])
    t["KP-ZEN-012.premium2bed.thb_m"] = f"฿{millions(big['price_thb'])}M"
    # range
    lo = min(b["thb"] for b in ssot["band_pricing"] if b["band"] in BAND_KEY)
    hi = max(b["thb"] for b in ssot["band_pricing"] if b["band"] in BAND_KEY)
    t["KP-ZEN-012.range.thb_m"]         = f"฿{millions(lo)}M–฿{millions(hi)}M"
    t["KP-ZEN-012.range.thb_m_compact"] = f"฿{millions(lo)}–{millions(hi)}M"
    # handover (from .delivery)
    m = re.search(r"([A-Z][a-z]+ \d{4})", ssot.get("delivery", ""))
    if m: t["KP-ZEN-012.handover"] = m.group(1)
    return t


def render_text(tmpl, tokens):
    """Resolve {{token}} -> display string."""
    def sub(m):
        k = m.group(1).strip()
        if k not in tokens:
            raise KeyError(f"unresolved token {{{{{k}}}}}")
        return tokens[k]
    return re.sub(r"\{\{([^}]+)\}\}", sub, tmpl)


def tokens_in(tmpl):
    return set(m.strip() for m in re.findall(r"\{\{([^}]+)\}\}", tmpl))


# ---------- curl (Cloudflare needs a browser UA; auth = raw hex + Bearer) ----------
def _token():
    return open(TOKEN_FILE).read().strip()


def curl_get(url):
    out = subprocess.run(
        ["curl", "-sS", "-A", "Mozilla/5.0",
         "-H", f"Authorization: Bearer {_token()}", url],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def get_section(key):
    d = curl_get(f"{BASE}/customers/{CID}/prompt-sections/{key}")
    return d["data"]["section"]


def get_projects_public(kp):
    d = curl_get(f"{BASE}/firebase-data/Projects_Public/{kp}?customerId={CID}")
    return d.get("data", d)


def get_inventory(kp):
    d = curl_get(f"{BASE}/firebase-data/Project_Inventory?customerId={CID}")
    d = d.get("data", d)
    recs = list(d.values()) if isinstance(d, dict) else d
    return [r for r in recs if isinstance(r, dict)
            and str(r.get("project_id", "")).startswith(kp)]


# ---------- rendered Projects_Public payload (derived from SSOT) ----------
def render_projects_public(ssot, tokens):
    # Build-to-suit: availability is PLOT-based (pick a plot + a band), not config-based.
    plots = ssot["land"]["plots"]
    avail = sorted(p for p, info in plots.items()
                   if str(info.get("status", "")).lower() == "available")
    lo = next(b for b in ssot["band_pricing"] if b["band"] == "1 Bed")
    hi = next(b for b in ssot["band_pricing"] if b["band"] == "4 Bed / Grand")
    summary = (f"{len(plots)} plots total, {len(avail)} available ({', '.join(avail)}). "
               f"Build-to-suit: choose your plot + villa type (1BR–4BR), fully customizable design. "
               f"Prices from {money('฿', lo['thb'])} (1BR, {money('₪', lo['ils'])}) "
               f"to {money('฿', hi['thb'])} (4BR). 10–12% est. long-term yield.")
    if ssot.get("short_term_revenue"):
        summary += f" {ssot['short_term_revenue']}."
    return {"availability_summary_public": summary,
            "google_maps_url": ssot.get("location_maps_url")}


# ---------- the two named diff findings ----------
def finding_band_vs_config(ssot):
    lines = ["### Finding 1 — public ladder (KPR-284 decision A: 5-band 'from')",
             "Public ladder = 5 bands, 'from' pricing. Upsell configs are visibility:internal_upsell — "
             "Maya surfaces them only when a lead picks that floor/layout; never in the public ladder or "
             "availability_summary.",
             "", "| Band (public 'from') | Public configs | Internal upsell (hidden) |",
             "|---|---|---|"]
    for b in ssot["public_ladder"]:
        cfgs = b.get("configs", [])
        internal = [c["unit_type"] for c in ssot["configs"]
                    if c["band"] == b["band"] and c.get("visibility") == "internal_upsell"]
        intstr = ", ".join(f"{u}={money('฿', next(c['price_thb'] for c in ssot['configs'] if c['unit_type']==u))}"
                            for u in internal) or "—"
        note = " *(positioning only, no floor plan)*" if b.get("status", "").startswith("positioning") else ""
        lines.append(f"| {b['band']} from {money('฿', b.get('from_thb'))}{note} | "
                     f"{', '.join(cfgs) or '—'} | {intstr} |")
    return "\n".join(lines)


def finding_fx(ssot, fx):
    entry = next(b for b in ssot["band_pricing"] if b["band"] == "1 Bed")
    thb = entry["thb"]
    legacy_rate = 1 / 32.5
    usd_now = entry["usd"]
    usd_legacy = round(thb * legacy_rate / 100) * 100
    return "\n".join([
        "### Finding 2 — FX drift: brochure ฿32.5/$1 vs fx.json 0.0302",
        f"Entry price ฿{thb:,}:",
        "",
        "| Currency | fx.json rate | rendered | brochure legacy (฿32.5) | delta |",
        "|---|---|---|---|---|",
        f"| USD | {fx['thb_to_usd']} | ${usd_now:,} | ${usd_legacy:,} | "
        f"${usd_legacy-usd_now:+,} ({(usd_legacy-usd_now)/usd_now*100:+.1f}%) |",
        f"| EUR | {fx['thb_to_eur']} | €{entry['eur']:,} | (n/a — brochure quoted USD only) | — |",
        f"| ILS | {fx['thb_to_ils']} | ₪{entry['ils']:,} | (n/a — HE not in brochure) | — |",
        "",
        "**Action (NOT applied):** rebuild brochure v3 from fx.json so USD drops to the current rate; "
        "EUR/ILS already on fx.json.",
    ])


# ---------- subcommands ----------
def cmd_validate(kp):
    ssot, fx, reg = load_ssot(kp), load_fx(), load_registry()
    tokens = derive_tokens(ssot)
    problems = []
    for r in ("thb_to_usd", "thb_to_eur", "thb_to_ils"):
        if not fx.get(r): problems.append(f"fx.json missing {r}")
    for b in ssot["band_pricing"]:
        for c in ("thb", "usd", "eur", "ils"):
            if not b.get(c): problems.append(f"band {b['band']} missing {c}")
    # config 'from' consistency: each band 'from_thb' == min config price in band
    for b in ssot["public_ladder"]:
        cps = [next((x["price_thb"] for x in ssot["configs"] if x["unit_type"] == ct), None)
               for ct in b.get("configs", [])]
        cps = [p for p in cps if p]
        if cps and b.get("from_thb") and min(cps) != b["from_thb"]:
            problems.append(f"band {b['band']} from_thb {b['from_thb']} != min config {min(cps)}")
    # every token in every template resolves
    sdir = os.path.join(proj_dir(kp), "sections")
    missing = set()
    if os.path.isdir(sdir):
        for f in sorted(os.listdir(sdir)):
            if f.endswith(".tmpl"):
                missing |= (tokens_in(open(os.path.join(sdir, f)).read()) - set(tokens))
    if missing: problems.append(f"unresolved tokens in templates: {sorted(missing)}")
    print(f"=== validate {kp} ===")
    print(f"registry fields: {len(reg['fields'])} | fx: present | tokens derived: {len(tokens)}")
    print(f"templates: {len([f for f in os.listdir(sdir) if f.endswith('.tmpl')]) if os.path.isdir(sdir) else 0}")
    if problems:
        print("FAIL:"); [print("  -", p) for p in problems]; return 1
    print("PASS — SSOT sane, FX present, all tokens resolve, band 'from' == min config.")
    return 0


def cmd_render(kp, outdir=None):
    ssot, fx = load_ssot(kp), load_fx()
    tokens = derive_tokens(ssot)
    outdir = outdir or os.path.join(tempfile.gettempdir(), f"kph-compile-{kp}")
    os.makedirs(os.path.join(outdir, "sections"), exist_ok=True)
    sdir = os.path.join(proj_dir(kp), "sections")
    n = 0
    for f in sorted(os.listdir(sdir)):
        if f.endswith(".tmpl"):
            rendered = render_text(open(os.path.join(sdir, f)).read(), tokens)
            open(os.path.join(outdir, "sections", f[:-5] + ".rendered.md"), "w").write(rendered)
            n += 1
    pp = render_projects_public(ssot, tokens)
    json.dump(pp, open(os.path.join(outdir, "Projects_Public.patch.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"=== render {kp} -> {outdir} ===")
    print(f"rendered {n} sections, Projects_Public.patch.json (NOT live).")
    return outdir


def cmd_diff(kp):
    ssot, fx = load_ssot(kp), load_fx()
    tokens = derive_tokens(ssot)
    sdir = os.path.join(proj_dir(kp), "sections")
    print(f"=== diff {kp} (live vs rendered-from-SSOT) ===\n")
    print("## Prompt-sections (render(tmpl) vs live content)")
    total = 0
    for f in sorted(os.listdir(sdir)):
        if not f.endswith(".tmpl"): continue
        key = f[:-5]
        rendered = render_text(open(os.path.join(sdir, f)).read(), tokens)
        live = get_section(key)["content"]
        if rendered == live:
            print(f"  ✅ {key}: 0 char delta (idempotent)")
        else:
            d = sum(1 for a, b in zip(rendered, live) if a != b) + abs(len(rendered) - len(live))
            total += d
            print(f"  ⚠️ {key}: {d} char delta")
    print(f"\n  sections total delta: {total}")
    # Projects_Public
    print("\n## Projects_Public (rendered patch vs live)")
    live = get_projects_public(kp)
    patch = render_projects_public(ssot, tokens)
    for k, v in patch.items():
        lv = live.get(k)
        mark = "✅" if lv == v else "⚠️"
        print(f"  {mark} {k}:")
        print(f"      live    : {json.dumps(lv, ensure_ascii=False)[:160]}")
        print(f"      rendered: {json.dumps(v, ensure_ascii=False)[:160]}")
    print()
    print(finding_band_vs_config(ssot)); print()
    print(finding_fx(ssot, fx))
    return 0


PP_FIELD = "availability_summary_public"
# wrapper may bump these on write; not counted as an "unexpected" change
TIMESTAMP_FIELDS = {"updated_at", "updatedAt", "last_updated_public"}


def curl_put(url, body_obj):
    # ensure_ascii=True for HE/emoji (aiagentpro wrapper convention); never PATCH.
    data = json.dumps(body_obj, ensure_ascii=True)
    out = subprocess.run(
        ["curl", "-sS", "-X", "PUT", "-A", "Mozilla/5.0",
         "-H", f"Authorization: Bearer {_token()}",
         "-H", "Content-Type: application/json",
         "--data-binary", data, url],
        capture_output=True, text=True, check=True).stdout
    return out


def cmd_apply(kp, confirm=False):
    # GUARD 1: no flag -> refuse, non-zero. A stub can never silently pass.
    if not confirm:
        print(f"=== apply {kp} — GATE ===")
        print("REFUSED. Live Firebase write requires --i-have-liams-go.")
        return 2

    ssot, fx = load_ssot(kp), load_fx()
    tokens = derive_tokens(ssot)
    intended = render_projects_public(ssot, tokens)[PP_FIELD]
    url = f"{BASE}/firebase-data/Projects_Public/{kp}?customerId={CID}"

    # PWRC: GET-before (full record)
    before = curl_get(url)
    before = before.get("data", before) if isinstance(before, dict) and "_id" not in before else before
    before_val = before.get(PP_FIELD)

    # write exactly ONE field on a full merged payload (PUT, never PATCH)
    merged = dict(before)
    merged[PP_FIELD] = intended
    curl_put(url, merged)
    time.sleep(3)

    # GET-after (independent re-read)
    after = curl_get(url)
    after = after.get("data", after) if isinstance(after, dict) and "_id" not in after else after
    after_val = after.get(PP_FIELD)

    # side-by-side
    print(f"=== PWRC apply {kp} : {PP_FIELD} ===")
    print("GET-before:")
    print(f"  {before_val!r}")
    print("GET-after :")
    print(f"  {after_val!r}")

    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    unexpected = [k for k in changed if k != PP_FIELD and k not in TIMESTAMP_FIELDS]
    print(f"\nfields changed: {changed}")
    print(f"prompt-sections written: 0 | Project_Inventory written: 0")

    # GUARD 2: post-write assert. Never exit 0 without a verified exact match.
    if after_val != intended:
        print("\n‼️‼️ FAILED — live value != intended string. Write did NOT verify.")
        print(f"INTENDED:\n  {intended!r}")
        return 1
    if unexpected:
        print(f"\n‼️‼️ FAILED — unexpected fields changed: {unexpected}")
        return 1
    print("\n✅ VERIFIED — 1 field written, GET-after == intended EXACTLY, 0 other fields, 0 sections.")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="kph-compile")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("validate", "render", "diff", "apply"):
        p = sub.add_parser(c); p.add_argument("kp")
        if c == "apply": p.add_argument("--i-have-liams-go", action="store_true")
    a = ap.parse_args()
    if a.cmd == "validate": sys.exit(cmd_validate(a.kp))
    if a.cmd == "render":   cmd_render(a.kp); sys.exit(0)
    if a.cmd == "diff":     sys.exit(cmd_diff(a.kp))
    if a.cmd == "apply":    sys.exit(cmd_apply(a.kp, a.i_have_liams_go))


if __name__ == "__main__":
    main()
