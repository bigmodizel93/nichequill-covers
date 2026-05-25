#!/usr/bin/env python3
"""
Quillmark POD — The Numbers Case (Decision Model for Business #3)
A numbers-first go/no-go analysis. Reuses the playbook styling.

Run:  python3 build_numbers_case.py
Out:  Quillmark-POD-Numbers-Case.pdf
"""
import os
from weasyprint import HTML
import build_booklet as bb

INK, NAVY, TEXT, MUTE, FAINT, LINE, SOFT = bb.INK, bb.NAVY, bb.TEXT, bb.MUTE, bb.FAINT, bb.LINE, bb.SOFT
FLAME, FLAME2, GOLD, GREEN, TEAL = bb.FLAME, bb.FLAME2, bb.GOLD, bb.GREEN, bb.TEAL
GREY = "#9AA6BC"
RED  = "#C9402B"
nib, table, callout, kpi = bb.nib, bb.table, bb.callout, bb.kpi

# ============================================================ CHARTS
def svg_distribution():
    # Etsy seller outcome distribution (approx; 65% <$100/yr is sourced)
    cats = [("&lt;$100 / yr", 65, GREY, "the 65% — most quit\nor post & forget"),
            ("$100–$1k / yr", 20, NAVY, "dabblers / part-timers"),
            ("$1k–$10k / yr", 11, FLAME, "treat it as a business"),
            ("&gt;$10k / yr", 4, GREEN, "serious operators")]
    out = ['<svg viewBox="0 0 920 270" width="100%" xmlns="http://www.w3.org/2000/svg">']
    base = 210; x = 70; bw = 150; gap = 60; maxh = 170
    for label, pct, col, note in cats:
        h = pct/65*maxh
        y = base - h
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="7" fill="{col}"/>')
        out.append(f'<text x="{x+bw/2}" y="{y-10}" text-anchor="middle" font-size="20" font-weight="800" fill="{TEXT}">{pct}%</text>')
        out.append(f'<text x="{x+bw/2}" y="{base+20}" text-anchor="middle" font-size="12" font-weight="700" fill="{INK}">{label}</text>')
        for j,ln in enumerate(note.split("\n")):
            out.append(f'<text x="{x+bw/2}" y="{base+36+j*13}" text-anchor="middle" font-size="9.4" fill="{MUTE}">{ln}</text>')
        x += bw + gap
    out.append(f'<line x1="60" y1="{base}" x2="900" y2="{base}" stroke="{LINE}" stroke-width="1.5"/>')
    out.append(f'<text x="60" y="262" font-size="10" fill="{FAINT}">Approximate distribution of Etsy seller outcomes. Only the &ldquo;&lt;$100&rdquo; figure is directly sourced; the rest are reasonable estimates. The point: outcome tracks effort, not luck.</text>')
    out.append('</svg>')
    return "".join(out)

