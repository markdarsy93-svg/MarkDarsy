#!/usr/bin/env python3
"""Villa-owner valuation landing pages for dubaipalmresale.com (static, upload-ready).

Writes export/dubai-villa-valuation/<community>/index.html plus an index page and
ads.csv (Meta and Google ad copy per community). Run: python3 tools/villa_pages.py
"""
import csv, html, os
from urllib.parse import quote

SITE = "https://dubaipalmresale.com"
BASE = "/dubai-villa-valuation"
OUT = os.path.join(os.path.dirname(__file__), "..", "export", "dubai-villa-valuation")
WA = "https://wa.me/971585414999"
PHONE, TEL = "+971 58 541 4999", "+971585414999"
EMAIL = "mark@palmjebelali-resale.com"

# slug, name, developer, villa areas owners will recognise, one-line context
COMMUNITIES = [
    ("palm-jumeirah", "Palm Jumeirah", "Nakheel", ["Signature Villas", "Garden Homes", "Frond villas", "Canal Cove townhouses"], "Beachfront villas on Dubai's best-known island."),
    ("district-one", "District One", "Meydan Sobha", ["District One villas", "District One mansions", "Waterfront villas"], "Contemporary villas and mansions in Mohammed Bin Rashid City."),
    ("opal-gardens", "Opal Gardens", "", ["Opal Gardens townhouses", "Opal Gardens villas"], "Family villas and townhouses in a gated garden community."),
    ("nad-al-sheba-gardens", "Nad Al Sheba Gardens", "Meraas", ["Nad Al Sheba Gardens villas", "Nad Al Sheba Gardens townhouses"], "Family villas and townhouses close to Meydan and Downtown."),
    ("emirates-living", "Emirates Living", "Emaar", ["The Springs", "The Meadows", "The Lakes", "Emirates Hills"], "Established lake-side villa communities around The Greens."),
    ("dubai-hills-estate", "Dubai Hills Estate", "Emaar and Meraas", ["Club Villas", "Fairway Vistas", "Sidra", "Maple", "Parkway Vistas", "Golf Place", "Palm Hills"], "Golf-side villas around the Dubai Hills championship course."),
    ("sobha-hartland", "Sobha Hartland", "Sobha", ["Sobha Hartland villas", "Hartland Estates", "Sobha Hartland II villas"], "Green waterfront villas in Mohammed Bin Rashid City."),
    ("the-oasis", "The Oasis", "Emaar", ["Palmiera", "Mirage", "Lavita"], "Emaar's new lagoon-side villa community."),
    ("arabian-ranches", "Arabian Ranches", "Emaar", ["Arabian Ranches 1", "Arabian Ranches 2", "Arabian Ranches 3"], "Dubai's original desert-golf family villa community."),
    ("damac-lagoons", "Damac Lagoons", "Damac", ["Santorini", "Costa Brava", "Portofino", "Malta", "Venice", "Nice", "Morocco", "Mykonos"], "Mediterranean-themed townhouses and villas around crystal lagoons."),
    ("damac-hills", "Damac Hills", "Damac", ["Damac Hills villas", "Damac Hills townhouses", "Golf-view villas"], "Golf community villas and townhouses off Al Qudra Road."),
]

def esc(s): return html.escape(s, quote=True)
def wa(t): return WA + "?text=" + quote(t)

