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
    # per-config price tokens (KPR-284 Step 5 — §18 8-config table renders each config's exact price from SSOT)
    for c in ssot["configs"]:
        t[f"KP-ZEN-012.cfg.{c['unit_type']}.thb"] = money("฿", c["price_thb"])
    return t


# ---------- generic (non-ZEN-012) token derivation (KPR-284 Step 3 rollout) ----------
# Every project except the KP-ZEN-012 pilot declares a flat SSOT:
#   {"schema":"generic-v1","project_id":..,"price_points":[{"name","thb","label_en"..}],
#    optional "range":{"thb_lo","thb_hi"}}
# Tokens are namespaced by project id, so a SHARED prompt-section can resolve pivot prices for
# ANY project it mentions ({{KP-BCH-011.villa1.usd}}). Converted currencies derive from fx.json
# and are display-rounded to nearest 100 (Step 1); THB is shown in full.
def derive_generic(kp, ssot, fx):
    t = {}
    for p in ssot.get("price_points", []):
        thb, name = p["thb"], p["name"]
        a = fx_amounts(thb, fx)
        t[f"{kp}.{name}.thb"]   = money("฿", thb)
        t[f"{kp}.{name}.thb_m"] = f"฿{millions(thb)}M"
        t[f"{kp}.{name}.usd"]   = money("$", a["usd"])
        t[f"{kp}.{name}.eur"]   = money("€", a["eur"])
        t[f"{kp}.{name}.ils"]   = money("₪", a["ils"])
    rg = ssot.get("range")
    if rg:
        lo, hi = rg["thb_lo"], rg["thb_hi"]
        alo, ahi = fx_amounts(lo, fx), fx_amounts(hi, fx)
        t[f"{kp}.range.thb"]   = f"{money('฿', lo)}–{money('฿', hi)}"
        t[f"{kp}.range.thb_m"] = f"฿{millions(lo)}M–฿{millions(hi)}M"
        t[f"{kp}.range.usd"]   = f"{money('$', alo['usd'])}–{money('$', ahi['usd'])}"
        t[f"{kp}.range.eur"]   = f"{money('€', alo['eur'])}–{money('€', ahi['eur'])}"
        t[f"{kp}.range.ils"]   = f"{money('₪', alo['ils'])}–{money('₪', ahi['ils'])}"
    return t


def derive_project_tokens(kp, ssot, fx):
    """Dispatch by SSOT shape: the KP-ZEN-012 pilot uses the rich band/config derive
    (byte-identical to before); every other project uses the generic price_points derive."""
    return derive_tokens(ssot, fx) if "band_pricing" in ssot else derive_generic(kp, ssot, fx)


def build_global_tokens(fx):
    """Union of every scaffolded project's namespaced tokens, so a shared prompt-section can
    resolve pivot prices for any project it references."""
    t, pdir = {}, os.path.join(DATA, "projects")
    for kp in sorted(os.listdir(pdir)):
        inv = os.path.join(pdir, kp, "inventory.json")
        if os.path.isfile(inv):
            t.update(derive_project_tokens(kp, json.load(open(inv)), fx))
    return t


def render_text(tmpl, tokens):
    """Resolve {{token}} -> display string."""
    def sub(m):
        k = m.group(1).strip()
        if k not in tokens:
            raise KeyError(f"unresolved token {{{{{k}}}}}")
        return tokens[k]
    return re.sub(r"\{\{([^}]+)\}\}", sub, tmpl)


