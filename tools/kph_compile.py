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
def round100(n):   return int(round(n / 100.0)) * 100   # display-rounding: converted currency -> nearest 100


# ---------- token derivation (SSOT -> display strings) ----------
def derive_tokens(ssot, fx):
    """Every display string is DERIVED from the SSOT, so changing the SSOT
    changes every rendered surface. Returns {token: display_string}.
    Converted currencies are derived from fx.json (single source) and display-rounded
    to nearest 100 (KPR-284 Step 1); THB is shown in full. Stored band_pricing
    usd/eur/ils are intentionally NOT read — FX is the one source."""
    t = {}
    bands = {b["band"]: b for b in ssot["band_pricing"]}
    for name, key in BAND_KEY.items():
        b = bands[name]
        a = fx_amounts(b["thb"], fx)
        t[f"KP-ZEN-012.{key}.thb"]   = money("฿", b["thb"])
        t[f"KP-ZEN-012.{key}.thb_m"] = f"฿{millions(b['thb'])}M"
        t[f"KP-ZEN-012.{key}.usd"]   = money("$", a["usd"])
        t[f"KP-ZEN-012.{key}.eur"]   = money("€", a["eur"])
        t[f"KP-ZEN-012.{key}.ils"]   = money("₪", a["ils"])
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
    # built m² of the 1-bed entry config — so SS18 derives it from inventory, never a hardcoded number
    t["KP-ZEN-012.1bed.sqm"] = f"{_band_entry_config(ssot, '1 Bed')['built_size_sqm']:g}"
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


# ---------- widened price block (KPR-284 Phase-1 WIDEN) ----------
# Exact THB*fx, NO display-rounding (step 5 owns rounding). EN=THB+USD+EUR, HE=THB+ILS.
PP_PUBLIC_BANDS = ["1 Bed", "2 Bed", "3 Bed", "4 Bed / Grand"]
PP_BAND_TOKEN = {"1 Bed": "1bed", "2 Bed": "2bed", "3 Bed": "3bed", "4 Bed / Grand": "4bed"}
# template-driven price-bearing Projects_Public prose (live field name -> template)
PP_TMPL = {
    "short_pitch_he":             "pp/short_pitch.he.tmpl",
    "short_pitch_en":             "pp/short_pitch.en.tmpl",
    "second_message_template":    "pp/second_message.he.tmpl",   # HE field has NO _he suffix (live truth)
    "second_message_template_en": "pp/second_message.en.tmpl",
}


# STC verdict (origin/production code-truth, 2026-06-25) — which widened fields the bot actually reads.
PP_STC_STATUS = {
    "availability_summary_public": "ACTIVE (7 prod files)",
    "google_maps_url":             "ACTIVE (10 prod files)",
    "second_message_template":     "ACTIVE (jade_master_prompt directs Maya)",
    "second_message_template_en":  "ACTIVE (jade_master_prompt directs Maya)",
    "short_pitch_he":              "ORPHANED (0 prod read paths)",
    "short_pitch_en":              "ORPHANED (0 prod read paths)",
}


def extract_thb(v, min_val=1_000_000):
    """THB villa prices in a value. Boundary-anchored so grouped numbers aren't sliced
    (₪315,350 stays 315350, not 15350). Filtered to >= min_val to isolate the THB ladder
    (villa prices are >=฿1M; USD/EUR/ILS conversions are all <฿1M) — set min_val=0 for all."""
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    out = set()
    for m in re.findall(r"(?<![\d,.])\d{1,3}(?:,\d{3})+(?![\d])", s):
        out.add(int(m.replace(",", "")))
    for m in re.findall(r"฿\s*(\d+(?:\.\d+)?)\s*M\b", s):
        out.add(int(float(m) * 1_000_000))
    return {n for n in out if n >= min_val}


def fx_amounts(thb, fx):
    # KPR-284 Step 1 display-rounding: converted currencies -> nearest 100 (THB never rounded).
    # Derived from the single FX source (fx.json); stored band_pricing usd/eur/ils are NOT read.
    return {"usd": round100(thb * fx["thb_to_usd"]),
            "eur": round100(thb * fx["thb_to_eur"]),
            "ils": round100(thb * fx["thb_to_ils"])}


def _sqm(x):  # exact built m²; %g only strips a trailing .0 (40.0->40), NOT display-rounding (79.4 stays 79.4)
    return f"{x:g}"


def _band_entry_config(ssot, band):
    """The 'from' config of a band = cheapest PUBLIC config in it (internal_upsell excluded)."""
    pub = [c for c in ssot["configs"] if c["band"] == band and c.get("visibility") == "public"]
    return min(pub, key=lambda c: c["price_thb"])