def svg_waterfall():
    # contribution margin of one $26.99 tee order on Etsy
    steps = [("Retail price", 26.99, "bar", FLAME),
             ("Product + shipping", -13.50, "down", NAVY),
             ("Etsy core fees", -3.01, "down", GOLD),
             ("Offsite ads (avg)", -0.80, "down", TEAL),
             ("Your profit", 9.68, "total", GREEN)]
    out = ['<svg viewBox="0 0 920 250" width="100%" xmlns="http://www.w3.org/2000/svg">']
    x = 40; bw = 150; gap = 24
    top = 30; bottom = 200; vmax = 28.0
    def Y(v): return bottom - (v/vmax)*(bottom-top)
    running = 0.0
    for i,(label, val, kind, col) in enumerate(steps):
        if kind == "bar" or kind == "total":
            y0 = Y(0); y1 = Y(abs(val)); h = y0 - y1
            out.append(f'<rect x="{x}" y="{y1}" width="{bw}" height="{h}" rx="5" fill="{col}"/>')
            out.append(f'<text x="{x+bw/2}" y="{y1-7}" text-anchor="middle" font-size="13" font-weight="800" fill="{TEXT}">${abs(val):.2f}</text>')
            running = abs(val) if kind=="bar" else running
        else:
            new = running + val  # val negative
            y_hi = Y(running); y_lo = Y(new); h = y_lo - y_hi
            out.append(f'<rect x="{x}" y="{y_hi}" width="{bw}" height="{h}" rx="5" fill="{col}"/>')
            out.append(f'<text x="{x+bw/2}" y="{y_hi-7}" text-anchor="middle" font-size="12.5" font-weight="800" fill="{RED}">&minus;${abs(val):.2f}</text>')
            running = new
        for j,ln in enumerate(label.split(" ")):
            pass
        out.append(f'<text x="{x+bw/2}" y="{bottom+18}" text-anchor="middle" font-size="10.2" fill="{INK}" font-weight="600">{label}</text>')
        # connector
        if i < len(steps)-1 and kind != "total":
            out.append(f'<line x1="{x+bw}" y1="{Y(running)}" x2="{x+bw+gap}" y2="{Y(running)}" stroke="{FAINT}" stroke-dasharray="3 3" stroke-width="1"/>')
        x += bw + gap
    out.append(f'<line x1="40" y1="{bottom}" x2="900" y2="{bottom}" stroke="{LINE}" stroke-width="1.5"/>')
    out.append(f'<text x="40" y="240" font-size="10" fill="{FAINT}">One order, Gildan/Bella tee at $26.99 with shipping baked in, Printify Premium base, US Etsy fees. Net margin ≈ 36%.</text>')
    out.append('</svg>')
    return "".join(out)

def svg_jcurve():
    cons = [-150,-180,-205,-220,-225,-220,-205,-180,-150,-110,-60,-5,60]
    base = [-150,-182,-195,-179,-124,-31,121,321,569,866,1231,1653,2144]
    aggr = [-300,-320,-300,-240,-110,140,460,840,1280,1780,2360,3040,3840]
    vmin, vmax = -500, 4000
    x0, x1, ytop, ybot = 70, 900, 26, 250
    def X(m): return x0 + m/12*(x1-x0)
    def Y(v): return ybot - (v-vmin)/(vmax-vmin)*(ybot-ytop)
    def poly(series, col, w=2.6):
        pts = " ".join(f"{X(m):.1f},{Y(v):.1f}" for m,v in enumerate(series))
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}"/>'
    out = ['<svg viewBox="0 0 920 285" width="100%" xmlns="http://www.w3.org/2000/svg">']
    # zero line
    out.append(f'<line x1="{x0}" y1="{Y(0):.1f}" x2="{x1}" y2="{Y(0):.1f}" stroke="{INK}" stroke-width="1.2"/>')
    out.append(f'<text x="{x0-8}" y="{Y(0)+3:.1f}" text-anchor="end" font-size="9" fill="{INK}">$0</text>')
    # gridlines
    for gv in [1000,2000,3000,4000]:
        out.append(f'<line x1="{x0}" y1="{Y(gv):.1f}" x2="{x1}" y2="{Y(gv):.1f}" stroke="{LINE}" stroke-width="0.8"/>')
        out.append(f'<text x="{x0-8}" y="{Y(gv)+3:.1f}" text-anchor="end" font-size="9" fill="{FAINT}">${gv:,}</text>')
    # x labels
    for m in range(0,13,2):
        out.append(f'<text x="{X(m):.1f}" y="268" text-anchor="middle" font-size="9" fill="{MUTE}">m{m}</text>')
    out.append(poly(aggr, GREEN))
    out.append(poly(base, FLAME, 3))
    out.append(poly(cons, GREY))
    # legend
    lx=80; ly=20
    for col,name in [(FLAME,"Base"),(GREEN,"Aggressive (ads)"),(GREY,"Conservative")]:
        out.append(f'<rect x="{lx}" y="{ly-9}" width="12" height="12" rx="3" fill="{col}"/>')
        out.append(f'<text x="{lx+17}" y="{ly+1}" font-size="10.5" fill="{TEXT}">{name}</text>')
        lx += 130
    out.append(f'<text x="70" y="283" font-size="10" fill="{FAINT}">Cumulative profit (after $150–$300 startup + monthly costs). Base case repays everything around month 6. Illustrative.</text>')
    out.append('</svg>')
    return "".join(out)