CSS = """:root{--ink:#1d1b18;--muted:#5d574e;--line:#e3dccf;--bg:#faf7f1;--cream:#f3ecdf;--gold:#a9874f}
@media (prefers-color-scheme:dark){:root{--ink:#f3ecdf;--muted:#c9c0b1;--line:#3a352e;--bg:#151310;--cream:#1d1a16}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Inter,system-ui,sans-serif}
a{color:inherit}.wrap{max-width:1120px;margin:0 auto;padding:0 20px}header{border-bottom:1px solid var(--line)}
header .wrap{display:flex;justify-content:space-between;align-items:center;min-height:68px;gap:12px}
.brand{font:600 20px Georgia,serif;text-decoration:none}.brand small{display:block;font:500 11px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.btn{display:inline-block;padding:14px 22px;border:1px solid var(--ink);text-decoration:none;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;cursor:pointer;background:none;color:var(--ink)}
.gold{background:var(--gold);border-color:var(--gold);color:#fff}section{padding:64px 0}.cream{background:var(--cream)}
h1{font:500 clamp(36px,6vw,64px)/1.05 Georgia,serif;margin:12px 0 18px}h2{font:500 clamp(28px,4vw,40px)/1.15 Georgia,serif;margin:0 0 14px}
.eyebrow{color:var(--gold);font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:600}.lead{color:var(--muted);max-width:640px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.chips span{border:1px solid var(--line);padding:6px 12px;font-size:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:48px}@media(max-width:820px){.grid{grid-template-columns:1fr;gap:28px}}
form{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:560px){form{grid-template-columns:1fr}}
.field label{display:block;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.field input,.field select,.field textarea{width:100%;padding:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:inherit}
.full{grid-column:1/-1}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}@media(max-width:820px){.steps{grid-template-columns:1fr}}
.steps div{border-top:1px solid var(--gold);padding-top:14px}.small{font-size:13px;color:var(--muted)}
details{border-top:1px solid var(--line);padding:14px 0}summary{cursor:pointer;font-weight:600}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}.cards a{border:1px solid var(--line);padding:20px;text-decoration:none}
footer{border-top:1px solid var(--line);padding:32px 0;font-size:14px;color:var(--muted)}"""

JS = """document.querySelectorAll('form[data-wa]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();
var l=[f.dataset.wa];f.querySelectorAll('.field').forEach(function(d){var a=d.querySelector('label'),i=d.querySelector('input,select,textarea');
if(a&&i&&i.value.trim())l.push(a.textContent+': '+i.value.trim())});window.open('%s?text='+encodeURIComponent(l.join('\\n')),'_blank')})});""" % WA

def shell(path, title, desc, body, ld=None):
    ldj = f'<script type="application/ld+json">{ld}</script>' if ld else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{SITE}{path}">
<style>{CSS}</style>{ldj}</head><body>
<header><div class="wrap"><a class="brand" href="{BASE}/">Mark Darsy<small>Dubai villa specialist</small></a><a class="btn" href="tel:{TEL}">Call Mark</a></div></header>
<main>{body}</main>
<footer><div class="wrap"><p>Mark Darsy · Regalia Tower, 1st Floor, Business Bay, Dubai · <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Valuations are written opinions of value prepared for the owner, not RICS valuations or advertisements. No property is advertised without the owner's signed instruction and a DLD advertising permit. Your details are used only to reply to your request; reply STOP to stop any updates.</p></div></footer>
<script>{JS}</script></body></html>"""

def page(slug, name, dev, areas, ctx):
    path = f"{BASE}/{slug}/"
    opts = "".join(f"<option>{esc(a)}</option>" for a in ["Not sure"] + areas)
    q = f"Hello Mark, I own a villa in {name} and would like a confidential valuation:"
    faq = [(f"What is my {name} villa worth?", f"It depends on the exact sub-community, plot, layout, upgrades, view and condition. Mark Darsy prepares a written opinion of value for your villa from recent comparable sales and current competition in {name}."),
           ("Is my request confidential?", "Yes. It goes only to Mark Darsy, who replies personally. Nothing is listed or advertised without your signed instruction and a DLD permit."),
           ("Can you also lease or manage my villa?", "Yes. If you would rather keep the villa, Mark can find a tenant and register the lease, or set it up as a licensed holiday home.")]
    body = f"""<section><div class="wrap grid"><div><span class="eyebrow">For {esc(name)} villa owners</span>