def derive_pp_tokens(ssot, fx):
    """Exact-from-fx price + built-m² tokens for the widened Projects_Public prose block."""
    bands = {b["band"]: b for b in ssot["band_pricing"]}
    t = {}
    for band in PP_PUBLIC_BANDS:
        key = PP_BAND_TOKEN[band]
        a = fx_amounts(bands[band]["thb"], fx)
        t[f"pp.{key}.thb"] = money("฿", bands[band]["thb"])
        t[f"pp.{key}.usd"] = money("$", a["usd"])
        t[f"pp.{key}.eur"] = money("€", a["eur"])
        t[f"pp.{key}.ils"] = money("₪", a["ils"])
        t[f"pp.{key}.sqm"] = _sqm(_band_entry_config(ssot, band)["built_size_sqm"])
    # premium 2-bed = the 2BR-BIG config (฿6.7M, visibility:public). 5.5M/6.4M stay internal_upsell (hidden).
    big = next(c for c in ssot["configs"] if c["unit_type"] == "2BR-BIG")
    ab = fx_amounts(big["price_thb"], fx)
    t["pp.2bedbig.thb"] = money("฿", big["price_thb"])
    t["pp.2bedbig.usd"] = money("$", ab["usd"])
    t["pp.2bedbig.eur"] = money("€", ab["eur"])
    t["pp.2bedbig.ils"] = money("₪", ab["ils"])
    t["pp.2bedbig.sqm"] = _sqm(big["built_size_sqm"])
    lo, hi = bands["1 Bed"]["thb"], bands["4 Bed / Grand"]["thb"]
    t["pp.range.thb"] = f"{money('฿', lo)}–{money('฿', hi)}"
    return t


def render_pp_fields(ssot, fx, kp):
    tok = derive_pp_tokens(ssot, fx)
    out = {}
    for field, rel in PP_TMPL.items():
        out[field] = render_text(open(os.path.join(proj_dir(kp), rel)).read().rstrip("\n"), tok)
    return out