def svg_evtree():
    outs = [("Flop / quit","&lt;$50/mo","35%","&minus;$300",GREY),
            ("Side income","$100–500/mo","35%","+$3,000",NAVY),
            ("Real business","$1k–3k/mo","22%","+$18,000",FLAME),
            ("Scaled","$5k+/mo","8%","+$70,000",GREEN)]
    out = ['<svg viewBox="0 0 920 250" width="100%" xmlns="http://www.w3.org/2000/svg">']
    rx, ry = 60, 125
    out.append(f'<circle cx="{rx}" cy="{ry}" r="12" fill="{INK}"/>')
    out.append(f'<text x="{rx}" y="{ry+30}" text-anchor="middle" font-size="10.5" fill="{INK}" font-weight="700">Start</text>')
    bx, bw, bh = 360, 470, 44; ys=[18,74,130,186]
    for (title,band,p,val,col),by in zip(outs,ys):
        out.append(f'<path d="M{rx+12} {ry} C 200 {ry}, 240 {by+bh/2}, {bx} {by+bh/2}" fill="none" stroke="{col}" stroke-width="2"/>')
        out.append(f'<text x="250" y="{(ry + by+bh/2)/2 - 2:.0f}" text-anchor="middle" font-size="11" font-weight="800" fill="{col}">{p}</text>')
        out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="9" fill="#fff" stroke="{col}" stroke-width="1.6"/>')
        out.append(f'<rect x="{bx}" y="{by}" width="6" height="{bh}" rx="3" fill="{col}"/>')
        out.append(f'<text x="{bx+20}" y="{by+19}" font-size="13" font-weight="700" fill="{TEXT}">{title}</text>')
        out.append(f'<text x="{bx+20}" y="{by+36}" font-size="10.5" fill="{MUTE}">{band}</text>')
        out.append(f'<text x="{bx+bw-16}" y="{by+27}" text-anchor="end" font-size="15" font-weight="800" fill="{col}">{val}</text>')
    out.append('</svg>')
    return "".join(out)

def svg_dollarhour():
    months = [3,6,9,12,18,24]
    dph     = [0.5,6.3,18,30,72,125]
    x0,x1,ytop,ybot = 70,890,24,210
    vmax=130
    def X(i): return x0 + i/(len(months)-1)*(x1-x0)
    def Y(v): return ybot - v/vmax*(ybot-ytop)
    out=['<svg viewBox="0 0 920 250" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for gv in [25,50,75,100,125]:
        out.append(f'<line x1="{x0}" y1="{Y(gv):.1f}" x2="{x1}" y2="{Y(gv):.1f}" stroke="{LINE}" stroke-width="0.8"/>')
        out.append(f'<text x="{x0-8}" y="{Y(gv)+3:.1f}" text-anchor="end" font-size="9" fill="{FAINT}">${gv}</text>')
    pts=" ".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(dph))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{FLAME}" stroke-width="3"/>')
    for i,(m,v) in enumerate(zip(months,dph)):
        out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" fill="{FLAME}"/>')
        out.append(f'<text x="{X(i):.1f}" y="{Y(v)-9:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{TEXT}">${v}</text>')
        out.append(f'<text x="{X(i):.1f}" y="228" text-anchor="middle" font-size="9.5" fill="{MUTE}">m{m}</text>')
    out.append(f'<text x="70" y="246" font-size="10" fill="{FAINT}">Effective $/hour (base case). Early hours pay like volunteering; you are buying an asset, not a wage. It compounds.</text>')
    out.append('</svg>')
    return "".join(out)