# ---------- pivot router (KPR-302 step 4) ----------
PIVOT_ROUTER_HEADER = """\
\U0001f6a8 SECTION GATE — GLOBAL, CONDITION-ROUTED (NOT project-locked)
═════════════════════════════════════════════════════════════════════════════
IF no project_id locked — STOP, defer to section 26-project-focus-lock's
"ASK, NEVER GUESS" rule. This section NEVER fires first and NEVER substitutes
for project detection.
═════════════════════════════════════════════════════════════════════════════

\U0001f501 PIVOT ROUTER — cross-project budget pivots (KPR-302)

This section EXTENDS section 26's Price-Collision Guard — it does not bypass it.
Only activates for the CURRENTLY LOCKED project_id, and only after an explicit
budget objection ("too expensive" / "out of my budget" / "anything cheaper?")
or 3+ silent follow-ups — never during initial presentation (same gate as the
per-campaign pivot blocks in sections 17/18/20/22 this section will eventually
replace — see step 5, not yet applied).

Every price below is a namespaced token resolved from that project's own
data/projects/<KP>/inventory.json — never a literal. If a token fails to
resolve, STOP and call get_project_info; do not guess a number.
"""

PIVOT_ROUTER_FOOTER = """\
═════════════════════════════════════════════════════════════════════════════
RED-FLAG CHECK before sending any pivot line: does the quoted price/unit name
trace to the TARGET project's own inventory.json token? If it was typed
literally instead of substituted from a token — DO NOT SEND, re-render.
"""


def load_pivot(kp):
    p = os.path.join(proj_dir(kp), "pivot.json")
    return json.load(open(p)) if os.path.isfile(p) else None


def render_pivot_router(fx):
    """Compile ALL data/projects/<KP>/pivot.json files into the single
    34-pivot-router.tmpl body. Tokens are left UNRESOLVED ({{...}} placeholders
    stay literal) -- this produces a .tmpl, same contract as every other
    sections-home file; render_text()/apply_section() resolve tokens later,
    at the same point every other section does.
    Read-only: does not touch Firebase. Does not overwrite pivot.json (source).
    """
    pdir = os.path.join(DATA, "projects")
    blocks = []
    for kp in sorted(os.listdir(pdir)):
        piv = load_pivot(kp)
        if not piv:
            continue
        lines = [f"### PIVOT FROM {kp}", ""]
        for t in piv.get("pivot_targets", []):
            trig = t.get("trigger", "?")
            note = t.get("budget_range_note") or t.get("note") or ""
            target = t.get("target_project_id")
            alt = t.get("target_project_id_alt")
            tgt_str = target if target else "(none -- out of range, no pivot)"
            if alt:
                tgt_str += f" (alt: {alt})"
            lines.append(f"IF project_id = {kp} AND trigger = {trig} "
                         f"{'(' + note + ')' if note else ''} -> OFFER {tgt_str}")
            if t.get("line_he"):
                lines.append(f"HE:\n{t['line_he']}")
            if t.get("line_en"):
                lines.append(f"EN:\n{t['line_en']}")
            lines.append("")
        if piv.get("budget_unknown_line_he") or piv.get("budget_unknown_line_en"):
            lines.append(f"IF project_id = {kp} AND trigger = budget_unknown_or_below_range -> ask, do not guess:")
            if piv.get("budget_unknown_line_he"):
                lines.append(f"HE:\n{piv['budget_unknown_line_he']}")
            if piv.get("budget_unknown_line_en"):
                lines.append(f"EN:\n{piv['budget_unknown_line_en']}")
            lines.append("")
        blocks.append("\n".join(lines))
    return PIVOT_ROUTER_HEADER + "\n---\n\n" + "\n---\n\n".join(blocks) + "\n" + PIVOT_ROUTER_FOOTER