# ---------- rendered Projects_Public payload (derived from SSOT) ----------
def render_projects_public(ssot, tokens, fx=None, kp=None):
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
    out = {"availability_summary_public": summary,
           "google_maps_url": ssot.get("location_maps_url")}
    # WIDEN: merge the price-bearing prose block only when fx+kp supplied (render/diff path,
    # NOT the gated single-field apply path, which calls with (ssot, tokens) only).
    if fx is not None and kp is not None:
        out.update(render_pp_fields(ssot, fx, kp))
    return out


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
    tokens = derive_tokens(ssot, fx)
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
    tokens = derive_tokens(ssot, fx)
    outdir = outdir or os.path.join(tempfile.gettempdir(), f"kph-compile-{kp}")
    os.makedirs(os.path.join(outdir, "sections"), exist_ok=True)
    sdir = os.path.join(proj_dir(kp), "sections")
    n = 0
    for f in sorted(os.listdir(sdir)):
        if f.endswith(".tmpl"):
            rendered = render_text(open(os.path.join(sdir, f)).read(), tokens)
            open(os.path.join(outdir, "sections", f[:-5] + ".rendered.md"), "w").write(rendered)
            n += 1
    pp = render_projects_public(ssot, tokens, fx, kp)
    json.dump(pp, open(os.path.join(outdir, "Projects_Public.patch.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"=== render {kp} -> {outdir} ===")
    print(f"rendered {n} sections, Projects_Public.patch.json (NOT live).")
    return outdir


def cmd_diff(kp):
    ssot, fx = load_ssot(kp), load_fx()
    tokens = derive_tokens(ssot, fx)
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
    # Projects_Public (WIDENED — full price block)
    print("\n## Projects_Public price block (rendered-from-SSOT vs live)")
    live = get_projects_public(kp)
    patch = render_projects_public(ssot, tokens, fx, kp)
    for k, v in patch.items():
        lv = live.get(k)
        same = (lv == v)
        stc = PP_STC_STATUS.get(k, "?")
        print(f"\n  {'✅' if same else '⚠️'} {k}   [STC: {stc}]")
        lp, rp = extract_thb(lv), extract_thb(v)
        if lp or rp:
            removed = sorted(lp - rp); added = sorted(rp - lp)
            print(f"      THB live : {sorted(lp)}")
            print(f"      THB SSOT : {sorted(rp)}")
            if removed: print(f"      ▸ live-only (stale, dropped by SSOT): {removed}")
            if added:   print(f"      ▸ SSOT-only (added):                 {added}")
        if not same:
            print(f"      live     : {json.dumps(lv, ensure_ascii=False)[:240]}")
            print(f"      rendered : {json.dumps(v, ensure_ascii=False)[:240]}")
    print()
    print(finding_band_vs_config(ssot)); print()
    print(finding_fx(ssot, fx))
    return 0


PP_WRITE_FIELDS = [
    "second_message_template",      # HE field has NO _he suffix (STC-confirmed live truth)
    "second_message_template_en",
    "short_pitch_he",
    "short_pitch_en",
]
# wrapper may bump these on write; not counted as an "unexpected" change
TIMESTAMP_FIELDS = {"updated_at", "updatedAt", "last_updated_public"}


def _norm(rec):
    return rec.get("data", rec) if isinstance(rec, dict) and "_id" not in rec else rec


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


def cmd_apply(kp, confirm=False, dry=False):
    # GUARD 1: no go-flag -> refuse, non-zero (applies to --dry too). A stub can never silently pass.
    if not confirm:
        print(f"=== apply {kp} — GATE ===")
        print("REFUSED. Live Firebase write requires --i-have-liams-go.")
        return 2

    ssot, fx = load_ssot(kp), load_fx()
    intended = render_pp_fields(ssot, fx, kp)   # exactly the 4 PP_WRITE_FIELDS, exact fx, no display-rounding
    assert sorted(intended) == sorted(PP_WRITE_FIELDS), f"render set {sorted(intended)} != write set {sorted(PP_WRITE_FIELDS)}"
    url = f"{BASE}/firebase-data/Projects_Public/{kp}?customerId={CID}"

    # PWRC: GET-before (full record)
    before = _norm(curl_get(url))

    # Build full merged record: live record with ONLY the 4 fields replaced. Every other field byte-identical.
    merged = dict(before)
    for f in PP_WRITE_FIELDS:
        merged[f] = intended[f]

    # top-level churn analysis (we replace VALUES, never add/remove keys)
    key_added = sorted(set(merged) - set(before))
    key_removed = sorted(set(before) - set(merged))
    val_changed = sorted(k for k in (set(before) | set(merged)) if before.get(k) != merged.get(k))
    keys_ok = (not key_added and not key_removed)
    # SUBSET invariant: every changed top-level key must be within PP_WRITE_FIELDS, and >=1 changed.
    # A re-apply that legitimately touches fewer than 4 (e.g. only the m²-bearing fields) still passes;
    # abort only on key churn or a changed field OUTSIDE the 4.
    outside_fields = [k for k in val_changed if k not in PP_WRITE_FIELDS]
    set_ok = (len(val_changed) >= 1 and not outside_fields)

    mode = "DRY-RUN (no PUT)" if dry else "LIVE PWRC WRITE"
    print(f"=== apply {kp} — {mode} : {len(PP_WRITE_FIELDS)} Projects_Public fields ===\n")
    for f in PP_WRITE_FIELDS:
        print(f"───────── {f} ─────────")
        print("LIVE (before):"); print(repr(before.get(f)))
        print("INTENDED (rendered, exact fx, no display-rounding):"); print(repr(intended[f]))
        print()
    print("EXACT json.dumps of the 4 changed keys (ensure_ascii=True — byte-for-byte as PUT would send):")
    print(json.dumps({f: intended[f] for f in PP_WRITE_FIELDS}, ensure_ascii=True, indent=2))
    print()
    print(f"top-level keys ADDED  : {key_added}    (MUST be [])")
    print(f"top-level keys REMOVED: {key_removed}    (MUST be [])")
    print(f"top-level VALUE-changed: {val_changed}")
    print(f"  → key-set unchanged: {'✅' if keys_ok else '‼️ NO'} | changed ⊆ the 4 (≥1): {'✅' if set_ok else '‼️ NO — outside: '+str(outside_fields)}")

    if dry:
        print("\n=== DRY-RUN — no PUT issued, zero Firebase writes. ===")
        return 0 if (keys_ok and set_ok) else 1

    # GUARD 2 (pre-PUT): refuse if the merged record changes anything beyond the 4 values.
    if not (keys_ok and set_ok):
        print("\n‼️‼️ ABORT — merged record would change more than the 4 fields. No PUT issued.")
        return 1

    # LIVE PWRC: PUT full merged -> sleep -> GET-after (independent re-read) -> verify
    curl_put(url, merged)
    time.sleep(3)
    after = _norm(curl_get(url))

    bad = [f for f in PP_WRITE_FIELDS if after.get(f) != intended[f]]
    after_changed = sorted(k for k in (set(before) | set(after)) if before.get(k) != after.get(k))
    unexpected = [k for k in after_changed if k not in PP_WRITE_FIELDS and k not in TIMESTAMP_FIELDS]
    print(f"\nGET-after top-level changed: {after_changed}")
    print("prompt-sections written: 0 | Project_Inventory written: 0")

    # GUARD 3: post-write assert. Never exit 0 without verified exact match + zero collateral.
    if bad:
        print(f"\n‼️‼️ FAILED — these fields did not verify (live != intended): {bad}")
        for f in bad:
            print(f"  {f}\n    intended: {intended[f]!r}\n    live    : {after.get(f)!r}")
        return 1
    if unexpected:
        print(f"\n‼️‼️ FAILED — unexpected top-level fields changed: {unexpected}")
        return 1
    print(f"\n✅ VERIFIED — {len(PP_WRITE_FIELDS)} fields written, GET-after == intended EXACTLY, 0 other fields, 0 sections.")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="kph-compile")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("validate", "render", "diff", "apply"):
        p = sub.add_parser(c); p.add_argument("kp")
        if c == "apply":
            p.add_argument("--i-have-liams-go", action="store_true")
            p.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    if a.cmd == "validate": sys.exit(cmd_validate(a.kp))
    if a.cmd == "render":   cmd_render(a.kp); sys.exit(0)
    if a.cmd == "diff":     sys.exit(cmd_diff(a.kp))
    if a.cmd == "apply":    sys.exit(cmd_apply(a.kp, a.i_have_liams_go, a.dry))


if __name__ == "__main__":
    main()