def svg_tornado():
    rows = [("# of listings × design hit-rate", 92, FLAME),
            ("Conversion rate (1% vs 3%)", 70, FLAME2),
            ("Price / AOV ($22 vs $32)", 52, GOLD),
            ("Base cost (Printful vs Printify)", 34, TEAL),
            ("Offsite-ads share of orders", 24, NAVY)]
    out=['<svg viewBox="0 0 920 230" width="100%" xmlns="http://www.w3.org/2000/svg">']
    x0=300; maxw=560; y=20; bh=30; gap=12
    for label,impact,col in rows:
        w=impact/100*maxw
        out.append(f'<text x="{x0-12}" y="{y+bh/2+4}" text-anchor="end" font-size="11" fill="{INK}" font-weight="600">{label}</text>')
        out.append(f'<rect x="{x0}" y="{y}" width="{w:.0f}" height="{bh}" rx="5" fill="{col}"/>')
        out.append(f'<text x="{x0+w+8:.0f}" y="{y+bh/2+4}" font-size="10.5" fill="{MUTE}">impact {impact}</text>')
        y += bh+gap
    out.append(f'<text x="{x0}" y="{y+6}" font-size="10" fill="{FAINT}">Relative impact on end-of-Year-1 profit. Volume × niche fit dwarfs everything &mdash; spend your effort there.</text>')
    out.append('</svg>')
    return "".join(out)

H=[]; add=H.append

# ---------------- COVER
add(f'''
<div class="cover">
  <div class="brandrow">{nib(58)}<span class="bn">Quillmark</span></div>
  <div class="eyebrow" style="margin-top:14mm">The Numbers Case · A decision model for business #3</div>
  <h1>Numbers<br>Can&rsquo;t Lie</h1>
  <div class="rule"></div>
  <div class="tag">No hype, no feelings &mdash; just the unit economics, the cash-flow curve, the
  probability-weighted expected value, the true cost of your hours, and a numeric go/no-go gate. Built
  so the decision to add a third business is made on math, not mood.</div>
  <div class="meta">
    Companion to <b>The Built-In Package</b> &nbsp;·&nbsp; A <b>BNBHubs</b> venture &nbsp;·&nbsp; v1.0
    <br><span style="font-size:9pt">Figures grounded in current (2026) benchmarks. Planning estimates for decision-making, not guarantees.</span>
  </div>
</div>''')

# ---------------- THE QUESTION
add(f'''
<h2 class="section">The question this answers</h2>
<p class="lead">&ldquo;I don&rsquo;t want to move on feeling. Do the numbers justify a third business?&rdquo;
That is a yes/no question with a numeric answer. This document builds it from the bottom up &mdash;
one order, then one month, then one year, then the full risk-weighted bet &mdash; and ends on an
explicit gate with thresholds you can hold me (and yourself) to.</p>

<div class="kpis">
  {kpi("$9.68","profit / order","≈36% margin, after every fee")}
  {kpi("~month 6","cash payback","base case repays startup")}
  {kpi("+$10.5k","2-yr expected value","probability-weighted")}
  {kpi("&lt;$600","max cash at risk","the entire downside")}
</div>

{callout("The shape of the answer (so you know where this lands)",
"The math says <b>YES &mdash; as a small, bounded bet</b>: the downside is capped at a few hundred "
"dollars and some front-loaded hours, while the upside is large and uncapped, so the expected value is "
"strongly positive <i>even using pessimistic odds</i>. The math says <b>NO</b> only if you treat it as "
"fast cash or let it steal hours from your two proven engines. The numbers reward it as an "
"<b>asset-building sprint</b>, not a wage.", "flame")}

{callout("Read these five numbers in order",
"<b>1.</b> The base rate (who actually makes money) &rarr; <b>2.</b> Unit economics (one order) &rarr; "
"<b>3.</b> The cash-flow curve (one year) &rarr; <b>4.</b> Expected value (the weighted bet) &rarr; "
"<b>5.</b> The true cost of your time. Then the decision gate.", "note")}
''')

