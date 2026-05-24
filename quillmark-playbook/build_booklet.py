#!/usr/bin/env python3
"""
Quillmark POD — The Built-In Package
Generates the consolidated business playbook PDF using WeasyPrint.

Run:  python3 build_booklet.py
Out:  Quillmark-POD-Business-Playbook.pdf
"""
from weasyprint import HTML
import datetime, os

# ----------------------------------------------------------------------------
# Brand palette (reconstructed from the Quillmark brand kit: red quill nib on
# near-black, BNBHubs navy document covers).
# ----------------------------------------------------------------------------
INK    = "#0E1320"   # near-black navy (cover / dividers)
NAVY   = "#161F33"   # dark panels
PAPER  = "#FFFFFF"
TEXT   = "#1B2230"
MUTE   = "#5C footnote".replace(" footnote", "6678")  # guard against typo
MUTE   = "#5C6678"
FAINT  = "#8A93A6"
LINE   = "#E4E8F0"
SOFT   = "#F4F6FA"   # soft panel fill
FLAME  = "#EE5A2B"   # primary accent (quill nib)
FLAME2 = "#F6824F"
GOLD   = "#E9A23B"
GREEN  = "#1E9E6A"
TEAL   = "#2E8C9E"

DATE = datetime.date(2026, 5, 24).strftime("%B %-d, %Y")

# ----------------------------------------------------------------------------
# Reusable SVG: the Quillmark nib mark
# ----------------------------------------------------------------------------
def nib(size=84, color=FLAME, bg=None):
    bgrect = f'<rect width="100" height="100" rx="22" fill="{bg}"/>' if bg else ''
    return f'''
<svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  {bgrect}
  <path d="M50 12 L70 60 Q50 78 30 60 Z" fill="{color}"/>
  <path d="M50 40 L50 70" stroke="{INK if bg else PAPER}" stroke-width="3.4" stroke-linecap="round"/>
  <circle cx="50" cy="36" r="4.4" fill="{INK if bg else PAPER}"/>
</svg>'''

# ----------------------------------------------------------------------------
# Diagrams
# ----------------------------------------------------------------------------
def svg_money_machine():
    box = lambda x,t,s: f'''
      <rect x="{x}" y="40" width="150" height="86" rx="12" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>
      <text x="{x+75}" y="74" text-anchor="middle" font-size="15" font-weight="700" fill="{TEXT}">{t}</text>
      <text x="{x+75}" y="98" text-anchor="middle" font-size="11.5" fill="{MUTE}">{s}</text>'''
    arr = lambda x: f'<path d="M{x} 83 l26 0" stroke="{FLAME}" stroke-width="2.4" marker-end="url(#ar)"/>'
    return f'''
<svg viewBox="0 0 920 210" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 0 L9 4.5 L0 9 z" fill="{FLAME}"/></marker></defs>
  {box(10,"You create","one design")}{arr(160)}
  {box(196,"Quillmark store","lists it on 20+ items")}{arr(346)}
  {box(382,"Customer buys","pays full retail")}{arr(532)}
  {box(568,"Printer prints","&amp; ships to them")}{arr(718)}
  {box(754,"You keep profit","~$8&ndash;12 / item")}
  <path d="M829 126 q40 70 -380 56 q-420 16 -440 -52" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#ar)"/>
  <text x="430" y="200" text-anchor="middle" font-size="11.5" fill="{GREEN}" font-weight="700">Reinvest profit &rarr; more designs &rarr; more daily lottery tickets</text>
</svg>'''

def svg_architecture():
    def b(x,y,w,h,t,s,fill="#fff",stroke=LINE,tc=TEXT):
        return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="11" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
        <text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" font-size="13.5" font-weight="700" fill="{tc}">{t}</text>
        <text x="{x+w/2}" y="{y+h/2+15}" text-anchor="middle" font-size="11" fill="{MUTE if tc==TEXT else '#C7D0E0'}">{s}</text>'''
    A = lambda x1,y1,x2,y2,c=FLAME: f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="2.2" marker-end="url(#ar2)"/>'
    return f'''
<svg viewBox="0 0 920 430" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ar2" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 0 L9 4.5 L0 9 z" fill="{FLAME}"/></marker>
    <marker id="ar3" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 0 L9 4.5 L0 9 z" fill="{TEAL}"/></marker></defs>

  <!-- top rail: traffic -->
  {b(20,18,260,64,"Traffic Engine","TikTok &middot; Pinterest &middot; SEO &middot; Etsy search",SOFT,LINE)}
  {A(150,82,150,128)}

  <!-- middle: storefront -->
  {b(20,130,260,84,"Storefront","Shopify (owned) or Etsy (rented)",NAVY,NAVY,"#fff")}
  {A(280,172,360,172)}

  <!-- design library -->
  {b(360,130,200,84,"Quillmark","brand + design library",FLAME,FLAME,"#fff")}
  {A(560,172,640,172)}

  <!-- POD supplier -->
  {b(640,130,260,84,"POD Supplier","Printify / Printful (auto)",NAVY,NAVY,"#fff")}

  <!-- payments / email / analytics rail -->
  {b(20,250,260,60,"Payments","Shopify Pay &middot; PayPal &middot; cards",SOFT,LINE)}
  {b(330,250,260,60,"Email / CRM","Klaviyo / Shopify Email",SOFT,LINE)}
  {b(640,250,260,60,"Analytics","GA4 &middot; Pinterest &middot; pixel",SOFT,LINE)}
  {A(150,214,150,250)}{A(460,214,460,250)}{A(770,214,770,250)}

  <!-- fulfillment to customer -->
  {b(330,346,260,68,"Customer receives order","printed &amp; shipped under your brand",SOFT,GREEN,TEXT)}
  <path d="M812 214 C 912 250, 912 372, 596 372" fill="none" stroke="{TEAL}" stroke-width="2.2" stroke-dasharray="5 4" marker-end="url(#ar3)"/>
  <text x="612" y="342" font-size="10.5" fill="{TEAL}">auto-fulfilled &rarr; ships to customer</text>