def cmd_render_pivot(write=False):
    """Read-only by default: prints the compiled router text.
    write=True writes ONLY the local .tmpl file (sections-home) -- NEVER Firebase."""
    fx = load_fx()
    tmpl_text = render_pivot_router(fx)
    tokens = build_global_tokens(fx)
    print("=== render-pivot -- compiled 34-pivot-router.tmpl (tokens UNRESOLVED, as-authored) ===\n")
    print(tmpl_text)
    print("\n=== same content with tokens RESOLVED (preview of what apply-section would render) ===\n")
    try:
        print(render_text(tmpl_text, tokens))
    except KeyError as e:
        print(f"‼️ UNRESOLVED TOKEN: {e}")
        return 1
    out = os.path.join(DATA, "projects", "KP-ZEN-012", "sections", "34-pivot-router.tmpl")
    if write:
        open(out, "w").write(tmpl_text)
        print(f"\nwritten (local file only, no Firebase): {out}")
    else:
        print(f"\n(dry -- not written; would write to {out})")
    return 0


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
    # Only the KP-ZEN-012 pilot renders a Projects_Public price block from SSOT; generic
    # rollout projects tokenize prompt-sections only (their PP prose is not rendered here).
    if "band_pricing" not in ssot:
        return {}
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
    tokens = build_global_tokens(fx)   # global: shared sections resolve cross-project pivot tokens
    problems = []
    for r in ("thb_to_usd", "thb_to_eur", "thb_to_ils"):
        if not fx.get(r): problems.append(f"fx.json missing {r}")
    if "band_pricing" in ssot:
        # KP-ZEN-012 pilot: rich band/config/ladder consistency checks
        for b in ssot["band_pricing"]:
            for c in ("thb", "usd", "eur", "ils"):
                if not b.get(c): problems.append(f"band {b['band']} missing {c}")
        for b in ssot["public_ladder"]:
            cps = [next((x["price_thb"] for x in ssot["configs"] if x["unit_type"] == ct), None)
                   for ct in b.get("configs", [])]
            cps = [p for p in cps if p]
            if cps and b.get("from_thb") and min(cps) != b["from_thb"]:
                problems.append(f"band {b['band']} from_thb {b['from_thb']} != min config {min(cps)}")
        shape = "band-pricing (pilot)"
    else:
        # generic price_points SSOT (rollout projects)
        pps = ssot.get("price_points", [])
        if not pps: problems.append("generic SSOT has no price_points")
        for p in pps:
            if not p.get("name"): problems.append(f"price_point missing name: {p}")
            if not p.get("thb"):  problems.append(f"price_point {p.get('name')} missing thb")
        shape = f"generic ({len(pps)} price_points)"
    # every token in THIS project's own templates resolves against the global table
    sdir = os.path.join(proj_dir(kp), "sections")
    missing, ntmpl = set(), 0
    if os.path.isdir(sdir):
        for f in sorted(os.listdir(sdir)):
            if f.endswith(".tmpl"):
                ntmpl += 1
                missing |= (tokens_in(open(os.path.join(sdir, f)).read()) - set(tokens))
    if missing: problems.append(f"unresolved tokens in templates: {sorted(missing)}")
    print(f"=== validate {kp} ===")
    print(f"shape: {shape} | registry fields: {len(reg['fields'])} | fx: present | "
          f"global tokens: {len(tokens)} | own templates: {ntmpl}")
    if problems:
        print("FAIL:"); [print("  -", p) for p in problems]; return 1
    print("PASS — SSOT sane, FX present, all tokens resolve globally.")
    return 0


def cmd_render(kp, outdir=None):
    ssot, fx = load_ssot(kp), load_fx()
    tokens = build_global_tokens(fx)
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