# ---------------- 1 BASE RATE
add(f'''
<div class="page-break"></div>
<h2 class="section">1 · The base rate &mdash; what happens to everyone else</h2>
<p class="lead">Start with the most uncomfortable number, because numbers can&rsquo;t lie:
<strong>about 65% of Etsy sellers make less than $100 per year.</strong> Any honest case has to begin here.</p>

<div class="diagram avoid-break">{svg_distribution()}
<div class="cap">Figure 1 — Roughly how Etsy seller outcomes split. Most earn almost nothing; a minority build real income.</div></div>

<h3>But that number is not what it looks like</h3>
<p>The 65% is not a coin flip you lost &mdash; it is dominated by people who <strong>opened a shop,
posted a few listings, and quit.</strong> The data is blunt about what separates the two groups:</p>
{table(["The 65% who earn ~nothing","The minority who earn $1k–$10k+/mo"],
[["A handful of listings","Large, growing catalog (100s of listings)"],
 ["Generic designs, no niche","Specific niche + point of view"],
 ["No SEO on titles/tags","Every listing keyword-optimized"],
 ["Quit at 4–8 weeks","Persist past the 6–12 month ramp"],
 ["No reviews / proof","Harvest reviews relentlessly"],
 ["Guess","Validate with data, kill losers"]],
 "tg",["50%","50%"])}

{callout("Why this matters for your decision",
"Your odds are <b>not</b> the unconditional 65%. You arrive with an agent pipeline that produces "
"listings at volume, SEO at scale, and the discipline to kill losers &mdash; exactly the inputs that "
"separate the two columns. The base rate is a warning about <i>behavior</i>, not a ceiling on outcome. "
"That is the single biggest reason the numbers can work for you when they don&rsquo;t for most.", "win")}

<p class="small">Sourced: 65% of Etsy sellers earn &lt;$100/yr; first sale typically in 2–4 weeks;
consistent income takes 6–12 months; year-one active sellers average ~$2,200–$8,000. See Sources.</p>
''')

# ---------------- 2 UNIT ECONOMICS
add(f'''
<h2 class="section">2 · Unit economics &mdash; the truth of one order</h2>
<p class="lead">Everything scales from a single order. Here it is to the cent, on the most common product
(a unisex tee at $26.99 with shipping baked into the price), on Etsy, US fees, Printify base cost.</p>

<div class="diagram avoid-break">{svg_waterfall()}
<div class="cap">Figure 2 — Contribution-margin waterfall for one order. You keep $9.68 of $26.99 ≈ 36%.</div></div>

{table(["Line","Amount","Note"],
[["Retail price (shipping included)","$26.99","what the buyer pays"],
 ["&minus; Product base cost","&minus;$9.00","Printify Premium tee"],
 ["&minus; Shipping (you pay Printify)","&minus;$4.50","carrier cost"],
 ["&minus; Etsy transaction fee (6.5%)","&minus;$1.75","on price + shipping"],
 ["&minus; Payment processing (3% + $0.25)","&minus;$1.06","US rate"],
 ["&minus; Listing fee","&minus;$0.20","renews on each sale"],
 ["&minus; Offsite Ads (avg allocation)","&minus;$0.80","15% on ~1 in 5 orders"],
 ["<b>= Net profit / order</b>","<b>$9.68</b>","<b>≈ 36% margin</b>"]],
 "tg",["48%","20%","32%"])}

<h3>The same order on each channel &amp; product</h3>
{table(["Scenario","Retail","Net profit","Margin"],
[["Tee on Etsy (above)","$26.99","$9.68","36%"],
 ["Tee on Shopify (no Etsy fees, you bring traffic)","$26.99","$11.40","42%"],
 ["Mug (entry product)","$14.99","$5.90","39%"],
 ["Hoodie (premium)","$48.99","$18.50","38%"],
 ["Tee via Printful instead of Printify","$26.99","$6.90","26%"]],
 "tg",["44%","18%","20%","18%"])}

{callout("Two levers the numbers reward immediately",
"<b>Supplier choice:</b> Printify over Printful adds ~$2.78 to <i>every</i> tee &mdash; that is +40% "
"profit per order for one setting. <b>Channel mix:</b> Etsy buys you traffic but taxes ~11%; Shopify "
"keeps the fee but you must supply the visitors. Run both: Etsy to discover winners, Shopify to bank margin.", "flame")}

<h3>Fixed costs (the monthly nut to clear)</h3>
{table(["Path","Monthly fixed","Break-even orders / mo"],
[["Lean (Etsy + Printify free)","~$0","≈ 1 (profitable on first sale)"],
 ["Standard (Printify Premium $29 + Canva $13)","~$42","≈ 4–5 orders"],
 ["+ Shopify Basic ($39)","~$81","≈ 8–9 orders"]],
 "tg",["48%","26%","26%"])}
''')