</svg>'''

def svg_funnel():
    rows = [
        ("Reach (impressions)", "30,000 / mo", 100, SOFT, TEXT),
        ("Profile / link clicks", "3,000 (10%)", 80, "#FCE9DF", TEXT),
        ("Store visits", "1,650 (55%)", 62, "#F8C9AE", TEXT),
        ("Add to cart", "165 (10%)", 42, FLAME2, "#fff"),
        ("Orders", "33 (2% of visits)", 26, FLAME, "#fff"),
    ]
    out = ['<svg viewBox="0 0 620 300" width="100%" xmlns="http://www.w3.org/2000/svg">']
    y = 14
    cx = 310
    for label, val, wpct, fill, tc in rows:
        w = 540 * wpct/100
        x = cx - w/2
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="42" rx="6" fill="{fill}" stroke="{LINE}" stroke-width="1"/>')
        out.append(f'<text x="{cx}" y="{y+26}" text-anchor="middle" font-size="13" font-weight="700" fill="{tc}">{label} &mdash; {val}</text>')
        y += 56
    out.append(f'<text x="{cx}" y="296" text-anchor="middle" font-size="11.5" fill="{MUTE}">Example math for the $1,000/mo rung at ~$30 AOV. Improve any band and the whole funnel lifts.</text>')
    out.append('</svg>')
    return "".join(out)

def svg_money_split():
    # where a $30 order goes
    segs = [("Product + shipping", 13, NAVY),
            ("Platform + payment fees", 3, GOLD),
            ("Ad / content cost", 4, TEAL),
            ("Your profit", 10, GREEN)]
    total = sum(s[1] for s in segs)
    out = ['<svg viewBox="0 0 620 150" width="100%" xmlns="http://www.w3.org/2000/svg">']
    x = 20; barw = 580
    for label, val, color in segs:
        w = barw * val/total
        out.append(f'<rect x="{x:.1f}" y="30" width="{w:.1f}" height="48" fill="{color}"/>')
        out.append(f'<text x="{x+w/2:.1f}" y="60" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">${val}</text>')
        x += w
    # legend
    lx = 20; ly = 104
    for label, val, color in segs:
        out.append(f'<rect x="{lx}" y="{ly-10}" width="13" height="13" rx="3" fill="{color}"/>')
        out.append(f'<text x="{lx+19}" y="{ly}" font-size="11.5" fill="{TEXT}">{label}</text>')
        lx += 150
    out.append(f'<text x="20" y="22" font-size="12" fill="{MUTE}">Anatomy of one $30 order (illustrative blended product)</text>')
    out.append('</svg>')
    return "".join(out)

def svg_ladder():
    rungs = [
        ("First $1", "proof", 14),
        ("$1/day\n~$30/mo", "1 order/mo", 26),
        ("$100/mo", "3-4 orders", 40),
        ("$5/day\n~$150/mo", "5 orders", 54),
        ("$10/day\n~$300/mo", "10 orders", 70),
        ("$1,000/mo", "~33 orders", 110),
        ("$5,000/mo", "~167 orders", 165),
    ]
    out = ['<svg viewBox="0 0 920 250" width="100%" xmlns="http://www.w3.org/2000/svg">']
    n = len(rungs); bw = 112; gap = 16; x = 20; base = 210
    for i,(label, sub, h) in enumerate(rungs):
        col = FLAME if i>=5 else (FLAME2 if i>=3 else NAVY if i>=1 else "#9AA6BC")
        y = base - h
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="7" fill="{col}"/>')
        lines = label.split("\n")
        ty = y - 10 - (len(lines)-1)*13
        for ln in lines:
            out.append(f'<text x="{x+bw/2}" y="{ty}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{TEXT}">{ln}</text>')
            ty += 14
        out.append(f'<text x="{x+bw/2}" y="{base+18}" text-anchor="middle" font-size="10.5" fill="{MUTE}">{sub}</text>')
        x += bw + gap
    out.append(f'<line x1="20" y1="{base}" x2="900" y2="{base}" stroke="{LINE}" stroke-width="1.5"/>')
    out.append(f'<text x="20" y="244" font-size="11" fill="{FAINT}">Each rung = the same machine, more designs &amp; traffic. Bar height = monthly revenue (not to exact scale).</text>')
    out.append('</svg>')
    return "".join(out)

def svg_timeline():
    phases = [("WEEK 1","Build","Brand, store, 25 listings, payments live",FLAME),
              ("WEEK 2-6","First sales","Daily content, hit first 10 sales, gather reviews",FLAME2),
              ("MONTH 2-3","Traction","Scale to 100+ listings, ~$300-1k/mo, start email",GOLD),
              ("MONTH 4-12","Scale","Best-sellers + paid ads + VA, push toward $5k/mo",GREEN)]
    out = ['<svg viewBox="0 0 920 150" width="100%" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<line x1="40" y1="40" x2="880" y2="40" stroke="{LINE}" stroke-width="3"/>')
    x = 70
    for tag,title,desc,color in phases:
        out.append(f'<circle cx="{x}" cy="40" r="9" fill="{color}"/>')
        out.append(f'<text x="{x}" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="{color}">{tag}</text>')
        out.append(f'<text x="{x}" y="74" text-anchor="middle" font-size="13" font-weight="700" fill="{TEXT}">{title}</text>')
        # wrap desc
        words = desc.split(); line=""; ly=92
        for w in words:
            if len(line)+len(w) > 26:
                out.append(f'<text x="{x}" y="{ly}" text-anchor="middle" font-size="10.3" fill="{MUTE}">{line}</text>'); line=w; ly+=13
            else:
                line = (line+" "+w).strip()
        out.append(f'<text x="{x}" y="{ly}" text-anchor="middle" font-size="10.3" fill="{MUTE}">{line}</text>')
        x += 270
    out.append('</svg>')
    return "".join(out)

# ----------------------------------------------------------------------------
# Small HTML helpers
# ----------------------------------------------------------------------------
def table(headers, rows, cls="", widths=None):
    colg = ""
    if widths:
        colg = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    h = "".join(f"<th>{c}</th>" for c in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return f'<table class="{cls}">{colg}<thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'

def callout(title, body, kind="note"):
    return f'<div class="callout {kind}"><div class="ct">{title}</div><div class="cb">{body}</div></div>'

def kpi(label, value, sub=""):
    return f'<div class="kpi"><div class="kv">{value}</div><div class="kl">{label}</div><div class="ks">{sub}</div></div>'

# ----------------------------------------------------------------------------
# CSS
# ----------------------------------------------------------------------------
CSS = f"""
@page {{
  size: Letter;
  margin: 20mm 16mm 18mm 16mm;
  @bottom-left  {{ content: "Quillmark POD  ·  The Built-In Package"; font-size: 8pt; color: {FAINT}; }}
  @bottom-center{{ content: "BNBHubs · Confidential"; font-size: 8pt; color: {FAINT}; }}
  @bottom-right {{ content: counter(page) " / " counter(pages); font-size: 8pt; color: {FAINT}; }}
}}
@page cover {{ margin: 0; @bottom-left{{content:none}} @bottom-center{{content:none}} @bottom-right{{content:none}} }}
@page divider {{ margin: 0; @bottom-left{{content:none}} @bottom-center{{content:none}} @bottom-right{{content:none}} }}

* {{ box-sizing: border-box; }}
html {{ -weasy-hyphens: auto; }}
body {{ font-family: "Liberation Sans","DejaVu Sans",Arial,sans-serif; color: {TEXT};
  font-size: 10.4pt; line-height: 1.5; margin: 0; }}

h1,h2,h3,h4 {{ font-family: "Liberation Sans","DejaVu Sans",Arial,sans-serif; color: {INK}; line-height: 1.2; }}
h2.section {{ font-size: 19pt; margin: 0 0 2pt 0; }}
h3 {{ font-size: 13pt; margin: 16pt 0 5pt; color: {INK}; }}
h4 {{ font-size: 11pt; margin: 12pt 0 3pt; color: {NAVY}; }}
p  {{ margin: 5pt 0; }}
ul,ol {{ margin: 5pt 0 5pt 0; padding-left: 17pt; }}
li {{ margin: 2.5pt 0; }}
strong {{ color: {INK}; }}
a {{ color: {FLAME}; text-decoration: none; }}
.small {{ font-size: 9pt; color: {MUTE}; }}
.mute {{ color: {MUTE}; }}
.flame {{ color: {FLAME}; }}

.page-break {{ break-before: page; }}
.avoid-break {{ break-inside: avoid; }}

/* ---------- COVER ---------- */
.cover {{ page: cover; break-after: page; height: 278mm;
  background: {INK}; color: #fff; padding: 30mm 22mm; position: relative; overflow: hidden; }}
.cover .eyebrow {{ letter-spacing: 3px; font-size: 10pt; color: {FLAME}; text-transform: uppercase; font-weight:700; }}
.cover h1 {{ color:#fff; font-size: 44pt; margin: 8mm 0 3mm; letter-spacing: -0.5px; }}
.cover .tag {{ font-size: 15pt; color: #C7D0E0; max-width: 150mm; line-height:1.35; }}
.cover .rule {{ height: 3px; width: 56mm; background: {FLAME}; margin: 9mm 0; }}
.cover .meta {{ position: absolute; bottom: 26mm; left: 22mm; right: 22mm; font-size: 10.5pt; color: #93A0B6; }}
.cover .meta b {{ color:#fff; }}
.cover .badge {{ display:inline-block; border:1px solid #2C3850; border-radius:30px; padding:5px 13px; font-size:9pt; color:#C7D0E0; margin-right:7px; }}
.brandrow {{ display:flex; align-items:center; gap:14px; }}
.brandrow .bn {{ font-size:22pt; font-weight:800; color:#fff; letter-spacing:-0.3px; }}

/* ---------- DIVIDERS ---------- */
.divider {{ page: divider; break-before: page; break-after: page; height:278mm;
  background: {NAVY}; color:#fff; padding: 60mm 22mm; overflow: hidden; }}
.divider .n {{ font-size: 12pt; color: {FLAME}; font-weight:700; letter-spacing:2px; }}
.divider h2 {{ color:#fff; font-size: 30pt; margin: 4mm 0 6mm; }}
.divider p {{ color:#AEB8CC; font-size: 12pt; max-width: 150mm; }}
.divider .rule {{ height:3px; width:48mm; background:{FLAME}; margin: 7mm 0; }}

/* ---------- generic ---------- */
.lead {{ font-size: 11.4pt; color: {NAVY}; }}
hr.sep {{ border:0; border-top:1px solid {LINE}; margin: 12pt 0; }}

table {{ border-collapse: collapse; width: 100%; margin: 7pt 0; font-size: 9.4pt; }}
th {{ background: {INK}; color:#fff; text-align:left; padding: 6pt 8pt; font-weight:700; font-size:9pt; }}
td {{ padding: 5.5pt 8pt; border-bottom: 1px solid {LINE}; vertical-align: top; }}
tbody tr:nth-child(even) td {{ background: {SOFT}; }}
table.tight td, table.tight th {{ padding: 4pt 7pt; }}
.tg td:first-child {{ font-weight:700; color:{INK}; }}

.callout {{ border-radius: 10px; padding: 10pt 13pt; margin: 9pt 0; break-inside: avoid; }}
.callout .ct {{ font-weight: 800; margin-bottom: 3pt; font-size:10.2pt; }}
.callout .cb {{ font-size: 9.8pt; }}
.callout.note {{ background: {SOFT}; border-left: 4px solid {NAVY}; }}
.callout.note .ct {{ color: {NAVY}; }}
.callout.flame {{ background: #FDEDE5; border-left: 4px solid {FLAME}; }}
.callout.flame .ct {{ color: {FLAME}; }}
.callout.win {{ background: #E8F6EF; border-left: 4px solid {GREEN}; }}
.callout.win .ct {{ color: {GREEN}; }}
.callout.warn {{ background: #FBF3E2; border-left: 4px solid {GOLD}; }}
.callout.warn .ct {{ color: #B9821F; }}

.kpis {{ display:flex; gap: 9pt; margin: 9pt 0; }}
.kpi {{ flex:1; background:#fff; border:1px solid {LINE}; border-top:3px solid {FLAME}; border-radius:9px; padding:9pt 10pt; }}
.kpi .kv {{ font-size: 18pt; font-weight:800; color:{INK}; line-height:1; }}
.kpi .kl {{ font-size: 9pt; color:{NAVY}; font-weight:700; margin-top:4pt; }}
.kpi .ks {{ font-size: 8.2pt; color:{MUTE}; }}

.diagram {{ border:1px solid {LINE}; border-radius:12px; padding:12pt; margin:10pt 0; background:#fff; break-inside: avoid; }}
.diagram .cap {{ font-size: 8.6pt; color:{MUTE}; margin-top:5pt; text-align:center; }}

.cols2 {{ display:flex; gap: 16pt; }}
.cols2 > div {{ flex:1; }}

.toc {{ font-size: 10.6pt; }}
.toc .row {{ display:flex; justify-content:space-between; border-bottom:1px dotted {LINE}; padding:5.5pt 0; }}
.toc .row b {{ color:{INK}; }}
.toc .row .pg {{ color:{FLAME}; font-weight:700; }}
.toc .grp {{ color:{FLAME}; font-weight:800; font-size:9pt; letter-spacing:1.5px; text-transform:uppercase; margin:11pt 0 2pt; }}

.tagchip {{ display:inline-block; background:{SOFT}; border:1px solid {LINE}; border-radius:20px;
  padding:3px 10px; font-size:8.6pt; color:{NAVY}; margin:2px 3px 2px 0; }}

.checkbox {{ list-style:none; padding-left:0; }}
.checkbox li {{ padding-left: 20pt; position: relative; }}
.checkbox li:before {{ content:"\\2610"; position:absolute; left:0; color:{FLAME}; font-size:12pt; top:-1pt;}}

.daygrid td {{ font-size:8.7pt; }}
.daygrid td:first-child {{ font-weight:800; color:{FLAME}; text-align:center; width:34px; }}
"""

# ----------------------------------------------------------------------------
# Build HTML
# ----------------------------------------------------------------------------
H = []
def add(x): H.append(x)

# ---------- COVER ----------
add(f'''
<div class="cover">
  <div class="brandrow">{nib(58)}<span class="bn">Quillmark</span></div>
  <div class="eyebrow" style="margin-top:14mm">Print-on-demand · Zero inventory · You sell the design</div>
  <h1>The Built-In<br>Package</h1>
  <div class="rule"></div>
  <div class="tag">The complete operating playbook for launching and running a design-led
  print-on-demand brand &mdash; architecture, funnel, feasibility, and a 30-day launch &mdash;
  built to run in 30&ndash;45 minutes a day alongside your other ventures.</div>
  <div style="margin-top:9mm">
    <span class="badge">Architecture</span><span class="badge">Sales Funnel</span>
    <span class="badge">Feasibility Study</span><span class="badge">30-Day Plan</span>
    <span class="badge">Operating System</span>
  </div>
  <div class="meta">
    Prepared for <b>the Founder &amp; Board</b> &nbsp;·&nbsp; A <b>BNBHubs</b> venture &nbsp;·&nbsp; {DATE}<br>
    <span style="font-size:9pt">Confidential strategy document. Projections are planning assumptions, not guarantees.</span>
  </div>