<h1>What is your {esc(name)} villa worth today?</h1><p class="lead">{esc(ctx)} Get a confidential, written valuation of your villa from Mark Darsy, a Dubai villa specialist with AED 200M+ in transactions.</p>
<div class="chips">{''.join(f'<span>{esc(a)}</span>' for a in areas)}</div>
<p><a class="btn gold" href="#valuation">Request my valuation</a> <a class="btn" href="{esc(wa(f'Hello Mark, I own a villa in {name}. Can we talk?'))}" target="_blank" rel="noopener">WhatsApp Mark</a></p></div>
<div class="cream" style="padding:28px" id="valuation"><h2>Tell us about your villa.</h2><p class="small">WhatsApp opens with your details. Press Send to share them privately with Mark.</p>
<form data-wa="{esc(q)}">
<div class="field"><label>Your name</label><input required autocomplete="name"></div>
<div class="field"><label>Sub-community</label><select>{opts}</select></div>
<div class="field"><label>Bedrooms</label><select><option>Not sure</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7+</option></select></div>
<div class="field"><label>Villa type</label><select><option>Villa</option><option>Townhouse</option><option>Mansion</option></select></div>
<div class="field"><label>What are you considering?</label><select><option>Just the value for now</option><option>Selling in the next 3 months</option><option>Selling later this year</option><option>Leasing it out</option><option>Holiday home</option></select></div>
<div class="field"><label>Monthly villa market update</label><select><option>Not now</option><option>Yes, send it to me</option></select></div>
<div class="field full"><label>Anything else</label><textarea rows="3" placeholder="Plot, upgrades, view, tenancy, timing"></textarea></div>
<div class="full"><button class="btn gold" type="submit" style="width:100%">Send my valuation request</button></div></form></div></div></section>
<section class="cream"><div class="wrap"><span class="eyebrow">How it works</span><h2>Valuation within 24 hours.</h2><div class="steps">
<div><b>1. Your details</b><p class="small">Send the basics on WhatsApp. Nothing is shared with anyone else.</p></div>
<div><b>2. Comparable evidence</b><p class="small">Recent {esc(name)} sales and the villas currently competing with yours.</p></div>
<div><b>3. Your options</b><p class="small">A written value range and the best route: sell, lease or hold.</p></div></div></div></section>
<section><div class="wrap"><h2>Questions owners ask.</h2>{''.join(f'<details><summary>{esc(a)}</summary><p class="small">{esc(b)}</p></details>' for a, b in faq)}</div></section>"""
    import json
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faq]})
    return path, shell(path, f"{name} Villa Valuation | Mark Darsy", f"What is your {name} villa worth? Request a confidential written valuation from Dubai villa specialist Mark Darsy.", body, ld)

def index():
    cards = "".join(f'<a href="{BASE}/{s}/"><b>{esc(n)}</b><p class="small">{esc(c)}</p></a>' for s, n, d, a, c in COMMUNITIES)
    body = f"""<section><div class="wrap"><span class="eyebrow">Dubai villa owners</span><h1>What is your villa worth today?</h1>
<p class="lead">Confidential, written valuations for villa and townhouse owners across Dubai's leading communities, from Mark Darsy, a Dubai villa specialist with AED 200M+ in transactions.</p></div></section>
<section class="cream"><div class="wrap"><h2>Choose your community.</h2><div class="cards">{cards}</div></div></section>"""
    return BASE + "/", shell(BASE + "/", "Dubai Villa Valuation | Mark Darsy", "Confidential villa valuations for owners in Palm Jumeirah, Dubai Hills, Arabian Ranches, District One, Emirates Living and more.", body)

def ads():
    rows = []
    for s, n, d, a, c in COMMUNITIES:
        url = f"{SITE}{BASE}/{s}/"
        rows.append({"community": n, "channel": "Meta", "headline": f"What's your {n} villa worth?",
                     "primary_text": f"{n} villa owners: get a confidential, written valuation of your villa within 24 hours from Mark Darsy, Dubai villa specialist with AED 200M+ in transactions. No listing, no obligation.",
                     "cta": "Get quote", "url": url, "targeting": f"Ages 35+, people living in or near {n}, interests: luxury real estate, Dubai property; exclude real estate agents"})
        rows.append({"community": n, "channel": "Google Search", "headline": f"{n[:30]} | Free Villa Valuation | Written Value in 24 Hours",
                     "primary_text": f"Own a villa in {n}? Get a confidential written valuation. | AED 200M+ in transactions. Request yours on WhatsApp today.",
                     "cta": "Request valuation", "url": url,
                     "targeting": f"Keywords: sell villa {n.lower()}; {n.lower()} villa valuation; {n.lower()} villa price; how much is my villa worth {n.lower()}"})
    return rows

if __name__ == "__main__":
    pages = [index()] + [page(*c) for c in COMMUNITIES]
    for path, content in pages:
        d = os.path.join(OUT, path[len(BASE):].strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(content)
    with open(os.path.join(OUT, "ads.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["community", "channel", "headline", "primary_text", "cta", "url", "targeting"])
        w.writeheader(); w.writerows(ads())
    print("wrote", len(pages), "pages and ads.csv to", os.path.normpath(OUT))