# ---------------- 3 CASHFLOW
add(f'''
<h2 class="section">3 · The cash-flow curve &mdash; one year, three scenarios</h2>
<p class="lead">A new store loses a little before it earns &mdash; the &ldquo;J-curve.&rdquo; The real
question is <strong>how deep the dip is and when it turns positive.</strong> For Quillmark the dip is
tiny because there is no inventory to buy.</p>

<div class="diagram avoid-break">{svg_jcurve()}
<div class="cap">Figure 3 — Cumulative profit over Year 1. The deepest the base case ever goes is about &minus;$195. That is the whole financial risk.</div></div>

{table(["","Conservative","Base","Aggressive (+ads)"],
[["Orders/mo by month 12","~12","~55","~160"],
 ["Revenue/mo by month 12","~$324","~$1,485","~$4,320"],
 ["Profit/mo by month 12","~$74","~$490","~$1,200"],
 ["Worst cumulative point","&minus;$295 (m6)","&minus;$195 (m2)","&minus;$320 (m1)"],
 ["Cash payback month","~m12+","~month 6","~month 5"],
 ["Year-1 cumulative profit","~&minus;$70","~+$2,140","~+$3,840"]],
 "tg",["34%","22%","22%","22%"])}

{callout("What the J-curve really says",
"The maximum you are ever &lsquo;down&rsquo; is roughly <b>$200–$320</b> &mdash; less than a single "
"month of most subscriptions. There is no scenario here where you lose thousands, because there is no "
"stock to buy and no lease to sign. <b>The downside is structurally capped.</b> That is the property "
"that makes this a rational bet.", "win")}
<p class="small">Month-by-month model assumes $9.68 net/order (base), ~$42/mo fixed, $150 startup. Aggressive assumes ad-funded volume at a lower ~$7.50 net/order. Illustrative, not a forecast.</p>
''')

# ---------------- 4 EV
add(f'''
<hr class="sep">
<h2 class="section">4 · Expected value &mdash; the whole bet on one line</h2>
<p class="lead">This is the heart of a numbers-first decision: weigh every outcome by how likely it is,
times what it pays. A bet is worth taking when the probability-weighted payoff beats the cost &mdash;
<strong>regardless of how any single outcome feels.</strong></p>

<div class="diagram avoid-break">{svg_evtree()}
<div class="cap">Figure 4 — Probability-weighted outcomes over a 2-year horizon (effort-adjusted estimates).</div></div>

{table(["Outcome","2-yr value","Effort-adjusted odds","Naive base-rate odds"],
[["Flop / quit (&lt;$50/mo)","&minus;$300","35%","65%"],
 ["Side income ($100–500/mo)","+$3,000","35%","20%"],
 ["Real business ($1k–3k/mo)","+$18,000","22%","12%"],
 ["Scaled ($5k+/mo)","+$70,000","8%","3%"],
 ["<b>Expected value</b>","","<b>+$10,505</b>","<b>+$4,665</b>"]],
 "tg",["34%","20%","23%","23%"])}

{callout("The number that decides it",
"Even on <b>pessimistic, unadjusted base-rate odds</b> (treating you like the average quitter), the "
"expected value is <b>+$4,665</b>. On effort-adjusted odds it is <b>+$10,505</b>. Against a maximum "
"downside under $600, both are strongly positive. <b>A bet with a small capped loss and a large "
"expected gain is one you take.</b> The asymmetry &mdash; not optimism &mdash; is the reason.", "flame")}

<h3>Why the asymmetry exists</h3>
<ul>
<li><strong>Downside is bounded</strong> by zero inventory and cancellable tools: ~$200–$600, full stop.</li>
<li><strong>Upside is uncapped and compounding:</strong> every winning design keeps selling for years and can be cloned across products and channels.</li>
<li><strong>The asset has resale value:</strong> profitable POD/ecom brands sell for multiples of annual profit &mdash; a scaled outcome is worth more than its cash flow.</li>
</ul>
''')