</div>''')

# ---------- HOW TO USE + ASSUMPTIONS ----------
add(f'''
<h2 class="section">How to read this in 25 minutes</h2>
<p class="lead">This booklet is your whole business in one file. Read it top to bottom once
(about a 25-minute walk-through) and you will understand exactly what Quillmark is, how the
money is made, what it costs to start, and what to do Monday morning.</p>
<div class="kpis">
  {kpi("§1–2","Know it","The 10,000-ft view + the model — 6 min")}
  {kpi("§3–4","Build it","Architecture + the funnel — 6 min")}
  {kpi("§5","Fund it","Feasibility + the revenue ladder — 7 min")}
  {kpi("§6–9","Run it","Scaling, 30-day content, operating system — 6 min")}
</div>
<p>Every section ends with something you can act on. The boxes in
<span class="flame">orange</span> are the highest-leverage moves; the
<span style="color:{GOLD}">amber</span> boxes are the risks to respect.</p>

{callout("Working assumption (correct me anytime)",
"This package was rebuilt from the Quillmark brand kit and the three source documents you "
"already have (the <b>Income Structure</b>, the <b>1&ndash;5 Year Board Plan</b>, and the "
"<b>Founder &amp; Operator Manual</b>). It treats Quillmark as a <b>design-led print-on-demand "
"brand</b> &mdash; your original designs printed on apparel, drinkware, wall art and accessories, "
"with zero inventory. If the originals used different numbers, re-share them (or re-authorize the "
"Google&nbsp;Drive connection) and I will reconcile this to the exact figures.", "flame")}

{callout("It runs on a Chromebook",
"Every tool in this plan is browser-based. No warehouse, no stock, no special hardware. "
"A Chromebook, a phone for content, and 30&ndash;45 focused minutes a day is the entire footprint. "
"That is the point of the &lsquo;built-in package&rsquo; &mdash; it is designed for a founder "
"running more than one business at once.", "note")}
''')

# ---------- TOC ----------
def toc_row(t, pg): return f'<div class="row"><b>{t}</b><span class="pg">{pg}</span></div>'
add(f'''
<div class="page-break"></div>
<h2 class="section">Contents</h2>
<div class="toc">
  <div class="grp">Know it</div>
  {toc_row("1 · The 10,000-Foot View","04")}
  {toc_row("2 · The Business Model &amp; Unit Economics","06")}
  <div class="grp">Build it</div>
  {toc_row("3 · The Architecture — how it is built","09")}
  {toc_row("4 · The Funnel — how the money flows","12")}
  <div class="grp">Fund it</div>
  {toc_row("5 · Feasibility Study &amp; the Revenue Ladder","15")}
  <div class="grp">Run it</div>
  {toc_row("6 · Go-To-Market &amp; Scaling (who to reach out to)","20")}
  {toc_row("7 · The 30-Day Content Plan","24")}
  {toc_row("8 · The Built-In Package — your operating system","27")}
  {toc_row("9 · The First 90 Days &amp; Next Actions","31")}
  <div class="grp">Reference</div>
  {toc_row("Appendix A · Tool &amp; cost reference","33")}
  {toc_row("Appendix B · Glossary &amp; one-page cheat sheet","34")}
</div>
''')

# ============================ SECTION 1 ============================
add(f'''
<div class="divider"><div class="n">SECTION 1</div><h2>The 10,000-Foot View</h2>
<div class="rule"></div><p>What Quillmark is, why it can win, and the numbers that matter &mdash; on two pages.</p></div>

<h2 class="section">1 · The 10,000-Foot View</h2>
<p class="lead">Quillmark is a print-on-demand brand: we publish <strong>original designs</strong> and
sell them printed on physical products &mdash; t-shirts, hoodies, mugs, tote bags, posters, phone
cases. We hold <strong>zero inventory</strong>. When a customer buys, a print partner
(Printify or Printful) makes the item on demand and ships it directly to them under the Quillmark
name. We keep the margin between the retail price and the print cost.</p>

<div class="diagram avoid-break">{svg_money_machine()}
<div class="cap">Figure 1 — The Quillmark money machine. One design becomes dozens of sellable products; the printer carries the cost and the labor.</div></div>

<h3>Why this is the right venture to add now</h3>
<ul>
<li><strong>Near-zero downside.</strong> You can launch on Etsy for the price of a few coffees and never hold stock. The risk is time, not capital.</li>
<li><strong>It compounds.</strong> Every design is a permanent, 24/7 sales asset. Designs do not expire. A catalog of 150 listings is 150 lottery tickets working while you sleep on the other businesses.</li>
<li><strong>It fits a multi-business operator.</strong> The work is batchable and delegatable: design in bulk, schedule content, let automation fulfill. This is why it is a &ldquo;built-in package,&rdquo; not a second job.</li>
<li><strong>It rides existing skills.</strong> You already run BNBHubs ventures and have a content/PDF engine (NicheQuill). Quillmark reuses the same muscles: pick a niche, make an asset, drive attention, convert.</li>
</ul>

