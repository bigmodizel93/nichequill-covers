#!/usr/bin/env python3
"""
Quillmark POD — Founder Brief, Agent Pipeline & 5-Year Board Plan
Companion to the Built-In Package playbook. Reuses the playbook's styling.

Run:  python3 build_founder_brief.py
Out:  Quillmark-Founder-Brief-and-5yr-Plan.pdf
"""
import os
from weasyprint import HTML
import build_booklet as bb   # reuse colors, CSS, helpers (no render on import)

INK, NAVY, TEXT, MUTE, FAINT, LINE, SOFT = bb.INK, bb.NAVY, bb.TEXT, bb.MUTE, bb.FAINT, bb.LINE, bb.SOFT
FLAME, FLAME2, GOLD, GREEN, TEAL = bb.FLAME, bb.FLAME2, bb.GOLD, bb.GREEN, bb.TEAL
nib, table, callout, kpi = bb.nib, bb.table, bb.callout, bb.kpi

# ---------------------------------------------------------------- agent pipeline diagram
def svg_pipeline():
    steps = [("1","Research","find a proven niche / phrase",FLAME),
             ("2","Generate","create the design",FLAME),
             ("3","List","publish across channels",FLAME),
             ("4","Market","content + pins + ads",FLAME),
             ("5","Analyze","kill losers, scale winners",FLAME)]
    out = ['<svg viewBox="0 0 920 250" width="100%" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'''<defs><marker id="pa" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0 0 L9 4.5 L0 9 z" fill="{FLAME}"/></marker></defs>''')
    x = 18; w = 158; gap = 18; y = 56; h = 78
    cx_list = []
    for i,(n,t,s,c) in enumerate(steps):
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="11" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>')
        out.append(f'<circle cx="{x+20}" cy="{y+20}" r="13" fill="{c}"/>')
        out.append(f'<text x="{x+20}" y="{y+25}" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">{n}</text>')
        out.append(f'<text x="{x+w/2+8}" y="{y+26}" text-anchor="middle" font-size="14" font-weight="700" fill="{TEXT}">{t}</text>')
        out.append(f'<text x="{x+w/2}" y="{y+52}" text-anchor="middle" font-size="10.4" fill="{MUTE}">{s}</text>')
        cx_list.append((x, x+w))
        if i < len(steps)-1:
            out.append(f'<path d="M{x+w} {y+h/2} l{gap} 0" stroke="{FLAME}" stroke-width="2.4" marker-end="url(#pa)"/>')
        x += w + gap
    # loop arrow back to step 1
    out.append(f'<path d="M{cx_list[-1][1]-20} {y+h} q40 70 -420 56 q-360 14 -380 -52" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#pa)"/>')
    out.append(f'<text x="460" y="232" text-anchor="middle" font-size="11.5" fill="{GREEN}" font-weight="700">Loop forever &mdash; this pipeline is the asset that rinse-repeats across businesses</text>')
    # agent vs you band
    out.append(f'<rect x="18" y="14" width="680" height="22" rx="6" fill="{SOFT}"/>')
    out.append(f'<text x="28" y="29" font-size="10.5" fill="{NAVY}"><tspan font-weight="800" fill="{FLAME}">AGENTS RUN:</tspan> steps 2&ndash;4 end to end &nbsp;·&nbsp; <tspan font-weight="800" fill="{INK}">YOU OWN:</tspan> niche taste (1) + the kill/scale call (5)</text>')
    out.append('</svg>')
    return "".join(out)

# ---------------------------------------------------------------- 5-year staircase
def svg_fiveyear():
    yrs = [("Y1","Validate","$1–3k/mo",60),
           ("Y2","Scale","$3–10k/mo",95),
           ("Y3","Multiply","$10–25k/mo",130),
           ("Y4","Portfolio","$25–50k/mo",165),
           ("Y5","Asset","$50k+/mo",195)]
    out = ['<svg viewBox="0 0 920 250" width="100%" xmlns="http://www.w3.org/2000/svg">']
    x = 40; bw = 150; gap = 22; base = 212
    cols = [NAVY, FLAME2, FLAME, "#D8431C", GREEN]
    for i,(tag,title,rev,h) in enumerate(yrs):
        y = base - h
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="8" fill="{cols[i]}"/>')
        out.append(f'<text x="{x+bw/2}" y="{y-26}" text-anchor="middle" font-size="14" font-weight="800" fill="{TEXT}">{tag} · {title}</text>')
        out.append(f'<text x="{x+bw/2}" y="{y-9}" text-anchor="middle" font-size="12" fill="{MUTE}">{rev}</text>')
        x += bw + gap
    out.append(f'<line x1="40" y1="{base}" x2="900" y2="{base}" stroke="{LINE}" stroke-width="1.5"/>')
    out.append(f'<text x="40" y="238" font-size="10.5" fill="{FAINT}">Planning targets, gated on Year-1 validation &mdash; not guarantees. Bar height = monthly revenue band.</text>')
    out.append('</svg>')
    return "".join(out)

H = []
add = H.append

# ---------- COVER ----------
add(f'''
<div class="cover">
  <div class="brandrow">{nib(58)}<span class="bn">Quillmark</span></div>
  <div class="eyebrow" style="margin-top:14mm">Founder Brief · Agent Pipeline · 5-Year Board Plan</div>
  <h1>The Model,<br>The Mentor,<br>The Map</h1>
  <div class="rule"></div>
  <div class="tag">Why print-on-demand should fire you up the way NicheQuill did &mdash; the proven
  operator to learn it from, the agent pipeline that makes it rinse-and-repeat, and the five-year
  plan to run Quillmark side-by-side with your other engines.</div>
  <div class="meta">
    Companion to <b>The Built-In Package</b> &nbsp;·&nbsp; A <b>BNBHubs</b> venture &nbsp;·&nbsp; v1.0
    <br><span style="font-size:9pt">Confidential. Projections are planning assumptions, not guarantees. First-pass research, not legal advice.</span>
  </div>
</div>''')

# ---------- 1 · RYAN HOGUE HOOK ----------
add(f'''
<h2 class="section">1 · The Mentor &mdash; Ryan Hogue, the &ldquo;Leon of POD&rdquo;</h2>
<p class="lead">You asked for the person who proves this works &mdash; the POD equivalent of Leon.
That person is <strong>Ryan Hogue</strong> (channel: <em>Ryan Hogue Passive Income</em>,
<span class="mute">@RyanHoguePassiveIncome</span>). Here is why he should light the same fire.</p>

{callout("The part that matters most",
"He got rich <b>running</b> the business, then taught it &mdash; not the other way around. A former "
"senior web developer and adjunct professor (~$117k/yr salary) who started a $0 print-on-demand side "
"hustle on Amazon in 2017, expanded it across Etsy, Walmart, eBay and Redbubble, and grew it into "
"~<b>$49k/month</b> across ~10 passive-income streams (~$500k+/yr). CNBC profiled him in 2024 and made "
"him an instructor in their passive-income course. His entire brand is one word: <b>automation</b>.","flame")}

<h3>Why it should hit you the way NicheQuill did</h3>
<p>Ryan built his automation <strong>by hand, alone, over years</strong> &mdash; scraping niches,
uploading designs across marketplaces, wiring up tools like his own <em>PODTurbo</em> uploader.
<strong>You already have the agent stack he wished he had.</strong> Same method, you skip the grind.
His one-line method is almost exactly the NicheQuill move applied to merch:</p>
{callout("Ryan&rsquo;s method in one line",
"Find a proven niche/phrase &rarr; generate the design &rarr; list it across multiple POD marketplaces "
"&rarr; let winners compound, kill the losers.","note")}

<h3>Watch in this order (the belief-builder)</h3>
{table(["#","Video","Why watch it"],
[["1","<b>Print-on-Demand Starter Guide</b> (w/ Ryan Hogue)","The whole model in one beginner video"],
 ["2","<b>Ryan Hogue&rsquo;s Print On Demand Tips For Success</b>","How he actually picks winners &amp; scales"],
 ["3","<b>Making Print On Demand Money Online with Ryan Hogue</b>","Real numbers &amp; mindset &mdash; the fire-starter"],
 ["4","<b>How to Automate 100% of Your Amazon POD Business</b> (short)","This is literally your agent model"],
 ["5","<b>Printful POD Review / Tutorial for Beginners</b>","The fulfilment side, start to finish"]],
 "tg",["6%","48%","46%"])}
<p class="small">Links are in the Sources page at the back. On his channel, also search his niche-research and
Redbubble-automation uploads &mdash; those are the exact &ldquo;find a 5,000-sales/month niche&rdquo; move,
applied to merch.</p>

{callout("Stay sharp: the vet-before-you-buy filter",
"&ldquo;100% automated, undeniable proof, fully scalable&rdquo; is exactly what low-quality gurus sell. "
"Ryan is legit, but apply your own discipline before paying for any course: <b>(1)</b> Do they earn from "
"the method or from teaching it? <b>(2)</b> Independent proof, not just testimonials on their own funnel. "
"<b>(3)</b> Who owns the customer (Etsy/Amazon can switch you off)? <b>(4)</b> Is the automation real, or "
"hidden daily hustle? The honest truth everywhere is <b>80&ndash;95% automated after setup</b>, not 100%.","warn")}
''')

# ---------- 2 · THE AGENT PIPELINE ----------
add(f'''
<hr class="sep">
<h2 class="section">2 · The Agent Pipeline &mdash; what actually rinse-repeats</h2>
<p class="lead">You said you love the agent pipeline &mdash; here it is, formalized. The thing that clones
across businesses is <strong>not the concept, it&rsquo;s this pipeline.</strong> Research a niche,
generate the asset, list it, market it, iterate. Models where this transfers with almost no change
are the true clones of your PDF engine.</p>

<div class="diagram avoid-break">{svg_pipeline()}
<div class="cap">Figure 1 — The Quillmark agent pipeline. Same five steps as your PDF engine; only the &ldquo;asset&rdquo; in step 2 changes (a design instead of a PDF).</div></div>

<h3>Where each business reuses this pipeline (the rinse-repeat map)</h3>
{table(["Business","Asset in step 2","Pipeline reuse","Verdict"],
[["NicheQuill / PDFTrender","Digital PDF guide","&mdash; (the original)","Proven model, validate revenue first"],
 ["Quillmark POD","A design on products","Step 2 swaps; 3&ndash;4 add channels","Closest physical cousin"],
 ["Kindle KDP / low-content books","Book interior + cover","Near-identical pipeline","True clone &mdash; build next"],
 ["Digital templates (Notion/Canva)","A template file","Near-identical pipeline","True clone &mdash; build next"],
 ["Stock asset packs","Presets/fonts/prompts","Near-identical pipeline","True clone"],
 ["Audiobooks of your guides","TTS of existing PDFs","Pure margin add-on","Free upside later"],
 ["Faceless YouTube / SEO sites","Video / article","New pipeline from scratch","Not a quick clone"]],
 "tg",["24%","22%","30%","24%"])}

{callout("The discipline that protects the whole portfolio",
"Rinse-and-repeat is the right instinct &mdash; but <b>repeat a model after one instance has pulled real "
"money, not before.</b> PDFTrender is built but not yet revenue-validated. &ldquo;Undeniable proof&rdquo; "
"describes Leon&rsquo;s / Ryan&rsquo;s numbers, not yet yours. Cloning an unproven bet 5&times; is 5&times; "
"the risk, not 5&times; the income. Smart order: prove one, then clone the <b>pipeline</b> (KDP and "
"templates first, because your agents barely change).","flame")}
''')

# ---------- 3 · SIDE-BY-SIDE ----------
add(f'''
<h2 class="section">3 · Running Quillmark side-by-side (the &ldquo;two engines by Friday&rdquo; play)</h2>
<p class="lead">Your plan is sound: stage Quillmark now while the Shopify/PDFTrender store finishes baking,
so by week&rsquo;s end you have two engines live and can watch which one pulls. This is the right use
of the wait &mdash; with one rule to keep it from becoming chaos.</p>

{table(["","NicheQuill / PDFTrender","Quillmark POD"],
[["Sells","Digital PDF guides","Original designs on physical products"],
 ["Delivery","Instant download (zero cost/order)","Printed &amp; shipped on demand (cost/order)"],
 ["Margin","Very high (~95%+)","Healthy (~30&ndash;45%)"],
 ["Channel","Shopify store","Etsy first, then Shopify + Amazon Merch"],
 ["Status","Built, awaiting launch (Fri)","Stage now, launch alongside"],
 ["Shared engine","The 5-step agent pipeline","The same 5-step pipeline"]],
 "tg",["18%","41%","41%"])}

{callout("The one rule for two engines",
"Each engine gets its <b>own dashboard and its own weekly review</b>, but they share the same batch "
"block and the same pipeline. Watch leading indicators side-by-side (reach &rarr; visits &rarr; sales). "
"Pour more time into whichever engine shows the earlier, cheaper sales &mdash; let the data, not the "
"excitement, allocate your hours.","win")}

<h3>Capital plan for the side-by-side test</h3>
<div class="kpis">
  {kpi("$15–$150","Quillmark start","Etsy lean &rarr; Shopify standard")}
  {kpi("$0","NicheQuill","Already built; launching Fri")}
  {kpi("$150–$450","optional ad test","only on a proven design")}
  {kpi("&lt;$600","total at risk","to run both engines for a month")}
</div>
<p class="small">You said you have funds to test something side-by-side &mdash; this is a low-cap test, not a big bet. The real investment is the content sprint, not cash.</p>
''')

# ---------- 4 · 5-YEAR BOARD PLAN ----------
add(f'''
<div class="page-break"></div>
<h2 class="section">4 · The 5-Year Board Plan</h2>
<p class="lead">Same long-horizon format as the PDFTrender board plan: where Quillmark goes each year,
what unlocks the next rung, and how it fits the BNBHubs portfolio. Every figure is a planning target
gated on the prior year&rsquo;s validation.</p>

<div class="diagram avoid-break">{svg_fiveyear()}
<div class="cap">Figure 2 — The 5-year arc: Validate &rarr; Scale &rarr; Multiply &rarr; Portfolio &rarr; Asset.</div></div>

{table(["Year","Theme","Revenue target*","What you do","What unlocks the next year"],
[["1","Validate &amp; systemize","$1–3k/mo by month 12","Launch Quillmark on Etsy; ship 150&ndash;400 listings; run the agent pipeline + 30-day content engine; find 3&ndash;5 winning designs/niches","Proof: a repeatable content&rarr;traffic&rarr;sale loop and real reviews"],
 ["2","Scale the winners","$3–10k/mo","Add Shopify + Amazon Merch + Redbubble; email list; light paid ads on proven designs only; hire first VA for listings/CS","ROAS &ge; 2 on ads; an audience you own"],
 ["3","Multiply","$10–25k/mo","Clone the pipeline into 2&ndash;3 adjacent niches/sub-brands; bring on a designer; ads manager; document every SOP","A team + SOPs running the pipeline without you in every step"],
 ["4","Portfolio","$25–50k/mo","Run Quillmark as one node of a multi-brand POD portfolio; reinvest into the other true-clone engines (KDP, templates)","Diversified, semi-autonomous brands; strong cash position"],
 ["5","Asset &amp; optionality","$50k+/mo","Mature brand(s) with their own equity: license designs, or operate for cash, or sell a brand (POD/ecom brands sell at multiples of profit)","A sellable asset &mdash; or a cash machine you choose to keep"]],
 "tg",["6%","18%","16%","36%","24%"])}
<p class="small">*Targets assume consistent execution and that Year-1 validation succeeds. POD is competitive; treat these as direction, not promises.</p>

<h3>Portfolio fit (BNBHubs)</h3>
<p>Quillmark is the <strong>physical-product arm</strong> of the BNBHubs &ldquo;Quill&rdquo; house
(alongside NicheQuill&rsquo;s digital guides). It diversifies revenue across <em>digital</em> and
<em>physical</em>, shares the same agent pipeline, and does not compete for the same hours as the core
businesses &mdash; the definition of a good portfolio addition.</p>

{callout("Compliance &amp; values alignment",
"The model is asset-based and requires no interest-based financing to start (halal-friendly): you sell "
"things you make. Keep it clean &mdash; <b>original or licensed art only</b> (never brands, logos, "
"characters, lyrics, names), honest marketing (no fake scarcity or false claims), and clear shipping/"
"returns. This single discipline protects Quillmark and the BNBHubs umbrella.","note")}
''')

# ---------- 5 · FOUNDER & OPERATOR MANUAL (quick reference) ----------
add(f'''
<h2 class="section">5 · Founder &amp; Operator Manual (quick reference)</h2>
<p class="lead">The operating detail lives in <em>The Built-In Package</em> (§8). This is the one-page
command card: who decides what, the cadence, and the numbers that matter.</p>

<h3>Roles &amp; decision rights</h3>
{table(["Role","Who","Owns"],
[["CEO / Board","You","Niche bets, brand, budget, the kill/scale calls"],
 ["Operator (pipeline)","Agents + you","Research, design, listing, content, fulfilment routing"],
 ["Support (later)","VA","Listings at volume, customer service, scheduling"],
 ["Creative (later)","Freelance designer","Design volume in proven niches"]],
 "tg",["26%","26%","48%"])}

<h3>The cadence</h3>
<div class="cols2">
<div>
<h4>Daily (30–45 min)</h4>
<ul><li>Orders &amp; messages (templates)</li><li>Post today&rsquo;s pre-made content</li><li>5 outreach DMs · reply/engage</li><li>Glance at the dashboard</li></ul>
</div>
<div>
<h4>Weekly / Monthly</h4>
<ul><li>Weekly: batch 3&ndash;5 designs + 7 videos; 2&ndash;4 listings; 1 email; review numbers</li><li>Monthly: cut losers, scale winners, set ad budget, plan next niches</li></ul>
</div>
</div>

<h3>The numbers that matter</h3>
{table(["Metric","Healthy target","Why"],
[["Gross margin / order","30–45%","Keeps the model worth running"],
 ["Conversion rate","1.5–3%","Listing/proof quality signal"],
 ["ROAS (if ads on)","&ge; 2.0x","Green light to scale spend"],
 ["Repeat rate","15%+ (with email)","Cheapest revenue you&rsquo;ll get"],
 ["Winners found","3–5 in Y1","The real Year-1 deliverable"]],
 "tg",["32%","28%","40%"])}

{callout("The first move (Monday)",
"Stage Quillmark now: lock the name, open the Etsy store, publish ONE design, and start the content "
"calendar &mdash; so by Friday both engines are live and you&rsquo;re comparing real data, not guessing.","flame")}

<div class="page-break"></div>
<h2 class="section">Sources &amp; links</h2>
<p class="small">Grounded in current web research (May 2026), not memory. Ryan Hogue&rsquo;s figures are
self-reported / press-reported; verify before paying for any course.</p>
<h4>Ryan Hogue &mdash; profile &amp; press</h4>
<ul class="small">
<li>CNBC: How I build lucrative side hustles ($11,400/wk) &mdash; cnbc.com/2024/05/02/passive-income-expert-ryan-hogue-how-i-build-lucrative-side-hustles.html</li>
<li>CNBC: Top passive-income side-hustle myths &mdash; cnbc.com/2024/03/25/ryan-hogue-top-passive-income-side-hustle-myths.html</li>
<li>CNBC: Favorite $0 side hustles &mdash; cnbc.com/2024/04/24/ryan-hogue-on-his-favorite-zero-dollar-side-hustles.html</li>
<li>CNBC author hub &mdash; cnbc.com/ryan-hogue/</li>
<li>Channel: YouTube &ldquo;Ryan Hogue Passive Income&rdquo; (@RyanHoguePassiveIncome) · site: ryanhogue.com</li>
</ul>
<h4>Videos (verified URLs)</h4>
<ul class="small">
<li>Print-on-Demand Starter Guide &mdash; youtube.com/watch?v=b_Sx8wz5BWY</li>
<li>Print On Demand Tips For Success &mdash; youtube.com/watch?v=gmb6Xq_H8XA</li>
<li>Making Print On Demand Money Online &mdash; youtube.com/watch?v=uGZjMs01ja0</li>
<li>Automate 100% of Your Amazon POD (short) &mdash; youtube.com/watch?v=qMyI_zmL4rs</li>
<li>Printful Review / Beginner Tutorial &mdash; youtube.com/watch?v=ONAvPYV0GZk</li>
</ul>
<h4>Balance / skeptic read (do your own diligence)</h4>
<ul class="small">
<li>Medium: &ldquo;Ryan Hogue: CNBC&rsquo;s Passive Income Prophet … or Poser?&rdquo; (a critical view &mdash; read it before buying a course)</li>
</ul>
<hr class="sep">
<p class="small">Companion to <b>Quillmark POD — The Built-In Package</b>. Consolidates the Ryan Hogue
founder brief, the agent pipeline, the side-by-side launch plan, the 5-year board plan, and the
founder/operator quick reference. Planning assumptions for decision-making, not financial or legal
guarantees; run a formal USPTO (class 25 apparel + 35 retail) and domain check before committing ad spend.</p>
''')

html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{bb.CSS}</style></head><body>{''.join(H)}</body></html>"
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Quillmark-Founder-Brief-and-5yr-Plan.pdf")
HTML(string=html).write_pdf(out_path)
print("WROTE", out_path, os.path.getsize(out_path), "bytes")