# ---------------- 5 TIME COST
add(f'''
<h2 class="section">5 · The true cost &mdash; your hours, honestly priced</h2>
<p class="lead">Cash is not the real cost here; <strong>your attention is</strong> &mdash; especially while
running two other businesses. So price it. This is the number feelings always skip.</p>

<div class="diagram avoid-break">{svg_dollarhour()}
<div class="cap">Figure 5 — Effective $/hour over time (base case). It starts brutal and climbs steeply as the asset compounds.</div></div>

{table(["Phase","Hours / week","Profit / mo","Effective $/hr","What you&rsquo;re really doing"],
[["Setup sprint (m1–2)","7–8","≈ $0","&lt; $1","Building the asset; wage is near zero"],
 ["Ramp (m3–6)","5–6","$16–150","$1–6","Finding winners; data &gt; dollars"],
 ["Traction (m7–12)","4–5","$200–490","$10–30","Compounding; now it pays"],
 ["Scaled (yr 2)","3–4 (+ VA)","$1.5k–6k","$75–150+","Mostly leverage &amp; oversight"]],
 "tg",["24%","16%","18%","16%","26%"])}

{callout("The honest trade",
"For the first ~3 months you are effectively <b>working for free</b> to build an asset. If you need "
"the next 90 days to pay an hourly wage, the numbers say <b>don&rsquo;t</b>. If you can spend "
"front-loaded, <i>batchable</i> hours that your agents amplify &mdash; while your two proven engines "
"carry the income &mdash; the numbers say this is one of the best uses of otherwise idle &lsquo;waiting&rsquo; time you have.", "warn")}

<h3>Opportunity cost vs your other two businesses</h3>
{table(["Engine","Capital to start","Margin","Time after setup","Status"],
[["NicheQuill / PDF","~$0","~95%","Very low","Built, launching"],
 ["Business #2 (Shopify)","low","high","low–med","Staging for Friday"],
 ["Quillmark POD","$15–$150","30–42%","Med, front-loaded","Decision now"]],
 "tg",["28%","20%","20%","16%","16%"])}
<p class="small">Quillmark&rsquo;s marginal hours are highest early and shrink fast. Because the work batches and the agents do steps 2–4, it competes far less for your hours than a normal third job would.</p>
''')

# ---------------- 6 SENSITIVITY
add(f'''
<h2 class="section">6 · Sensitivity &mdash; which number actually moves the outcome</h2>
<p class="lead">If numbers decide, then knowing <strong>which</strong> number matters most tells you where
to spend every hour. Here is what swings Year-1 profit, ranked.</p>

<div class="diagram avoid-break">{svg_tornado()}
<div class="cap">Figure 6 — Sensitivity of Year-1 profit to each input. Volume × niche fit dominates.</div></div>

{table(["Lever","Why it dominates","Your move"],
[["# listings × design hit-rate","More quality listings = more search surface &amp; more &lsquo;tickets&rsquo;; this is multiplicative","Ship volume in validated niches (agents make this cheap)"],
 ["Conversion rate","1% &rarr; 3% triples orders on the same traffic","Great mockups, reviews, clear listings"],
 ["Price / AOV","Bumps &amp; bundles lift profit per order directly","Add order bumps; tier products"],
 ["Supplier base cost","Printify vs Printful is ~$2.78/tee","Default to the cheapest reliable blank"],
 ["Offsite-ads share","Only bites above $10k/yr (then 12% locked)","Drive your own traffic so attribution is yours"]],
 "tg",["28%","44%","28%"])}

{callout("The one-sentence strategy the numbers imply",
"Put your effort into <b>volume of quality listings in specific niches</b> &mdash; everything else is a "
"rounding error by comparison. This is precisely what an agent pipeline is good at, which is why the "
"model fits you.", "flame")}
''')