{callout("The one-sentence model",
"Make a design once &rarr; list it on many products &rarr; drive cheap attention from short-form video and Pinterest &rarr; the printer fulfills every order automatically &rarr; you keep <b>$8&ndash;$12 profit per item</b> and reinvest it into more designs.","flame")}

<h3>The numbers at a glance</h3>
<div class="kpis">
  {kpi("$15–$150","to start","Etsy lean vs. Shopify standard")}
  {kpi("~35%","net margin","after print, fees &amp; ad cost")}
  {kpi("~$10","profit / item","on a typical $26–$30 product")}
  {kpi("5–6 mo","to ~$1k/mo","base-case, consistent effort")}
</div>

<div class="cols2">
<div>
<h4>The three reasons it wins</h4>
<ol>
<li><strong>Asset leverage</strong> — designs are evergreen and stack.</li>
<li><strong>Distribution is free to start</strong> — organic short-form + Pinterest + marketplace search.</li>
<li><strong>Automated fulfillment</strong> — the hardest, most expensive part (making and shipping) is outsourced per order.</li>
</ol>
</div>
<div>
<h4>The honest risks (respected in §8)</h4>
<ol>
<li><strong>Saturation</strong> — generic designs lose; niche + point of view wins.</li>
<li><strong>IP / trademark</strong> — never use protected names, logos or art.</li>
<li><strong>Platform dependence</strong> — own an email list so you are never one ban away from zero.</li>
</ol>
</div>
</div>

{callout("Board-level take","Quillmark is a low-capital, high-asset, automatable income stream that diversifies BNBHubs without competing for the same hours as the core businesses. Recommendation: fund the lean launch, commit to a 90-day content sprint, and judge it on the leading indicators in §8 &mdash; not on week-one revenue.","win")}
''')

# ============================ SECTION 2 ============================
add(f'''
<div class="divider"><div class="n">SECTION 2</div><h2>The Business Model &amp; Unit Economics</h2>
<div class="rule"></div><p>What we sell, how each sale breaks down, and the product ladder that lifts the average order.</p></div>

<h2 class="section">2 · The Business Model &amp; Unit Economics</h2>

<h3>What Quillmark actually sells</h3>
<p>We do not sell &ldquo;t-shirts.&rdquo; We sell <strong>a point of view, printed on whatever the
buyer wants to wear or display.</strong> The product is the design + the identity it signals. That
distinction is the entire moat: anyone can print a blank shirt; the buyer pays for the idea on it.</p>

<p>One design is published across a <strong>product matrix</strong> so a single creative effort earns
many ways:</p>
{table(["Tier","Product","Typical retail","Print cost (approx)","Gross / item"],
[["Entry","Sticker / mug","$6 – $16","$2 – $6","$4 – $10"],
 ["Core","Unisex tee","$24 – $29","$9 – $12","$10 – $14"],
 ["Core","Tote / phone case","$22 – $28","$10 – $13","$9 – $13"],
 ["Premium","Hoodie / sweatshirt","$42 – $55","$22 – $30","$15 – $22"],
 ["Premium","Framed / large poster","$28 – $60","$10 – $24","$14 – $30"]],
 "tg", ["12%","26%","20%","20%","22%"])}
<p class="small">Figures are representative blended ranges across Printify/Printful catalogs; confirm live costs for the exact blanks you choose.</p>

<h3>Anatomy of one order</h3>
<div class="diagram avoid-break">{svg_money_split()}
<div class="cap">Figure 2 — Where a single $30 order goes. Roughly a third is yours to keep, before you scale ad spend.</div></div>

<p>The four levers you control: <strong>(1)</strong> retail price, <strong>(2)</strong> print cost
(choose competitive blanks), <strong>(3)</strong> fees (Etsy vs. Shopify), and <strong>(4)</strong>
ad/content cost (free organic reach keeps this near zero early on).</p>

<h3>Niche strategy — pick a fight you can win</h3>
<p>Broad &ldquo;funny shirt&rdquo; stores drown. Quillmark wins by owning <strong>specific identities
and micro-communities</strong> where buyers are emotional and underserved. Start with 3&ndash;5
niches, double down on whatever sells:</p>
<div>
<span class="tagchip">Hobby pride (e.g. crochet, disc golf, beekeeping)</span>
<span class="tagchip">Profession humor (nurses, teachers, devs, trades)</span>
<span class="tagchip">Pet-parent / breed-specific</span>
<span class="tagchip">Faith &amp; affirmations</span>
<span class="tagchip">Life-stage &amp; family (new mom, retirement, big sis)</span>
<span class="tagchip">Local pride &amp; events</span>
<span class="tagchip">Gifting occasions (anniversary, birthday no.)</span>
<span class="tagchip">Fandom-adjacent (legal, original art only)</span>
</div>

{callout("The reuse advantage with NicheQuill",
"You already produce relationship &amp; self-help content under NicheQuill. Those themes "
"(&lsquo;couples who budget together,&rsquo; &lsquo;step-parent pride,&rsquo; &lsquo;healing era&rsquo;) "
"translate straight into wearable designs and affirmation wall-art. Quillmark can monetize the same "
"audience insight in a second format &mdash; physical product instead of PDF.","flame")}

<h3>Brand &amp; positioning</h3>
<p>Quillmark sits under the <strong>BNBHubs</strong> umbrella as the physical-product arm. The
brand promise is in the tagline already on your kit: <strong>&ldquo;Original designs, on
everything.&rdquo;</strong> The nib mark signals authorship &mdash; these are <em>made</em>, not
scraped. Keep the look consistent: the flame-orange nib, near-black packaging inserts, a clean
modern voice. Consistency is what turns a pile of listings into a brand people follow.</p>

<h4>The product ladder (raises average order value)</h4>
{table(["Stage","Offer","Purpose"],
[["Hook","$6–$16 sticker / mug","Low-risk first purchase; turns a follower into a buyer"],
 ["Core","$24–$29 tee","The profit engine; most volume lives here"],
 ["Bump","&ldquo;Add the matching mug for $9&rdquo;","Lifts AOV at checkout with one click"],
 ["Premium","$45 hoodie / framed print","Higher margin for your biggest fans"],
 ["Bundle","&ldquo;Set of 3, save 15%&rdquo;","Increases units per order; clears your best designs"]],
 "tg",["14%","40%","46%"])}
''')

# ============================ SECTION 3 ============================
add(f'''
<div class="divider"><div class="n">SECTION 3</div><h2>The Architecture</h2>
<div class="rule"></div><p>Exactly how the machine is wired &mdash; the same build method behind your other ventures, applied to product.</p></div>

<h2 class="section">3 · The Architecture — how it is built</h2>
<p class="lead">Everything is browser-based and connected so that an order placed at 3&nbsp;a.m. is
designed, charged, printed and shipped without you touching it. Here is the full wiring.</p>

<div class="diagram avoid-break">{svg_architecture()}
<div class="cap">Figure 3 — Quillmark system architecture. Traffic feeds the storefront; the storefront passes paid orders to the POD supplier; the supplier prints and ships. You own the brand, designs, list and audience.</div></div>

<h3>The two ways to run the storefront</h3>
{table(["","Etsy (rented audience)","Shopify (owned storefront)"],
[["Best for","Day-one validation, built-in buyers","Brand, margins, scale, your data"],
 ["Cost","$0.20 / listing + ~6.5% + payment fees","$39/mo + 2.9% + $0.30 / order"],
 ["Traffic","Etsy search sends free buyers","You must bring the traffic"],
 ["Upside","Fast first sales, low effort","Higher margin, email list, no ban-risk to catalog"],
 ["Risk","Fees stack; you don&rsquo;t own the customer","Slower start; needs marketing from day one"]],
 "tg",["18%","41%","41%"])}
{callout("Recommended path","Start on <b>Etsy</b> to prove which designs sell with real buyers (cheap, fast feedback). The moment a handful of designs get traction, stand up the <b>Shopify</b> store and run both &mdash; Etsy for discovery, Shopify for margin and for the email list you actually own.","flame")}