def cmd_diff_generic(kp, ssot, fx):
    """Rollout-project dry-run: derived (fx-rounded) price tokens vs the live Projects_Public
    price-bearing fields. Read-only. Section deltas for this project surface in the shared
    sections-home diff (`diff KP-ZEN-012`), which resolves every project's namespaced tokens."""
    tok = derive_generic(kp, ssot, fx)
    print(f"=== diff {kp} — generic (derived-from-SSOT vs live Projects_Public) ===\n")
    print("## Derived price tokens (THB full · USD/EUR/ILS from fx.json, nearest-100)")
    for p in ssot.get("price_points", []):
        n = p["name"]
        print(f"  {n:<12} {tok[f'{kp}.{n}.thb']:>13}  {tok[f'{kp}.{n}.usd']:>10}  "
              f"{tok[f'{kp}.{n}.eur']:>10}  {tok[f'{kp}.{n}.ils']:>12}   {p.get('label_en','')}")
    if ssot.get("range"):
        print(f"  {'range':<12} {tok[f'{kp}.range.thb']}  |  {tok[f'{kp}.range.usd']}  |  "
              f"{tok[f'{kp}.range.eur']}  |  {tok[f'{kp}.range.ils']}")
    print("\n## Live Projects_Public price-bearing fields (for reconcile)")
    live = get_projects_public(kp)
    price_fields = [k for k in sorted(live) if isinstance(live.get(k), str)
                    and re.search(r"(price|pitch|short_pitch|range|second_message|first_message)", k)]
    for k in price_fields:
        print(f"  {k} = {live[k][:180]}")
    print("\n(Any converted-currency delta live-vs-derived is the FX-consistency correction — gated, no apply.)")
    return 0


def cmd_diff(kp):
    ssot, fx = load_ssot(kp), load_fx()
    if "band_pricing" not in ssot:
        return cmd_diff_generic(kp, ssot, fx)
    tokens = build_global_tokens(fx)
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


# ---------- prompt-section apply (KPR-284 Step 5) ----------
# PUT /customers/{CID}/prompt-sections/{key}; body {content,isEnabled,sortOrder,metadata,agentId}.
# Backend upsert: isEnabled/sortOrder default to existing when omitted — we PASS them from GET-before
# so they are preserved exactly. Only `content` changes; `updatedAt` is the sole expected side-effect.
SECTION_PRESERVE = ["sectionKey", "id", "customerId", "createdAt", "isEnabled", "sortOrder", "agentId", "metadata"]


def curl_put_section(section_key, body_obj):
    data = json.dumps(body_obj, ensure_ascii=True)   # ensure_ascii for HE/emoji; never PATCH
    url = f"{BASE}/customers/{CID}/prompt-sections/{section_key}"
    return subprocess.run(
        ["curl", "-sS", "-X", "PUT", "-A", "Mozilla/5.0",
         "-H", f"Authorization: Bearer {_token()}",
         "-H", "Content-Type: application/json",
         "--data-binary", data, url],
        capture_output=True, text=True, check=True).stdout