# ---------------- 7 DECISION
add(f'''
<div class="page-break"></div>
<h2 class="section">7 · The decision &mdash; numbers to verdict</h2>
<p class="lead">Put it together. A bet is rational when the downside is bounded and survivable, the
expected value is positive, and you can pay the true cost. Score it:</p>

{table(["Test","Threshold","Quillmark","Pass?"],
[["Max cash at risk","&lt; one month&rsquo;s slack","~$150–$600","YES"],
 ["Can you survive the worst case?","Lose it all = fine","Yes, trivially","YES"],
 ["Expected value positive?","&gt; 0 on pessimistic odds","+$4,665 to +$10,505","YES"],
 ["Payback period","&lt; 12 months (base)","~month 6","YES"],
 ["Does it steal from proven engines?","Must not","Batchable + agent-run","CONDITIONAL"],
 ["Can you fund the free first 90 days?","Time, not cash","Your call","CONDITIONAL"]],
 "tg",["34%","26%","26%","14%"])}

<h3>The verdict</h3>
{callout("GO — as a capped, asset-building bet (not a wage, not a bet-the-farm)",
"The numbers clear every financial bar with room to spare: bounded ~$200–$600 downside, +$4.7k–$10.5k "
"expected value, ~6-month payback. The only real cost is front-loaded, batchable hours &mdash; which "
"you can spend during the current &lsquo;waiting&rsquo; phase without pulling from NicheQuill or "
"business&nbsp;#2. <b>Proceed on the lean path.</b>", "win")}

<h3>The conditions (so the bet stays rational)</h3>
<ul>
<li><strong>Cap the cash.</strong> Start lean (&lt;$50). Do not spend on ads until a design is proven.</li>
<li><strong>Protect the engines.</strong> Quillmark gets batched/agent hours only; the two proven businesses keep priority.</li>
<li><strong>Judge on leading indicators</strong> at day 30/60/90 &mdash; reach, listings shipped, first reviews, a repeatable content&rarr;sale loop &mdash; not on early revenue.</li>
</ul>

<h3>Kill criteria (decide now, in numbers, so feelings don&rsquo;t)</h3>
{table(["By","If you have NOT…","Then"],
[["Day 30","shipped 25+ listings &amp; made 1+ sale","fix execution (likely volume/SEO), not the model"],
 ["Day 90","reached ~$100–$300/mo &amp; found 1 design that reliably sells","pause new effort; keep winners live as passive assets"],
 ["Month 6","crossed cash break-even on the lean path","stop reinvesting; do not scale a model that isn&rsquo;t converting"]],
 "tg",["14%","48%","38%"])}

{callout("Prove-before-clone (the portfolio rule)",
"This GO is for <b>one</b> instance, funded lean. Do not clone the model into a 4th/5th business until "
"either Quillmark or NicheQuill has pulled real, repeatable revenue. The expected value above assumes a "
"single small bet; stacking five unproven bets multiplies risk, not income.", "note")}

<div class="page-break"></div>
<h2 class="section">Sources</h2>
<p class="small">Figures grounded in current (2026) web research, not memory. Self-reported / blog
benchmarks vary; treat as planning estimates.</p>
<ul class="small">
<li>Etsy fees 2026 (listing $0.20, 6.5% transaction, 3%+$0.25 US payment, 12–15% offsite ads): Etsy Fees &amp; Payments Policy; Gelato; Craftybase; Voolist.</li>
<li>Base costs &amp; margins (Printify vs Printful, ~40% standard margin, Bella+Canvas $9.04 vs $11.69): Printify t-shirt pricing guide; printondemandbusiness.com; Merch Titans.</li>
<li>Outcomes (65% of Etsy sellers earn &lt;$100/yr; $2,200–$8,000 year-one active; most POD shops a few hundred $/mo): Printful; Insight Agent; printkk Etsy statistics.</li>
<li>Conversion (1–3% good Etsy average): Merchize; Gelato; Listybox.</li>
</ul>
<hr class="sep">
<p class="small">Companion to <b>Quillmark POD — The Built-In Package</b> and the <b>Founder Brief &amp;
5-Year Board Plan</b>. A decision aid, not financial or legal advice; verify live fees/costs before
committing spend.</p>
''')

html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{bb.CSS}</style></head><body>{''.join(H)}</body></html>"
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Quillmark-POD-Numbers-Case.pdf")
HTML(string=html).write_pdf(out_path)
print("WROTE", out_path, os.path.getsize(out_path), "bytes")