<h3>The full stack (every tool, what it does, what it costs)</h3>
{table(["Layer","Tool (pick one)","Job","Cost to start"],
[["Storefront","Etsy &nbsp;/&nbsp; Shopify Basic","Where customers buy","$0 / $39 mo"],
 ["POD &amp; fulfillment","Printify &nbsp;/&nbsp; Printful","Prints &amp; ships each order","$0 (pay per order)"],
 ["Design","Canva Pro + AI image tools","Create the artwork &amp; mockups","$0–$13 mo"],
 ["Brand assets","Your Quillmark kit (nib, banner)","Consistent identity","Owned"],
 ["Email / CRM","Shopify Email / Klaviyo","Repeat sales, abandoned cart","$0 to start"],
 ["Content","CapCut + phone","Short-form video for reach","$0"],
 ["Scheduling","Buffer / Metricool / native","Batch &amp; auto-post","$0–$15 mo"],
 ["Analytics","GA4 + Pinterest + platform pixel","See what converts","$0"],
 ["Payments","Shopify Payments / PayPal","Take money","% per sale"],
 ["Domain","quillmark.&lt;tld&gt;","Trust &amp; email","~$12 / yr"]],
 "tg",["20%","30%","32%","18%"])}

<h3>The design pipeline (idea &rarr; live listing)</h3>
<ol>
<li><strong>Pick the niche &amp; the feeling</strong> — who is this for and what do they want to signal?</li>
<li><strong>Generate the concept</strong> — text-led designs (typography + a clever line) and AI/vector art. Keep it original; never copy protected work.</li>
<li><strong>Compose in Canva</strong> at print resolution (300 DPI; transparent PNG for apparel).</li>
<li><strong>Push to the POD supplier</strong> — place the art on the product matrix, auto-generate mockups.</li>
<li><strong>Publish with SEO</strong> — keyword-rich title, tags, description (see listing SOP in §8).</li>
<li><strong>Syndicate</strong> — the mockup becomes Pinterest pins and a short video. One design = one design job + many marketing assets.</li>
</ol>

<h3>What happens automatically when an order comes in</h3>
{table(["Step","Who does it","You?"],
[["Customer pays","Storefront + payment processor","No"],
 ["Order routed to printer","Auto-sync (Printify/Printful app)","No"],
 ["Item printed","Print partner","No"],
 ["Shipped + tracking sent","Print partner &rarr; customer","No"],
 ["Post-purchase email + review ask","Email automation","Set once"],
 ["Customer service / refunds","You (templates in §8)","~5 min as needed"]],
 "tg",["34%","44%","22%"])}

{callout("Day-1 build checklist","Domain bought · Quillmark logo + banner loaded · Etsy (or Shopify) store live · POD app connected &amp; a test order placed to yourself · payments verified · 5 listings published. That is a launchable store in an afternoon.","note")}
''')

# ============================ SECTION 4 ============================
add(f'''
<div class="divider"><div class="n">SECTION 4</div><h2>The Funnel</h2>
<div class="rule"></div><p>How a stranger scrolling a video becomes a paying customer &mdash; and then a repeat one.</p></div>

<h2 class="section">4 · The Funnel — how the money flows</h2>
<p class="lead">Sales are not luck; they are a funnel. Each stage has a number you can improve.
Quillmark&rsquo;s funnel is built so that <strong>free attention</strong> at the top can carry the
whole thing until you choose to add paid fuel.</p>

<div class="diagram avoid-break">{svg_funnel()}
<div class="cap">Figure 4 — The conversion funnel with example math for the $1,000/mo rung. Lift any single band and everything below it rises.</div></div>

<h3>Top of funnel — where attention comes from</h3>
{table(["Channel","Why it works for POD","Cost","Speed"],
[["TikTok / Reels / Shorts","Designs are visual; a single video can reach thousands free","Free","Fast, spiky"],
 ["Pinterest","Buyers search with intent; pins sell for years","Free","Slow build, compounding"],
 ["Etsy search","Built-in shoppers already looking to buy","Listing fee","Medium"],
 ["SEO / blog","&lsquo;Best gifts for X&rsquo; round-ups send buyers","Time","Slow, durable"],
 ["Paid (Meta / Pinterest / Etsy Ads)","Pour fuel on proven winners","$5–$20/day","Instant, costs money"]],
 "tg",["26%","40%","16%","18%"])}

<h3>Middle — turning a visit into a sale</h3>
<ul>
<li><strong>The listing is the salesperson.</strong> First photo = scroll-stopping mockup on a clean or lifestyle background. Title and first line answer &ldquo;is this for me?&rdquo; in two seconds.</li>
<li><strong>Proof.</strong> Reviews and &ldquo;X sold&rdquo; do the convincing. Your first job after launch is harvesting reviews (a polite post-purchase ask + a tiny incentive).</li>
<li><strong>Friction kills.</strong> Clear sizing, shipping time stated up front, easy returns policy. Every unanswered question is a lost sale.</li>
<li><strong>Gentle urgency.</strong> Seasonal/limited drops and &ldquo;order by X for delivery by Y&rdquo; convert browsers now instead of &ldquo;later&rdquo; (which never comes).</li>
</ul>

<h3>Raising the average order value (AOV)</h3>
{table(["Tactic","Mechanism","Typical lift"],
[["Order bump","&ldquo;Add matching mug for $9&rdquo; at checkout","+10–20% AOV"],
 ["Volume discount","&ldquo;Buy 2, save 10%&rdquo;","+units per order"],
 ["Curated bundle","Themed set of 3 at a set price","+AOV &amp; clears winners"],
 ["Free-shipping threshold","&ldquo;Free shipping over $35&rdquo;","Nudges a second item"]],
 "tg",["26%","48%","26%"])}

<h3>Bottom &amp; beyond — retention is the real profit</h3>
<p>The first sale often just covers acquisition. The <strong>profit is in the second and third
order</strong>, where you pay nothing to reacquire the customer.</p>
<ul>
<li><strong>Capture the email</strong> at checkout and via a small welcome offer.</li>
<li><strong>Automate three emails:</strong> welcome + first-order nudge, abandoned-cart recovery, post-purchase review ask &amp; cross-sell.</li>
<li><strong>Seasonal re-engagement:</strong> new-drop announcements to past buyers convert far above cold traffic.</li>
</ul>

{callout("Funnel rule of thumb","If sales are slow, diagnose top-down: <b>No reach?</b> &rarr; post more / better content. <b>Reach but no clicks?</b> &rarr; fix the thumbnail/hook. <b>Clicks but no sales?</b> &rarr; fix the listing, price, or proof. Always fix the highest leaky band first.","flame")}
''')

# ============================ SECTION 5 ============================
add(f'''
<div class="divider"><div class="n">SECTION 5</div><h2>Feasibility Study &amp; the Revenue Ladder</h2>
<div class="rule"></div><p>What it costs to start, when it pays for itself, and exactly what each income milestone requires.</p></div>

<h2 class="section">5 · Feasibility Study &amp; the Revenue Ladder</h2>

<h3>5.1 — Startup capital required</h3>
<p>Three funding levels. You can genuinely begin at the lean tier and let revenue fund the rest.</p>

<h4>Lean launch — Etsy, organic only</h4>
{table(["Item","Cost"],
[["Etsy listings (25 × $0.20)","$5.00"],
 ["Canva Pro (optional, monthly)","$0–$13"],
 ["Domain (optional early)","$0–$12/yr"],
 ["Sample order (recommended, 1 item)","$15–$25"],
 ["<b>Total to open the doors</b>","<b>$15 – $50</b>"]],"tg",["70%","30%"])}

<h4>Standard launch — Shopify + Etsy</h4>
{table(["Item","Cost"],
[["Shopify Basic (first month)","$39"],
 ["Domain","$12/yr"],
 ["Canva Pro","$13/mo"],
 ["3–4 sample items (quality check)","$60–$90"],
 ["Apps (email, reviews — free tiers)","$0"],
 ["<b>Total month one</b>","<b>~$125 – $155</b>"]],"tg",["70%","30%"])}

<h4>Comfortable launch — adds a paid-ad test</h4>
{table(["Item","Cost"],
[["Everything in Standard","~$150"],
 ["Paid ad test budget (30 days)","$150–$450"],
 ["Premium apps / scheduler","$15–$40/mo"],
 ["Extra samples for content","$60–$120"],
 ["<b>Total month one</b>","<b>~$400 – $750</b>"]],"tg",["70%","30%"])}

{callout("Break-even","On the <b>lean Etsy</b> path fixed costs are near zero, so you are profitable on roughly the <b>first sale</b>. On the <b>Shopify standard</b> path, fixed cost is ~$52/mo (Shopify + Canva), so break-even is about <b>5 orders/month</b> — i.e. the $5/day rung pays for the whole tool stack.","win")}

<h3>5.2 — The Revenue Ladder</h3>
<p class="lead">This is the heart of the study: every income milestone you named, translated into the
<strong>orders, traffic, catalog size and time</strong> it actually takes. Assumptions:
<strong>$30 average order</strong>, <strong>~$10 profit/order</strong> before ads,
<strong>~2% store conversion</strong>.</p>

