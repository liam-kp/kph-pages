// ============================================================================
// KPH Investor Panel — shared renderer for (a) dashboard_v2 Reports → PHASE 1 /
// PHASE 2 modes and (b) the standalone investor.html pitch page.
// Reads investor_data.json (aggregate only, zero PII). No token, no fetches.
// Exposes window.KPHInvestor = { renderPhase1, renderPhase2, renderTrackRecord, fmt }.
// ============================================================================
(function () {
  const CSS = `
  .inv{--i-bg:#0a0a0a;--i-bg2:#111;--i-bg3:#161616;--i-line:#1f1f1f;--i-line2:#2a2a2a;--i-t1:#fff;--i-t2:#999;--i-t3:#5a5a5a;
       --i-green:#00d68f;--i-greenb:#00ff9d;--i-gold:#d4a843;--i-goldb:#f5c84b;--i-red:#ff3358;--i-blue:#4a90d9;
       font-family:'Inter',system-ui,sans-serif;color:var(--i-t1);}
  .inv *{box-sizing:border-box;margin:0;padding:0}
  .inv .mono{font-family:'JetBrains Mono',ui-monospace,monospace;font-feature-settings:'tnum'}
  .inv-sec{margin:28px 0}
  .inv-sec-title{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--i-t3);margin-bottom:14px;display:flex;align-items:center;gap:12px}
  .inv-sec-title .g{color:var(--i-goldb)} .inv-sec-title:after{content:'';flex:1;height:1px;background:var(--i-line)}
  .inv-tag{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;padding:3px 8px;border-radius:2px;border:1px solid var(--i-line2);color:var(--i-t2)}
  .inv-tag.live{color:var(--i-green);border-color:rgba(0,214,143,.3);background:rgba(0,214,143,.06)}
  .inv-tag.rep{color:var(--i-gold);border-color:rgba(212,168,67,.35);background:rgba(212,168,67,.06)}
  .inv-tag.demo{color:var(--i-blue);border-color:rgba(74,144,217,.4);background:rgba(74,144,217,.08)}
  .inv-tag.hist{color:var(--i-t2)}
  .inv-grid{display:grid;gap:1px;background:var(--i-line);border:1px solid var(--i-line)}
  .inv-grid.c4{grid-template-columns:repeat(4,1fr)} .inv-grid.c3{grid-template-columns:repeat(3,1fr)} .inv-grid.c5{grid-template-columns:repeat(5,1fr)}
  @media(max-width:860px){.inv-grid.c4,.inv-grid.c5{grid-template-columns:repeat(2,1fr)} .inv-grid.c3{grid-template-columns:1fr}}
  .inv-cell{background:var(--i-bg2);padding:18px 20px;position:relative}
  .inv-cell .l{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--i-t3);margin-bottom:10px}
  .inv-cell .v{font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:700;line-height:1;letter-spacing:-1px}
  .inv-cell .v.g{color:var(--i-greenb)} .inv-cell .v.y{color:var(--i-goldb)} .inv-cell .v.r{color:var(--i-red)} .inv-cell .v.b{color:var(--i-blue)} .inv-cell .v.m{color:var(--i-t3);font-size:18px}
  .inv-cell .s{font-size:10px;color:var(--i-t3);margin-top:8px;font-family:'JetBrains Mono',monospace;line-height:1.5}
  .inv-funnel{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--i-line);border:1px solid var(--i-line)}
  @media(max-width:860px){.inv-funnel{grid-template-columns:repeat(2,1fr)}}
  .inv-step{background:var(--i-bg2);padding:16px 12px 14px;position:relative;text-align:center}
  .inv-step .l{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:1.5px;text-transform:uppercase;color:var(--i-t3);margin-bottom:8px;min-height:22px}
  .inv-step .v{font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:700;color:var(--i-greenb);letter-spacing:-.5px}
  .inv-step .v.y{color:var(--i-goldb)} .inv-step .v.r{color:var(--i-red)} .inv-step .v.b{color:var(--i-blue)} .inv-step .v.m{color:var(--i-t3)}
  .inv-step .p{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--i-t2);margin-top:6px}
  .inv-step .c{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--i-gold);margin-top:3px}
  .inv-step .bar{height:3px;background:var(--i-bg3);margin-top:10px;overflow:hidden}
  .inv-step .bar i{display:block;height:100%;background:linear-gradient(90deg,var(--i-green),var(--i-greenb))}
  .inv-step.rep .bar i{background:linear-gradient(90deg,var(--i-gold),var(--i-goldb))}
  .inv-step.rep{background:repeating-linear-gradient(135deg,var(--i-bg2) 0 6px,#141200 6px 7px)}
  .inv-step.demo{border-top:2px dashed rgba(74,144,217,.5)} .inv-step.demo .bar i{background:var(--i-blue)}
  .inv-note{font-size:11px;line-height:1.7;color:var(--i-t2);margin-top:12px;padding:12px 14px;border-left:2px solid var(--i-line2);background:var(--i-bg2)}
  .inv-note b{color:var(--i-t1)} .inv-note code{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--i-gold)}
  .inv-note.rep{border-left-color:var(--i-gold)} .inv-note.demo{border-left-color:var(--i-blue)}
  .inv-table{width:100%;border-collapse:collapse;font-size:12px;border:1px solid var(--i-line)}
  .inv-table th{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--i-t3);text-align:left;padding:10px 12px;border-bottom:1px solid var(--i-line);background:var(--i-bg3);font-weight:500}
  .inv-table td{padding:10px 12px;border-bottom:1px solid var(--i-line);font-family:'JetBrains Mono',monospace;color:var(--i-t2)}
  .inv-table td:first-child{color:var(--i-t1);font-family:'Inter',sans-serif}
  .inv-table td.g{color:var(--i-greenb)} .inv-table td.y{color:var(--i-goldb)} .inv-table tr:hover td{background:var(--i-bg3)}
  .inv[dir=rtl] .inv-table th,.inv[dir=rtl] .inv-table td{text-align:right}
  .inv-loop{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
  .inv-loop .n{background:var(--i-bg2);border:1px dashed rgba(74,144,217,.45);padding:14px;position:relative;font-size:11.5px;line-height:1.55;color:var(--i-t2)}
  .inv-loop .n b{display:block;color:var(--i-t1);font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px}
  .inv-loop .n i{position:absolute;top:8px;right:10px;font-style:normal;font-family:'JetBrains Mono',monospace;font-size:20px;color:rgba(74,144,217,.35);font-weight:700}
  .inv[dir=rtl] .inv-loop .n i{right:auto;left:10px}
  .inv-input{display:inline-block;min-width:60px;padding:2px 8px;border:1px dashed var(--i-gold);color:var(--i-goldb);font-family:'JetBrains Mono',monospace;font-size:12px;border-radius:2px}
  `;
  function ensureCSS() {
    if (document.getElementById('inv-style')) return;
    const s = document.createElement('style'); s.id = 'inv-style'; s.textContent = CSS; document.head.appendChild(s);
  }

  const I18N = {
    en: {
      spend:'Media spend', convs:'WhatsApp conversations', leads:'Leads in CRM', engaged:'Engaged (≥1 message)', multi:'Replied to the AI (≥2)', deep:'Real conversation (≥5)',
      hot:'HOT / WARM', island:'On island / arriving', calls:'Phone calls', meetings:'Meetings held', contracts:'Contracts', closings:'Closings (in signing)',
      sales:'Total sales', comm:'Total commissions', cpl:'cost / lead', cpe:'cost / engaged', cpm:'cost / meeting', cpc:'cost / closing', cpconv:'cost / conversation', cph:'cost / hot-warm', cpcall:'cost / call',
      await:'awaiting', awaitSub:'not yet in the system — Liam to confirm', none:'none attributable',
      lay1:'System-recorded · 2026 pilot', lay2:'Reconstructed · backup + reminder bot', lay3:'Track record · all-time ledger', demo:'ILLUSTRATIVE · not real data',
      ofPrev:'of previous', fromSpend:'of media spend',
      tr_won:'Closed deals', tr_sales:'Sales volume', tr_camp:'Campaign-sourced', tr_cycle:'Avg. sales cycle', tr_days:'days', tr_comm:'Gross commission', tr_commHidden:'on request',
      byCamp:'By campaign', campNote:'Aligned window. Rows + unattributed link-click tests reconcile to the spend and conversations above. Per-campaign leads count only records carrying a campaign tag ({tagged} of {all}), so campaign-level cost per lead is a ceiling, not the blended figure.', unattr:'Unattributed', camp:'Campaign', spendc:'Spend', convc:'Conversations', leadsc:'CRM leads', eng:'Engaged', multic:'>1 reply', hotc:'Hot/Warm', cplc:'$ / lead',
      engine:'What the engine did', ai:'AI messages sent', team:'Human messages sent', fu:'Automated follow-ups', inbound:'Customer messages received', reply:'Best-week reply rate',
      replySub:'re-engagement waves to cold leads', p2title:'Closed loop — how the full report works',
      loop:[['Lead arrives','Any source — Meta, Google, portal, referral — lands in one WhatsApp number. CRM record created automatically.'],
            ['AI qualifies','Bot answers in the lead\'s language, sends the right project, scores HOT / WARM / COLD, captures arrival dates.'],
            ['Call logged','Agent taps "called" in the panel. Outcome + next step recorded on the lead. No spreadsheet.'],
            ['Meeting booked','Meeting date written to the record. Reminder fires. No-show → automatic re-book follow-up.'],
            ['Outcome tracked','Contract / closing / lost logged once. Commission attached to the originating campaign.'],
            ['Cost recomputes','Cost per call, meeting and closing update live, per campaign and per source. Media budget follows what converts.']],
      p1note:'<b>Three layers, three denominators — deliberately not blended.</b> Green tiles are system-recorded from Meta Ads + the CRM + the WhatsApp message store. Gold tiles are stages the pilot ran but never logged into the system; calls and meetings were reconstructed from the phone\'s WhatsApp call log, lead chats and the reminder bot, closings are Liam-reported — each tile says which. The all-time ledger proves closing ability, not pilot ROI — all 17 first-contacts predate the 2026 media spend.',
      alignedNote:'Cost ratios use the spend from {win} ({spend}) so numerator and denominator cover the same leads; lifetime spend since {lwin} is {lspend}.',
      nonMedia:'The CRM holds {c} leads created in 2026; {n} are non-media imports (dormant re-activation, manual, reminder-bot backlog) and are excluded, so every stage above is computed on the {m} media-origin leads.',
    },
    he: {
      spend:'הוצאת מדיה', convs:'שיחות וואטסאפ', leads:'לידים ב-CRM', engaged:'Engaged (≥1 הודעה)', multi:'ענו ל-AI (≥2)', deep:'שיחה אמיתית (≥5)',
      hot:'HOT / WARM', island:'באי / מגיעים', calls:'שיחות טלפון', meetings:'פגישות', contracts:'חוזים', closings:'סגירות (בחתימה)',
      sales:'סך מכירות', comm:'סך עמלות', cpl:'עלות / ליד', cpe:'עלות / engaged', cpm:'עלות / פגישה', cpc:'עלות / סגירה', cpconv:'עלות / שיחה', cph:'עלות / ליד חם', cpcall:'עלות / שיחת טלפון',
      await:'ממתין', awaitSub:'לא במערכת — ליאם משלים', none:'אין ייחוס',
      lay1:'נרשם במערכת · פיילוט 2026', lay2:'שוחזר · גיבוי + בוטי', lay3:'טרק-רקורד · כל הזמנים', demo:'המחשה · לא נתונים אמיתיים',
      ofPrev:'מהשלב הקודם', fromSpend:'מהוצאת המדיה',
      tr_won:'עסקאות סגורות', tr_sales:'היקף מכירות', tr_camp:'מקור קמפיין', tr_cycle:'מחזור מכירה ממוצע', tr_days:'ימים', tr_comm:'עמלה ברוטו', tr_commHidden:'מוסתר',
      byCamp:'לפי קמפיין', campNote:'חלון מיושר. השורות + בדיקות link-click לא-מיוחסות מסתכמות בדיוק להוצאה ולשיחות שלמעלה. לידים לפי קמפיין סופרים רק רשומות עם תג קמפיין ({tagged} מתוך {all}), ולכן עלות-לליד ברמת קמפיין היא תקרה, לא הממוצע המשוקלל.', unattr:'לא מיוחס', camp:'קמפיין', spendc:'הוצאה', convc:'שיחות', leadsc:'לידים', eng:'Engaged', multic:'>1 תשובה', hotc:'חם/פושר', cplc:'$ / ליד',
      engine:'מה המנוע עשה', ai:'הודעות AI שנשלחו', team:'הודעות אנושיות', fu:'פולואפים אוטומטיים', inbound:'הודעות שהתקבלו מלקוחות', reply:'אחוז תגובה שבוע שיא',
      replySub:'גלי הפעלה מחדש ללידים קרים', p2title:'לופ סגור — איך הדוח המלא עובד',
      loop:[['ליד נכנס','מכל מקור — מטא, גוגל, פורטל, הפניה — נוחת במספר וואטסאפ אחד. רשומת CRM נוצרת אוטומטית.'],
            ['AI מסנן','הבוט עונה בשפת הליד, שולח את הפרויקט הנכון, מדרג HOT / WARM / COLD, אוסף תאריכי הגעה.'],
            ['שיחה נרשמת','הסוכן מסמן "התקשרתי" בפאנל. תוצאה + צעד הבא נשמרים על הליד. בלי אקסל.'],
            ['פגישה נקבעת','תאריך הפגישה נכתב לרשומה. תזכורת יוצאת. לא הגיע → פולואפ אוטומטי לקביעה מחדש.'],
            ['תוצאה נרשמת','חוזה / סגירה / אבוד נרשם פעם אחת. העמלה מוצמדת לקמפיין המקור.'],
            ['העלות מתעדכנת','עלות לשיחה, לפגישה ולסגירה מתעדכנות חי, לפי קמפיין ולפי מקור. תקציב המדיה הולך אחרי מה שממיר.']],
      p1note:'<b>שלוש שכבות, שלושה מכנים — בכוונה לא מעורבבים.</b> אריחים ירוקים נרשמו במערכת (Meta Ads + CRM + מאגר ההודעות). אריחי זהב הם שלבים שהפיילוט ביצע אבל לא נרשמו — שיחות ופגישות שוחזרו מיומן השיחות של וואטסאפ בטלפון, משיחות הלידים ומהבוטי; סגירות מדווחות על ידי ליאם — כל אריח אומר מאיפה. הטרק-רקורד מוכיח יכולת סגירה, לא ROI של הפיילוט — כל 17 העסקאות נוצרו לפני הוצאת המדיה של 2026.',
      alignedNote:'יחסי העלות משתמשים בהוצאה של {win} ({spend}) כדי שהמונה והמכנה יכסו את אותם לידים; הוצאה מצטברת מ-{lwin}: {lspend}.',
      nonMedia:'ב-CRM יש {c} לידים שנוצרו ב-2026; {n} הם ייבואים שלא ממדיה (הפעלה מחדש, ידני, בקלוג בוטי) והוצאו, כך שכל השלבים למעלה מחושבים על {m} לידים ממקור מדיה.',
    }
  };

  const fmt = {
    usd: (n, d = 0) => n == null ? '—' : '$' + Number(n).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }),
    num: (n) => n == null ? '—' : Number(n).toLocaleString('en-US'),
    pct: (a, b) => (!b) ? '—' : (100 * a / b).toFixed(a / b < 0.1 ? 1 : 0) + '%',
    thbM: (n) => n == null ? '—' : '฿' + (n / 1e6).toFixed(1) + 'M',
    usdFromThb: (thb, fx) => '$' + (thb / fx / 1e6).toFixed(2) + 'M',
  };
  const esc = (s) => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const tpl = (s, vars) => s.replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? '');

  function step(label, value, opts = {}) {
    const { cls = '', prev = null, cost = null, t, pct = null, sub = null, kind = '' } = opts;
    const p = pct !== null ? pct : (prev ? fmt.pct(value, prev) : '');
    const barW = prev && value != null ? Math.max(3, Math.min(100, 100 * value / prev)) : (value != null ? 100 : 0);
    return `<div class="inv-step ${kind}">
      <div class="l">${label}</div>
      <div class="v ${cls}">${value == null ? `<span class="m">${t.await}</span>` : (typeof value === 'number' ? fmt.num(value) : value)}</div>
      ${p ? `<div class="p">${p} ${t.ofPrev}</div>` : ''}${sub ? `<div class="p" style="font-size:8.5px;color:var(--i-t3);line-height:1.35">${sub}</div>` : (p ? '' : '<div class="p">&nbsp;</div>')}
      ${cost ? `<div class="c">${cost}</div>` : ''}
      <div class="bar"><i style="width:${barW}%"></i></div>
    </div>`;
  }

  function renderPhase1(data, opts = {}) {
    ensureCSS();
    const lang = opts.lang || 'en', t = I18N[lang], dir = lang === 'he' ? 'rtl' : 'ltr';
    const m = data.media, a = m.aligned, L = m.lifetime, f = data.funnel, r = data.reported, e = data.engine, fx = data.meta.fx.thb_per_usd;
    const spend = a.spend_usd;
    const cp = (n) => n ? fmt.usd(spend / n, 2) : null;
    const rep = (v) => v == null ? null : v;
    const rnote = (k) => r[k + '_note' + (lang === 'he' ? '_he' : '')] || r[k + '_note'] || t.awaitSub;

    const funnel = `
      <div class="inv-funnel">
        ${step(t.spend, fmt.usd(spend), { cls: 'y', t, sub: a.window })}
        ${step(t.convs, a.conversations_started, { t, cost: cp(a.conversations_started) + ' ' + t.cpconv, sub: 'Meta-attributed' })}
        ${step(t.leads, f.leads_media_origin, { t, prev: a.conversations_started, cost: cp(f.leads_media_origin) + ' ' + t.cpl })}
        ${step(t.engaged, f.engaged_1plus, { t, prev: f.leads_media_origin, cost: cp(f.engaged_1plus) + ' ' + t.cpe })}
        ${step(t.multi, f.engaged_2plus, { t, prev: f.engaged_1plus })}
        ${step(t.deep, f.engaged_5plus, { t, prev: f.engaged_2plus })}
        ${step(t.hot, f.hot_warm, { t, prev: f.engaged_1plus, cost: cp(f.hot_warm) + ' ' + t.cph })}
        ${step(t.calls, rep(r.phone_calls), { t, kind: 'rep', cls: 'y', prev: r.phone_calls != null ? f.engaged_1plus : null, cost: r.phone_calls ? cp(r.phone_calls) + ' ' + t.cpcall : null, sub: rnote('phone_calls') })}
        ${step(t.meetings, rep(r.meetings_held), { t, kind: 'rep', cls: 'y', prev: r.meetings_held != null && r.phone_calls != null ? r.phone_calls : null, cost: r.meetings_held ? cp(r.meetings_held) + ' ' + t.cpm : null, sub: rnote('meetings') })}
        ${step(t.closings, rep(r.closings), { t, kind: 'rep', cls: 'y', prev: r.closings != null && r.meetings_held != null ? r.meetings_held : null, cost: r.closings ? cp(r.closings) + ' ' + t.cpc : null, sub: rnote('closings') })}
      </div>`;

    const rows = f.by_campaign.map(c => {
      const mc = (m.campaigns || []).find(x => x.code === c.code) || {};
      return `<tr><td>${esc(c.label)} <span class="mono" style="color:var(--i-t3);font-size:10px">${c.code}</span></td>
        <td class="y">${mc.spend_usd != null ? fmt.usd(mc.spend_usd) : '—'}</td><td>${mc.conversations != null ? fmt.num(mc.conversations) : '—'}</td>
        <td class="g">${fmt.num(c.leads)}</td><td>${fmt.num(c.engaged_1plus)} <span style="color:var(--i-t3)">${fmt.pct(c.engaged_1plus, c.leads)}</span></td>
        <td>${fmt.num(c.engaged_2plus)}</td><td>${fmt.num(c.hot_warm)}</td><td class="y">${mc.spend_usd != null ? fmt.usd(mc.spend_usd / c.leads, 2) : '—'}</td></tr>`;
    }).join('') + (m.unattributed ? `<tr><td style="color:var(--i-t3)">${esc(m.unattributed.label)}</td><td class="y">${fmt.usd(m.unattributed.spend_usd)}</td><td style="color:var(--i-t3)">— (${fmt.num(m.unattributed.link_clicks)} clicks)</td><td colspan="5" style="color:var(--i-t3)">${t.unattr}</td></tr>` : '');

    return `<div class="inv" dir="${dir}">
      <div class="inv-sec">
        <div class="inv-sec-title"><span class="g">▸</span> ${lang === 'he' ? 'שלב 1 — פיילוט קופנגן, מקצה לקצה' : 'Phase 1 — Koh Phangan pilot, end to end'}
          <span class="inv-tag live">${t.lay1}</span><span class="inv-tag rep">${t.lay2}</span></div>
        ${funnel}
        <div class="inv-note">${t.p1note}<br>${tpl(t.alignedNote, { win: a.window, spend: fmt.usd(spend, 2), lwin: L.window.split(' ')[0], lspend: fmt.usd(L.spend_usd, 2) })}
          ${tpl(t.nonMedia, { c: fmt.num(f.leads_in_crm), n: f.leads_non_media_imports, m: fmt.num(f.leads_media_origin) })}</div>
        ${r.method ? `<div class="inv-note rep"><b>${lang === 'he' ? 'שחזור אריחי הזהב.' : 'Reconstruction of the gold tiles.'}</b> ${esc(lang === 'he' && r.method_he ? r.method_he : r.method)}${r.phone_calls_floor_note ? ' ' + esc(r.phone_calls_floor_note) : ''}</div>` : ''}
      </div>
      <div class="inv-sec">
        <div class="inv-sec-title"><span class="g">▸</span> ${t.byCamp}<span class="inv-tag live">${t.lay1}</span></div>
        <div style="overflow-x:auto"><table class="inv-table"><thead><tr><th>${t.camp}</th><th>${t.spendc}</th><th>${t.convc}</th><th>${t.leadsc}</th><th>${t.eng}</th><th>${t.multic}</th><th>${t.hotc}</th><th>${t.cplc}</th></tr></thead><tbody>${rows}</tbody></table></div>
        <div class="inv-note">${tpl(t.campNote, { tagged: fmt.num(f.leads_campaign_attributed), all: fmt.num(f.leads_media_origin) })}</div>
      </div>
      <div class="inv-sec">
        <div class="inv-sec-title"><span class="g">▸</span> ${t.engine}<span class="inv-tag live">${t.lay1}</span></div>
        <div class="inv-grid c5">
          <div class="inv-cell"><div class="l">${t.ai}</div><div class="v g">${fmt.num(e.ai_outbound_messages)}</div></div>
          <div class="inv-cell"><div class="l">${t.fu}</div><div class="v g">${fmt.num(e.followups_sent)}</div><div class="s">${Object.entries(e.followups_by_trigger).slice(0, 3).map(([k, v]) => k + ' ' + v).join(' · ')}</div></div>
          <div class="inv-cell"><div class="l">${t.inbound}</div><div class="v">${fmt.num(e.customer_inbound_messages)}</div></div>
          <div class="inv-cell"><div class="l">${t.team}</div><div class="v">${fmt.num(e.team_outbound_messages)}</div></div>
          <div class="inv-cell"><div class="l">${t.reply}</div><div class="v y">${e.best_week_reply_rate.rate}%</div><div class="s">${e.best_week_reply_rate.replies}/${e.best_week_reply_rate.delivered} · ${t.replySub}</div></div>
        </div>
      </div>
      ${renderTrackRecord(data, opts)}
    </div>`;
  }

  function renderTrackRecord(data, opts = {}) {
    ensureCSS();
    const lang = opts.lang || 'en', t = I18N[lang], dir = lang === 'he' ? 'rtl' : 'ltr';
    const tr = data.track_record, fx = data.meta.fx.thb_per_usd;
    const yrs = tr.by_year.map(y => `<tr><td>${y.year}</td><td class="g">${y.deals}</td><td class="y">${fmt.thbM(y.sales_thb)} <span style="color:var(--i-t3)">${fmt.usdFromThb(y.sales_thb, fx)}</span></td></tr>`).join('');
    return `<div class="inv" dir="${dir}"><div class="inv-sec">
      <div class="inv-sec-title"><span class="g">▸</span> ${lang === 'he' ? 'טרק-רקורד — עסקאות סגורות' : 'Track record — closed deals'}<span class="inv-tag hist">${t.lay3}</span></div>
      <div class="inv-grid c4">
        <div class="inv-cell"><div class="l">${t.tr_won}</div><div class="v g">${tr.closed_won}</div><div class="s">2023 → 2026</div></div>
        <div class="inv-cell"><div class="l">${t.tr_sales}</div><div class="v y">${fmt.thbM(tr.sales_thb)}</div><div class="s">≈ ${fmt.usdFromThb(tr.sales_thb, fx)}</div></div>
        <div class="inv-cell"><div class="l">${t.tr_camp}</div><div class="v">${tr.campaign_share_by_count_pct}%</div><div class="s">${tr.campaign_sourced_deals} / ${tr.closed_won} deals · ${fmt.thbM(tr.campaign_sourced_sales_thb)}</div></div>
        <div class="inv-cell"><div class="l">${tr.show_commission ? t.tr_comm : t.tr_cycle}</div><div class="v ${tr.show_commission ? 'y' : ''}">${tr.show_commission ? fmt.thbM(tr.gross_commission_thb) : tr.avg_cycle_days}</div><div class="s">${tr.show_commission ? '≈ ' + fmt.usdFromThb(tr.gross_commission_thb, fx) : t.tr_days}</div></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px;align-items:start">
        <table class="inv-table"><thead><tr><th>Year</th><th>${t.tr_won}</th><th>${t.tr_sales}</th></tr></thead><tbody>${yrs}</tbody></table>
        <div class="inv-note" style="margin-top:0">${esc(tr.note)}${data.pipeline && data.pipeline.signing_2026 ? `<br><b>${lang === 'he' ? 'בחתימה כעת (2026)' : 'In signing now (2026)'}:</b> ${data.pipeline.signing_2026.deals} ${lang === 'he' ? 'עסקאות' : 'deals'} · ${fmt.thbM(data.pipeline.signing_2026.sales_thb)} · ${lang === 'he' ? 'עמלה' : 'commission'} ${fmt.thbM(data.pipeline.signing_2026.commission_thb)}${data.pipeline.signing_2026.paid ? '' : (lang === 'he' ? ' · טרם שולם' : ' · not yet paid')}. ${lang === 'he' ? 'לא נספרות כמכירות עד ההשלמה.' : 'Not counted as sales until completed.'}` : ''}</div>
      </div>
    </div></div>`;
  }

  function renderPhase2(data, opts = {}) {
    ensureCSS();
    const lang = opts.lang || 'en', t = I18N[lang], dir = lang === 'he' ? 'rtl' : 'ltr';
    const d = data.phase2_demo;
    const cp = (n) => fmt.usd(d.spend_usd / n, 0);
    const sales = d.closings * d.avg_deal_usd, comm = sales * d.commission_pct / 100;
    const s = (label, v, prev, cost) => step(label, v, { t, prev, cost, kind: 'demo', cls: 'b' });
    return `<div class="inv" dir="${dir}">
      <div class="inv-sec">
        <div class="inv-sec-title"><span class="g">▸</span> ${lang === 'he' ? 'שלב 2 — הדוח המלא, כשהלופ סגור' : 'Phase 2 — the full report, once the loop is closed'}<span class="inv-tag demo">${t.demo}</span></div>
        <div class="inv-funnel">
          ${step(t.spend, fmt.usd(d.spend_usd), { cls: 'b', t, kind: 'demo', sub: lang === 'he' ? 'דוגמה · חודש' : 'example · one month' })}
          ${s(t.convs, d.conversations, null, cp(d.conversations) + ' ' + t.cpconv)}
          ${s(t.leads, d.leads, d.conversations, cp(d.leads) + ' ' + t.cpl)}
          ${s(t.engaged, d.engaged, d.leads, cp(d.engaged) + ' ' + t.cpe)}
          ${s(t.multi, d.multi_reply, d.engaged)}
          ${s(t.calls, d.calls, d.multi_reply, cp(d.calls))}
          ${s(t.meetings, d.meetings, d.calls, cp(d.meetings) + ' ' + t.cpm)}
          ${s(t.closings, d.closings, d.meetings, cp(d.closings) + ' ' + t.cpc)}
          ${step(t.sales, fmt.usd(sales), { cls: 'b', t, kind: 'demo', sub: fmt.usd(d.avg_deal_usd) + ' avg' })}
          ${step(t.comm, fmt.usd(comm), { cls: 'b', t, kind: 'demo', sub: d.commission_pct + '% · ' + (comm / d.spend_usd).toFixed(1) + '× ' + t.fromSpend })}
        </div>
        <div class="inv-note demo"><b>${t.demo}.</b> ${esc(d.note)}</div>
      </div>
      <div class="inv-sec">
        <div class="inv-sec-title"><span class="g">▸</span> ${t.p2title}<span class="inv-tag demo">${t.demo}</span></div>
        <div class="inv-loop">${t.loop.map(([h, b], i) => `<div class="n"><i>${i + 1}</i><b>${h}</b>${b}</div>`).join('')}</div>
      </div>
    </div>`;
  }

  window.KPHInvestor = { renderPhase1, renderPhase2, renderTrackRecord, fmt, I18N };
})();