def apply_section(section_key, confirm=False, dry=False, sort_order=None):
    if not confirm:
        print(f"=== apply-section {section_key} — GATE ===")
        print("REFUSED. Live prompt-section write requires --i-have-liams-go.")
        return 2
    fx = load_fx(); tokens = build_global_tokens(fx)
    tmpl = os.path.join(DATA, "projects", "KP-ZEN-012", "sections", section_key + ".tmpl")
    rendered = render_text(open(tmpl).read(), tokens)

    before = get_section(section_key)                       # PWRC: GET-before (full record)
    is_new = before.get("id") is None                       # wrapper returns an empty stub, not 404, for an unknown key

    if is_new:
        if sort_order is None:
            print(f"=== apply-section {section_key} — GATE ===")
            print("REFUSED. This section does not exist live yet (no id/sortOrder to preserve) — "
                  "pass --sort-order explicitly (confirm the next free slot via a live GET first; "
                  "never guess, per LES-002/003). No write issued.")
            return 2
        target_sortOrder, target_isEnabled = sort_order, True
    else:
        target_sortOrder, target_isEnabled = before["sortOrder"], before["isEnabled"]

    body = {"content": rendered,
            "isEnabled": target_isEnabled,
            "sortOrder": target_sortOrder,
            "metadata": before.get("metadata", {}),
            "agentId": before.get("agentId")}

    mode = "DRY-RUN (no PUT)" if dry else "LIVE PWRC WRITE"
    print(f"=== apply-section {section_key} — {mode}{' — NEW SECTION' if is_new else ''} ===")
    print(f"sortOrder(before)={before.get('sortOrder')}  isEnabled(before)={before.get('isEnabled')}  agentId={before.get('agentId')}")
    if is_new:
        print(f"NEW SECTION — no live record existed. Will create with sortOrder={target_sortOrder}, isEnabled={target_isEnabled}.")
    print(f"content len: live={len(before['content'])} -> rendered={len(rendered)} | content changes: {before['content'] != rendered}")
    if before["content"] == rendered:
        print("content already in sync — no write needed.")
        return 0
    if dry:
        print("=== DRY-RUN — no PUT issued. ===")
        return 0

    curl_put_section(section_key, body)                     # PUT full merged
    time.sleep(3)
    after = get_section(section_key)                        # GET-after (independent re-read)

    changed = sorted(k for k in (set(before) | set(after)) if before.get(k) != after.get(k))
    unexpected = [k for k in changed if k not in ("content", "updatedAt")]
    if is_new:
        # A create legitimately populates id/createdAt/customerId/sectionKey that were absent
        # before — only the two fields we explicitly set are enforced, not the full preserve list.
        preserved_bad = [k for k in ("isEnabled", "sortOrder") if after.get(k) != body[k]]
        # A create legitimately assigns id/createdAt/customerId/sectionKey (absent before),
        # flips source (platform stub -> customer record), echoes back a "key" field, and
        # sets sortOrder from None -> the intended value -- all expected, not anomalies.
        unexpected = [k for k in unexpected
                      if k not in ("id", "createdAt", "customerId", "sectionKey", "source", "key", "sortOrder")]
    else:
        preserved_bad = [k for k in SECTION_PRESERVE if before.get(k) != after.get(k)]
    print(f"sortOrder(after)={after['sortOrder']}  isEnabled(after)={after['isEnabled']}")
    print(f"GET-after changed keys: {changed}")

    if after["content"] != rendered:
        print(f"\n‼️‼️ FAILED — content did not verify (live != rendered). No further writes.")
        return 1
    if preserved_bad:
        print(f"\n‼️‼️ FAILED — preserved fields changed: {preserved_bad}")
        return 1
    if unexpected:
        print(f"\n‼️‼️ FAILED — unexpected fields changed: {unexpected}")
        return 1
    print(f"\n✅ VERIFIED — {section_key}: content written, sortOrder={after['sortOrder']} & isEnabled={after['isEnabled']} preserved, only content+updatedAt changed{' (+ id/createdAt/customerId newly assigned on create)' if is_new else ''}.")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="kph-compile")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("validate", "render", "diff", "apply"):
        p = sub.add_parser(c); p.add_argument("kp")
        if c == "apply":
            p.add_argument("--i-have-liams-go", action="store_true")
            p.add_argument("--dry", action="store_true")
    ps = sub.add_parser("apply-section"); ps.add_argument("section_key")
    ps.add_argument("--i-have-liams-go", action="store_true"); ps.add_argument("--dry", action="store_true")
    ps.add_argument("--sort-order", type=int, default=None, help="required only when the section doesn't exist live yet")
    rp = sub.add_parser("render-pivot")  # KPR-302 step 4: local-only, never touches Firebase
    rp.add_argument("--write", action="store_true", help="write the compiled .tmpl to sections-home (local file only)")
    a = ap.parse_args()
    if a.cmd == "validate": sys.exit(cmd_validate(a.kp))
    if a.cmd == "render":   cmd_render(a.kp); sys.exit(0)
    if a.cmd == "diff":     sys.exit(cmd_diff(a.kp))
    if a.cmd == "apply":    sys.exit(cmd_apply(a.kp, a.i_have_liams_go, a.dry))
    if a.cmd == "apply-section": sys.exit(apply_section(a.section_key, a.i_have_liams_go, a.dry, a.sort_order))
    if a.cmd == "render-pivot": sys.exit(cmd_render_pivot(a.write))


if __name__ == "__main__":
    main()