<div class="diagram avoid-break">{svg_ladder()}
<div class="cap">Figure 5 — The revenue ladder. Same machine at every rung; you are just adding designs and attention.</div></div>

{table(["Rung","Revenue","Orders","Visits / mo needed","Catalog size","Primary engine","Realistic timing*"],
[["Proof","First $1","1 sale","~50","5–10 listings","Organic + share to friends","Week 1–3"],
 ["$1/day","~$30/mo","~1/mo","~50","10–25","Organic content","Month 1"],
 ["$100/mo","~$3.3/day","3–4/mo","~175","25–50","Organic + Etsy search","Month 1–2"],
 ["$5/day","~$150/mo","~5/mo","~250","40–75","Organic, reviews building","Month 2–3"],
 ["$10/day","~$300/mo","~10/mo","~500","60–100","Organic + Pinterest compounding","Month 3–4"],
 ["$1,000/mo","~$33/day","~33/mo","~1,650","100–150","Organic + email + light ads","Month 5–7"],
 ["$5,000/mo","~$166/day","~167/mo","~8,350","150–300+","Winners + paid ads + repeat buyers","Month 9–15"]],
 "tg",["10%","13%","10%","16%","13%","24%","14%"])}
<p class="small">*Timing assumes consistent execution of the §7 content plan. POD is competitive; these are planning targets, not promises. Some niches move faster, some slower.</p>

<h3>5.3 — What changes as you climb</h3>
<div class="cols2">
<div>
<h4>Rungs 1–4 ($1–$10/day)</h4>
<ul>
<li><strong>Engine:</strong> 100% free organic + marketplace search.</li>
<li><strong>Your job:</strong> publish designs, post daily, get the first 10 reviews.</li>
<li><strong>Spend:</strong> ~$0 ads. Reinvest profit into more designs/samples.</li>
<li><strong>Goal:</strong> find 3–5 designs that actually sell. That data is worth more than the revenue.</li>
</ul>
</div>
<div>
<h4>Rungs 5–6 ($1k–$5k/mo)</h4>
<ul>
<li><strong>Engine:</strong> scale winners with paid ads + an email list of past buyers.</li>
<li><strong>Your job:</strong> shift from making everything to <em>doubling down</em> on proven niches; bring in a VA/designer (§8).</li>
<li><strong>Spend:</strong> reinvest 20–40% of profit into ads on proven designs only.</li>
<li><strong>Goal:</strong> repeatable acquisition where every $1 in returns $2+.</li>
</ul>
</div>
</div>

<h3>5.4 — 12-month scenarios</h3>
{table(["Month","Conservative (rev)","Base (rev)","Aggressive (rev)"],
[["1","$0–30","$30–100","$150"],
 ["2","$30","$120","$400"],
 ["3","$75","$300","$800"],
 ["4","$150","$500","$1,400"],
 ["6","$300","$1,000","$2,800"],
 ["9","$600","$2,200","$4,500"],
 ["12","$1,000","$3,500–5,000","$7,000+"]],
 "tg",["16%","28%","28%","28%"])}
<p class="small">Drivers of the spread: number of designs shipped, content consistency, how fast you find winners, and whether/when you add paid ads. Effort &mdash; not luck &mdash; is what moves you from the left column to the right.</p>

<h3>5.5 — The key ratios to watch</h3>
{table(["Metric","What it means","Healthy target"],
[["Gross margin / order","Profit after print + fees","30–45%"],
 ["Conversion rate","Visits that become orders","1.5–3% (Etsy higher)"],
 ["ROAS (if running ads)","Revenue per $1 of ad spend","&ge; 2.0x to scale"],
 ["AOV","Average order value","$30+ (raise with bumps/bundles)"],
 ["Repeat rate","Buyers who buy again","15%+ once email is running"]],
 "tg",["26%","44%","30%"])}

{callout("Feasibility verdict","Financially feasible at low risk. The lean path costs less than a dinner out and is profitable on the first sale. The real investment is the <b>90-day content sprint</b> in §7. If you ship designs and post daily, the base-case ladder ($1k/mo around months 5–7) is realistic; $5k/mo is a function of finding winners and adding paid fuel.","win")}
''')

# ============================ SECTION 6 ============================
add(f'''
<div class="divider"><div class="n">SECTION 6</div><h2>Go-To-Market &amp; Scaling</h2>
<div class="rule"></div><p>The phased roadmap, exactly who to reach out to, and copy-paste outreach you can send today.</p></div>

<h2 class="section">6 · Go-To-Market &amp; Scaling</h2>

<div class="diagram avoid-break">{svg_timeline()}
<div class="cap">Figure 6 — The phased roadmap from empty store to scaling brand.</div></div>

<h3>6.1 — The two growth engines</h3>
<div class="cols2">
<div>
<h4>Organic engine (start here)</h4>
<ul>
<li>Short-form video showing the design + the &ldquo;who it&rsquo;s for&rdquo; moment.</li>
<li>Pinterest pins for every product (compounds for months).</li>
<li>Marketplace SEO (Etsy titles/tags).</li>
<li>Cost: time. Ceiling: high but slower.</li>
</ul>
</div>
<div>
<h4>Paid engine (add after winners appear)</h4>
<ul>
<li>Etsy Ads on proven listings.</li>
<li>Pinterest / Meta ads on your best-converting design.</li>
<li>Only scale spend while ROAS &ge; 2.</li>
<li>Cost: money. Ceiling: very high, fast.</li>
</ul>
</div>
</div>

<h3>6.2 — Who to reach out to (and why)</h3>
<p>Outreach multiplies organic reach. Target people who already hold the attention of your niche:</p>
{table(["Who","Why them","The ask"],
[["Micro-influencers (1k–50k) in your niche","Trusted by exactly your buyer; cheap or free","Gift a product for an honest post / affiliate code"],
 ["Niche meme / fan pages","Massive cheap reach in one community","Paid shout-out or rev-share on a code"],
 ["Pinterest creators &amp; group-board owners","Evergreen, buyer-intent traffic","Collaborate / contribute pins"],
 ["Facebook groups &amp; subreddits for the niche","Concentrated superfans","Participate genuinely; share only where allowed"],
 ["Complementary small brands","Shared audience, not competitors","Cross-promo / bundle collab"],
 ["Local boutiques, gyms, salons, events","Real-world distribution","Wholesale or consignment of best-sellers"],
 ["Affiliates / ambassadors","Sell for you on commission","10–20% per sale via code/link"],
 ["Etsy / gift round-up bloggers","&lsquo;Best gifts for X&rsquo; lists send buyers","Pitch your product for inclusion"]],
 "tg",["28%","40%","32%"])}

<h3>6.3 — Outreach methods &amp; copy-paste templates</h3>
<p>Send 5&ndash;10 personalized messages a day. Personalize the first line; keep it short; make the
ask tiny.</p>

<h4>Micro-influencer gifting DM</h4>
{callout("Template",
"&ldquo;Hi [name] &mdash; I love your [specific post about X]. I run <b>Quillmark</b>, we make original "
"[niche] designs on tees &amp; mugs. I&rsquo;d love to send you a free [product] in your size &mdash; no "
"strings. If you love it and want to share, even better. Can I get it shipped to you?&rdquo;","note")}

<h4>Affiliate / ambassador pitch</h4>
{callout("Template",
"&ldquo;Hey [name], your audience is exactly who our [niche] designs are for. Want to earn <b>15% on every "
"sale</b> with your own code? You share what you already love, we handle printing &amp; shipping, you get "
"paid monthly. I&rsquo;ll set up [CODE] today if you&rsquo;re in.&rdquo;","note")}

<h4>Cross-promo with a complementary brand</h4>
{callout("Template",
"&ldquo;Hi [brand] &mdash; we serve the same [niche] customer but don&rsquo;t compete (you do [X], we do "
"apparel/print). Want to cross-feature each other to our audiences this month, or build a little bundle "
"together? Happy to go first.&rdquo;","note")}

<h4>Wholesale / local stockist email</h4>
{callout("Template",
"&ldquo;Hi [shop] &mdash; your customers are [niche] lovers and so are ours. We&rsquo;d love to stock a small "
"set of our best-selling [niche] designs with you on wholesale or consignment &mdash; no upfront risk to you. "
"Could I drop off 5 samples this week?&rdquo;","note")}

<h3>6.4 — Scaling levers (in order)</h3>
<ol>
<li><strong>More designs</strong> in proven niches &mdash; cheapest growth; more lottery tickets.</li>
<li><strong>More products per winning design</strong> &mdash; squeeze every winner across the matrix.</li>
<li><strong>More channels</strong> &mdash; add Shopify, then Pinterest at scale, then ads.</li>
<li><strong>Email &amp; repeat buyers</strong> &mdash; the cheapest revenue you will ever get.</li>
<li><strong>Paid ads on winners only</strong> &mdash; never advertise an unproven design.</li>
<li><strong>People</strong> &mdash; a VA for listings/CS, then a designer for volume (see §8).</li>
<li><strong>New niches</strong> &mdash; clone the whole playbook into an adjacent audience.</li>
</ol>

{callout("Scaling discipline","Do not add a new lever until the previous one is working. Most POD stores die from doing ten things badly. Quillmark wins by doing the next single highest-leverage thing well, then stacking the next.","flame")}
''')

# ============================ SECTION 7 ============================
add(f'''
<div class="divider"><div class="n">SECTION 7</div><h2>The 30-Day Content Plan</h2>
<div class="rule"></div><p>A day-by-day calendar so &lsquo;market it&rsquo; becomes a checklist, not a mystery.</p></div>

<h2 class="section">7 · The 30-Day Content Plan</h2>
<p class="lead">Content is the free engine that powers rungs 1&ndash;4. The goal of month one is not
perfection &mdash; it is <strong>reps and signal</strong>: post enough to learn what your niche
reacts to, and get your first sales and reviews.</p>

<h3>Content pillars (rotate these)</h3>
<div>
<span class="tagchip">1 · Design reveal (&ldquo;made this for [niche]&rdquo;)</span>
<span class="tagchip">2 · Relatable niche humor / truth</span>
<span class="tagchip">3 · Behind the brand (the nib, the process)</span>
<span class="tagchip">4 · Social proof (reviews, &ldquo;it shipped!&rdquo;)</span>
<span class="tagchip">5 · Gift framing (&ldquo;perfect for the [niche] in your life&rdquo;)</span>
</div>

<h3>Platform focus</h3>
{table(["Platform","Format","Cadence","Job"],
[["TikTok / Reels / Shorts","15–25s vertical video","1/day","Reach &amp; discovery"],
 ["Pinterest","Product pins + idea pins","3–5 pins/day","Evergreen buyer traffic"],
 ["Instagram","Reels + carousel","4–5/wk","Brand + proof"],
 ["Etsy/Shopify","New listings","2–4/wk","The asset that converts"]],
 "tg",["26%","30%","18%","26%"])}

<h3>The 30-day calendar</h3>
<p class="small">Each day = one short video + repurpose to other platforms + the listing/admin task. &ldquo;DR&rdquo;=design reveal, &ldquo;H&rdquo;=humor/relatable, &ldquo;BTS&rdquo;=behind the scenes, &ldquo;SP&rdquo;=social proof, &ldquo;GIFT&rdquo;=gift framing.</p>
''')

# 30-day grid as a table (week rows)
day_rows = [
 ["1","Launch: store live + announce. Post DR of hero design. List 5 products."],
 ["2","H video for niche A. Make 5 Pinterest pins. List 2 products."],
 ["3","DR design #2. Reply to every comment. Set up post-purchase email."],
 ["4","BTS: &lsquo;why Quillmark / the nib&rsquo;. List 2. DM 5 micro-influencers."],
 ["5","GIFT angle for niche A. Schedule weekend posts. List 2."],
 ["6","H video (trend audio). Pin batch. Ask first buyers for reviews."],
 ["7","Week-1 review: which post got most reach? Note the winner."],
 ["8","DR design #3 (lean into week-1 winner). List 3 products."],
 ["9","SP: screenshot any sale/review. H video niche B. Pin batch."],
 ["10","Collab DM day: 5 cross-promo / affiliate pitches. List 2."],
 ["11","GIFT bundle idea video. Set up an order bump at checkout."],
 ["12","DR design #4. Pinterest idea pin. Reply/engage 20 min."],
 ["13","H video remix of best week-1 hook. List 2."],
 ["14","Week-2 review: double down on best niche; cut what flopped."],
 ["15","DR design #5 in winning niche. Launch a small &lsquo;drop&rsquo;."],
 ["16","SP compilation. Pin batch. Email past visitors the new drop."],
 ["17","BTS packaging/branding insert. List 3. DM 5 more creators."],
 ["18","GIFT angle niche B. Trend-jack with your design. Pin batch."],
 ["19","DR design #6. Add a volume discount (&lsquo;buy 2 save 10%&rsquo;)."],
 ["20","H video. Reach out to 1 local stockist / boutique."],
 ["21","Week-3 review: is a design selling? If yes, plan ad test."],
 ["22","DR design #7. Make 3 variations of your best-selling design."],
 ["23","SP + UGC ask (&lsquo;tag us&rsquo;). Pin batch. List 2."],
 ["24","GIFT seasonal angle. Set free-shipping threshold at $35."],
 ["25","BTS &lsquo;30 days in&rsquo; story. Affiliate code for 1 creator who replied."],
 ["26","DR design #8. Repurpose top video to all platforms."],
 ["27","H video. Email list: review request + cross-sell."],
 ["28","Week-4 review: pick THE winner. Draft a $5–$10/day ad test."],
 ["29","Launch small ad test on the winner only. DR design #9."],
 ["30","Month review: revenue, best niche, best design, next-month plan."],
]
rows_html = ""
for d,t in day_rows:
    rows_html += f"<tr><td>{d}</td><td>{t}</td></tr>"
add(f'''<table class="daygrid"><colgroup><col style="width:34px"><col></colgroup>
<thead><tr><th>Day</th><th>Action (1 video · repurpose · 1 store task)</th></tr></thead>
<tbody>{rows_html}</tbody></table>''')

add(f'''
<h3>Hook bank (steal these openers)</h3>
<ul>
<li>&ldquo;If you&rsquo;re a [niche], this one&rsquo;s for you&hellip;&rdquo;</li>
<li>&ldquo;POV: someone finally made a [niche] shirt that isn&rsquo;t cringe.&rdquo;</li>
<li>&ldquo;Tag the [niche] in your life before [holiday].&rdquo;</li>
<li>&ldquo;I made this because every [niche] I know needs it.&rdquo;</li>
<li>&ldquo;Things only a [niche] will understand &mdash; on a mug.&rdquo;</li>
</ul>

{callout("Batch it (the multi-business hack)","Do not create daily. Once a week, in one 90-minute block: design 3–5 pieces, film 7 short videos, and write 7 captions. Schedule them. Now &lsquo;daily content&rsquo; costs you 15 minutes a day of posting + replying. This is what makes Quillmark survivable next to your other ventures.","flame")}
''')

# ============================ SECTION 8 ============================
add(f'''
<div class="divider"><div class="n">SECTION 8</div><h2>The Built-In Package</h2>
<div class="rule"></div><p>Your operating system: the daily routine, the SOPs, the dashboard, automation, hiring and risk &mdash; so it runs without living in your head.</p></div>

<h2 class="section">8 · The Built-In Package — your operating system</h2>
<p class="lead">This is the part that matters most for a founder running several businesses: a
<strong>system you can follow on autopilot</strong> and hand to someone else. If you only operate
the routines below, Quillmark runs in <strong>30&ndash;45 minutes a day</strong>.</p>

<h3>8.1 — The daily 30-minute routine</h3>
<ul class="checkbox">
<li><strong>(5 min)</strong> Check orders &amp; messages; answer any customer using a template.</li>
<li><strong>(10 min)</strong> Post today&rsquo;s pre-made video; pin 3–5 to Pinterest.</li>
<li><strong>(10 min)</strong> Reply to comments/DMs; send 3–5 outreach messages.</li>
<li><strong>(5 min)</strong> Glance at the dashboard: yesterday&rsquo;s sales, reach, any review to action.</li>
</ul>

<h3>8.2 — Weekly &amp; monthly cadence</h3>
<div class="cols2">
<div>
<h4>Weekly (~2 hrs, one block)</h4>
<ul class="checkbox">
<li>Batch: 3–5 designs + 7 videos + captions, scheduled.</li>
<li>Publish 2–4 new listings (SEO&rsquo;d).</li>
<li>Send one email to the list (new drop / tip).</li>
<li>Review numbers; note best &amp; worst performer.</li>
</ul>
</div>
<div>
<h4>Monthly (~1 hr)</h4>
<ul class="checkbox">
<li>Cut dead listings; double down on winners.</li>
<li>Check print costs/margins; adjust prices.</li>
<li>Decide ad spend for next month (winners only).</li>
<li>Plan next month&rsquo;s niches &amp; drops.</li>
</ul>
</div>
</div>

<h3>8.3 — The KPI dashboard (track weekly)</h3>
{table(["Metric","Where","Target trend"],
[["Revenue &amp; orders","Store backend","Up week over week"],
 ["Conversion rate","Store analytics","Toward 2%+"],
 ["Reach / profile clicks","Platform insights","Up; spot winning content"],
 ["New reviews","Store","+ every week early on"],
 ["Email list size","Email tool","Steadily up"],
 ["ROAS (if ads on)","Ads manager","&ge; 2.0x"],
 ["Best design / niche","Your notes","Reallocate effort here"]],
 "tg",["34%","30%","36%"])}

<h3>8.4 — Automation map (set once, runs forever)</h3>
{table(["Trigger","Automation","Tool"],
[["Order placed","Auto-send to printer, print, ship, tracking","POD app"],
 ["Order placed","Post-purchase thank-you + review ask","Email tool"],
 ["Cart abandoned","Recovery email after 1–4 hrs","Email tool"],
 ["New subscriber","Welcome + first-order offer","Email tool"],
 ["Content","Pre-scheduled posts publish themselves","Scheduler"],
 ["New listing","Auto-create Pinterest pin","Native / integration"]],
 "tg",["26%","48%","26%"])}

<h3>8.5 — Standard Operating Procedures (hand these to a VA)</h3>
<h4>Listing SOP</h4>
<ol>
<li>Export 300-DPI PNG from Canva. 2) Upload to POD; place on the product matrix. 3) Generate mockups. 4) Title = &ldquo;[keyword] [product] for [niche] &mdash; [occasion] gift.&rdquo; 5) Fill all 13 Etsy tags with buyer search terms. 6) Description: who it&rsquo;s for, materials, sizing, shipping time, care. 7) Set price from the margin table. 8) Publish &amp; create one pin + one video.</li>
</ol>
<h4>Customer-service templates</h4>
{callout("Shipping question","&ldquo;Thanks for reaching out! Your order is made to order and typically ships in 2–5 business days, with delivery around [date]. Here&rsquo;s your tracking: [link]. Anything else I can help with?&rdquo;","note")}
{callout("Refund / problem","&ldquo;So sorry about that! We stand behind every Quillmark order. I&rsquo;m arranging a free replacement/refund right now &mdash; could you send a photo so we can fix it with our print partner? Thank you for your patience.&rdquo;","note")}

<h3>8.6 — When &amp; who to hire</h3>
{table(["Trigger","Hire","Cost guide","Frees you to"],
[["~$1k/mo &amp; admin eats your time","VA (listings, CS, scheduling)","$4–$8/hr, ~10 hrs/wk","Strategy + content"],
 ["Design is the bottleneck","Freelance designer","Per-design or retainer","Ship more winners"],
 ["~$5k/mo, ads working","Ads/marketing help","% or retainer","Scale spend safely"]],
 "tg",["30%","26%","20%","24%"])}

<h3>8.7 — Risk register &amp; compliance (respect these)</h3>
{table(["Risk","Likelihood","Mitigation"],
[["Trademark / copyright strike","Medium","Original art only; never use brands, logos, lyrics, characters, athlete/celebrity names. When unsure, don&rsquo;t."],
 ["Market saturation","High","Win on specific niche + point of view, not generic designs."],
 ["Platform ban / policy change","Medium","Own a domain + email list; sell on 2 channels; never depend on one."],
 ["Print quality / shipping delays","Medium","Order samples; pick reliable suppliers; state times clearly; fast CS."],
 ["Chargebacks / refunds","Low–Med","Clear policy, sizing, photos; resolve fast; the print partner often covers defects."],
 ["Founder time / burnout","Medium","The batch + automation system above; delegate early."]],
 "tg",["30%","16%","54%"])}

{callout("Compliance one-liner","If a design uses someone else&rsquo;s name, brand, logo, character, photo, or lyric &mdash; do not list it. Original or licensed only. This single rule protects the whole business and the BNBHubs umbrella.","warn")}
''')

# ============================ SECTION 9 ============================
add(f'''
<div class="divider"><div class="n">SECTION 9</div><h2>The First 90 Days &amp; Next Actions</h2>
<div class="rule"></div><p>From this booklet to a live, selling store &mdash; starting Monday morning.</p></div>

<h2 class="section">9 · The First 90 Days &amp; Next Actions</h2>

<h3>The first 7 days</h3>
{table(["Day","Do this"],
[["1","Buy domain. Set up Etsy (and/or Shopify). Load Quillmark logo + banner."],
 ["2","Connect Printify/Printful. Place a test order to yourself. Verify payments."],
 ["3","Create 5 designs in your top niche. Publish 5 listings (use the SOP)."],
 ["4","Set up post-purchase + abandoned-cart emails. Make 15 Pinterest pins."],
 ["5","Film 7 short videos (batch). Write 7 captions. Schedule the week."],
 ["6","Go live: announce the store. Post video 1. Start the §7 calendar."],
 ["7","DM 5 micro-influencers. Rest + review. You now have a running business."]],
 "tg",["10%","90%"])}

<h3>30 / 60 / 90-day milestones</h3>
{table(["By day","Target","Leading indicator that matters more than revenue"],
[["30","First sales + first reviews; 25+ listings","You&rsquo;ve identified your best-reacting niche &amp; design"],
 ["60","~$150–$500/mo; email list started","One design reliably sells &mdash; a proven winner"],
 ["90","~$300–$1,000/mo; first ad test live","Repeatable: content &rarr; traffic &rarr; sales loop works"]],
 "tg",["12%","34%","54%"])}

{callout("Do this Monday morning","Buy the domain, open the Etsy store, and publish ONE design. Perfection is the enemy &mdash; a live store with one listing beats a perfect plan with none. Everything in this booklet builds on that first published product.","flame")}

{callout("Board recommendation","Approve the lean launch (&lt;$50 at risk). Commit to the 90-day content sprint as the real investment. Review at day 30/60/90 against the leading indicators above &mdash; not week-one revenue. Quillmark&rsquo;s value to BNBHubs is a compounding, automatable, low-capital income stream that does not compete for the same hours as the core businesses.","win")}

<div class="page-break"></div>
<h2 class="section">Appendix A · Tool &amp; cost reference</h2>
{table(["Need","Free / cheap option","Paid upgrade","Notes"],
[["Storefront","Etsy ($0.20/listing)","Shopify Basic $39/mo","Run both once validated"],
 ["Printing","Printify (free plan)","Printify Premium / Printful","Compare base cost + quality"],
 ["Design","Canva free","Canva Pro $13/mo","Brand kit, background remover"],
 ["AI art/text","Free tiers","Paid as needed","Original art only"],
 ["Email","Shopify Email / free tier","Klaviyo paid","Automations = repeat sales"],
 ["Video","CapCut free","&mdash;","Phone is enough"],
 ["Scheduling","Native schedulers","Buffer/Metricool $0–15","Enables batching"],
 ["Analytics","GA4, Pinterest, pixels","&mdash;","All free"]],
 "tg",["18%","30%","26%","26%"])}

<h2 class="section" style="margin-top:18pt">Appendix B · Glossary &amp; cheat sheet</h2>
{table(["Term","Means"],
[["POD","Print-on-demand: item is made only after it&rsquo;s ordered. Zero inventory."],
 ["AOV","Average order value &mdash; raise it with bumps &amp; bundles."],
 ["Conversion rate","% of visitors who buy."],
 ["ROAS","Return on ad spend; revenue per $1 of ads."],
 ["Margin","Profit left after print + fees."],
 ["SKU / listing","A single product page (one design on one product)."],
 ["Mockup","A render of your design on a product, used in listings &amp; ads."],
 ["UGC","User-generated content &mdash; customer photos/videos."]],
 "tg",["22%","78%"])}

{callout("Quillmark on one page",
"<b>Sell:</b> original designs on POD products (zero inventory). "
"<b>Make money:</b> ~$10 profit/item, ~35% margin. "
"<b>Get traffic:</b> daily short-form video + Pinterest + marketplace SEO (free), then ads on winners. "
"<b>Start cost:</b> $15–$150. "
"<b>Ladder:</b> $1/day &rarr; $10/day on organic; $1k&ndash;$5k/mo by scaling winners + email + ads. "
"<b>Run it:</b> 30–45 min/day on batched content + automation. "
"<b>Rule #1:</b> original art only. <b>Rule #2:</b> double down on what sells.","flame")}

<hr class="sep">
<p class="small">Prepared as a BNBHubs strategy document. All figures are planning assumptions for
decision-making, not financial guarantees; print costs, fees and platform rules change &mdash; verify
live before committing spend. This consolidates the Quillmark Income Structure, the 1&ndash;5 Year
Board Plan, and the Founder &amp; Operator Manual into a single operating package.</p>
''')

# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------
html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(H)}</body></html>"
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Quillmark-POD-Business-Playbook.pdf")
HTML(string=html).write_pdf(out_path)
print("WROTE", out_path, os.path.getsize(out_path), "bytes")
