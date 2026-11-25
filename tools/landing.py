#!/usr/bin/env python3
"""Lead-generation landing pages (ads destinations) for Mark Darsy.

Builds site/lp/<slug>/index.html for Athlon, Palm Jebel Ali and Nad Al Sheba Gardens.
Pages are noindex (paid/social traffic only) and are not linked from the main site nav.

  python3 tools/landing.py            -> writes into site/lp/
  python3 tools/landing.py --preview DIR -> self-contained copies (images inlined) for review

Every form submit:
  1. emails the lead to Mark's Gmail (same FormSubmit alias the main site uses)
  2. appends a row to the leads Google Sheet when SHEET_URL is set (Apps Script web app, see tools/leads_sheet.gs)
  3. fires a GA4 generate_lead event
  4. opens WhatsApp +971 58 541 4999 with the enquiry pre-written
"""
import base64, html, json, os, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "lp")
IMG = os.path.join(ROOT, "site", "images")

PHONE, TEL, WA = "+971 58 541 4999", "+971585414999", "https://wa.me/971585414999"
BRN = "52456"
GA4_ID = "G-NTDK9JD9R6"
FORMSUBMIT = "https://formsubmit.co/ajax/715e5c60acd46c05a631cf518901d219"
SHEET_URL = ""  # paste the Apps Script web-app URL here once Mark deploys tools/leads_sheet.gs
PERMIT = ""     # DLD / Trakheesi advertising permit number; leave empty until issued
PITCH = "Multiple units available at great prices. Contact me to discuss floor plans, prices and payment plan."
SERVICES = [
    ("Free valuation", "A written price opinion based on recent transfers and live competing listings."),
    ("Free premium listing", "Professional marketing on the main portals and to Mark's buyer database, at no listing cost."),
    ("Resale & leasing", "Sell, rent out, or sell and reinvest. One advisor from first call to transfer."),
    ("Furnishing & maintenance", "Furnishing, snagging and upkeep arranged so the home is ready to rent or sell."),
]

def esc(s): return html.escape(s, quote=True)

PAGES = [
  dict(
    slug="athlon",
    name="Athlon by Aldar",
    short="Athlon",
    title="Athlon by Aldar | Villas & Townhouses | Mark Darsy, Villa Specialist",
    desc="Athlon by Aldar in Dubailand: 3 and 4-bed townhouses, 3 to 6-bed villas. Ask Mark Darsy for floor plans, prices and payment plan, or a free valuation of your Athlon home.",
    eyebrow="Aldar · Dubailand, Dubai",
    h1="Athlon by Aldar.<br><em>Homes made for movement.</em>",
    hero="athlon-clubhouse.webp",
    hero_alt="Athlon Signature Clubhouse at dusk, developer render",
    facts=[("4.6 km", "trail-running loop"), ("3.7 km", "cycling loop, linked to Al Qudra"), ("7", "clubhouses"), ("25 min", "to DXB airport (developer figure)")],
    about_h="The first community in Dubai built around active living.",
    about=("Aldar designed Athlon with wellbeing experts so that every home is never more than 5 minutes from the next activity. "
           "A 2.2 km family loop, padel courts, a pump track, splash pads, lap and family pools, a skate park and a Signature Clubhouse you can cycle through. "
           "Athlon is set within one of the largest green spaces in Dubai, about 30 minutes from Jumeirah Beach (developer figure)."),
    units=[("Townhouses", "3 and 4 bedrooms", "4-plex cluster townhouses, Type 1 and Type 2."),
           ("Standard villas", "3, 4 and 5 bedrooms", "Detached villas, Type 1 and Type 2 designs."),
           ("Premium villas", "4, 5 and 6 bedrooms", "Horizon and Pillar designs on larger footprints.")],
    gallery=[("athlon-townhouses.webp", "Athlon 4-plex townhouses, front, developer render"),
             ("athlon-premium-villa.webp", "Athlon premium villa, developer render"),
             ("athlon-interior.webp", "Athlon villa living room, light scheme, developer render"),
             ("athlon-loop.webp", "Athlon cycling and running loop, developer render")],
    split=("athlon-masterplan.webp", "Athlon master plan aerial view, developer render"),
    types=["3-bed townhouse", "4-bed townhouse", "3-bed villa", "4-bed villa", "5-bed villa", "6-bed premium villa", "Not sure yet"],
    budgets=["Under AED 3M", "AED 3M – 4M", "AED 4M – 5M", "AED 5M – 7M", "AED 7M+"],
    owner_h="Own a home in Athlon?",
    creds=None,
    img_note="Images: Aldar's Athlon brochure, developer renders.",
  ),
  dict(
    slug="palm-jebel-ali",
    name="Palm Jebel Ali",
    short="Palm Jebel Ali",
    title="Palm Jebel Ali Villas | Resale & Off-Plan | Mark Darsy, Villa Specialist",
    desc="Palm Jebel Ali villas by Nakheel: Beach Collection and Coral Collection, 5 to 7 bedrooms. Ask Mark Darsy for floor plans, prices and payment plan, or a free valuation of your villa.",
    eyebrow="Nakheel · Palm Jebel Ali, Dubai",
    h1="Palm Jebel Ali villas.<br><em>Beachfront living on the fronds.</em>",
    hero="palm-jebel-ali-beach-villas.webp",
    hero_alt="Palm Jebel Ali Beach Collection villas on the shoreline, developer image",
    facts=[("12", "villa fronds, A–F and K–P"), ("90 km+", "of beachfront (Nakheel plan)"), ("5–7", "bedrooms"), ("Late 2026", "first handovers begin (Nakheel)")],
    about_h="Nakheel's new island, built around twelve villa fronds.",
    about=("Palm Jebel Ali's villas sit on twelve fronds, each with a sunrise side and a sunset side. Nakheel's published plan lists 7 islands, about 120 km of coastline and more than 90 km of beachfront. "
           "Nakheel states that a phased handover of the first villas begins in late 2026 and continues through 2027. "
           "Most buying today is resale from original owners, with the remaining developer payment plan taken over by the buyer."),
    units=[("Beach Collection", "5 and 6 bedrooms", "Detached frond villas by studios including SAOTA, NAGA, LW Design and LOCI."),
           ("Coral Collection", "6 and 7 bedrooms", "The larger frond residences, including Coral Dune and Sunset Mirage designs."),
           ("Beachfront mansions", "7 bedrooms", "Selected larger plots and signature designs. Ask for what is available now.")],
    gallery=[("pja-beach-villas-evening.webp", "Palm Jebel Ali beach villas at evening, developer image"),
             ("palm-jebel-ali-frond-villas.webp", "Palm Jebel Ali villas along a frond, developer image"),
             ("pja-fronds-masterplan.webp", "Palm Jebel Ali fronds master plan"),
             ("pja-aerial-progress-overview-v2.webp", "Palm Jebel Ali construction progress, aerial photograph")],
    split=("pja-connectivity-map-v2.webp", "Palm Jebel Ali location and connectivity map"),
    types=["5-bed Beach Collection", "6-bed Beach Collection", "6-bed Coral Collection", "7-bed Coral / mansion", "Not sure yet"],
    budgets=["AED 15M – 20M", "AED 20M – 30M", "AED 30M – 50M", "AED 50M+"],
    owner_h="Own a villa on Palm Jebel Ali?",
    creds=["AED 200M+ in Palm Jebel Ali transactions", "Direct purchase experience with Nakheel", "VIP access to selected developer stock"],
    img_note="Villa images are developer conceptual imagery, not a specific resale villa; aerial photograph supplied by Mark Darsy.",
  ),
  dict(
    slug="nad-al-sheba-gardens",
    name="Nad Al Sheba Gardens",
    short="Nad Al Sheba Gardens",
    title="Nad Al Sheba Gardens Villas | Meraas | Mark Darsy, Villa Specialist",
    desc="Nad Al Sheba Gardens by Meraas: townhouses and 4 to 7-bed villas around a swimmable lagoon. Ask Mark Darsy for floor plans, prices and payment plan, or a free valuation.",
    eyebrow="Meraas · Nad Al Sheba, Dubai",
    h1="Nad Al Sheba Gardens.<br><em>Family villas around a lagoon.</em>",
    hero=None,
    hero_alt="",
    facts=[("Meraas", "master developer"), ("3–7", "bedrooms, townhouses and villas"), ("Lagoon", "swimmable, with beach-style shores"), ("Gated", "family community")],
    about_h="A gated Meraas community close to Meydan and Downtown.",
    about=("Nad Al Sheba Gardens is a gated villa community by Meraas, built in phases around landscaped parks and a swimmable lagoon. "
           "Homes range from 3-bedroom townhouses to 4 to 7-bedroom villas with open-plan layouts, and the newer phases add larger villas facing the water and green spaces. "
           "Phases, layouts and availability differ, so tell Mark which phase or size you want and he will send what is available now."),
    units=[("Townhouses", "3 bedrooms", "Family townhouses in the earlier and newer phases."),
           ("Villas", "4 and 5 bedrooms", "Detached villas, open-plan with double-height living in newer designs."),
           ("Large villas", "6 and 7 bedrooms", "Selected larger villas on the lagoon and parks. Ask for what is available now.")],
    gallery=[],
    types=["3-bed townhouse", "4-bed villa", "5-bed villa", "6-bed villa", "7-bed villa", "Not sure yet"],
    budgets=["Under AED 5M", "AED 5M – 8M", "AED 8M – 12M", "AED 12M – 20M", "AED 20M+"],
    owner_h="Own a home in Nad Al Sheba Gardens?",
    creds=None,
    img_note="",
  ),
]

CSS = r"""
:root{--ivory:#FBF8F2;--cream:#F3EDE2;--ink:#1E1D1B;--char:#2B2A27;--mut:#6B665D;--line:#E3DACB;--gold:#B08D57;--gold-d:#8C6D3F;--ok:#2F6B4F;--err:#A23B2A}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ivory);color:var(--ink);font:16px/1.6 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
img{max-width:100%;display:block}a{color:inherit}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;line-height:1.08;margin:0 0 .5em;letter-spacing:-.01em}
h1{font-size:clamp(2.3rem,5.4vw,4rem)}h1 em,h2 em{font-style:italic;color:var(--gold)}
h2{font-size:clamp(1.9rem,3.6vw,2.8rem)}h3{font-size:1.5rem}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.eyebrow{display:inline-block;font-size:.74rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:14px}
.top{position:absolute;inset:0 0 auto;z-index:5;padding:18px 0}
.top .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff}
.mono{width:40px;height:40px;border:1px solid rgba(255,255,255,.6);display:grid;place-items:center;font-family:"Cormorant Garamond",serif;font-size:1.15rem}
.brand b{display:block;font-weight:600;letter-spacing:.02em}.brand small{display:block;font-size:.72rem;opacity:.85;letter-spacing:.06em}
.toplinks{display:flex;gap:10px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:0 22px;border:1px solid transparent;font:600 .92rem/1 Inter,system-ui,sans-serif;letter-spacing:.02em;text-decoration:none;cursor:pointer;border-radius:2px;transition:background .2s,color .2s}
.btn-gold{background:var(--gold);color:#fff}.btn-gold:hover{background:var(--gold-d)}
.btn-line{border-color:currentColor;background:transparent}
.btn-wa{background:#1F7A4D;color:#fff}.btn-wa:hover{background:#17603c}
.btn svg{width:18px;height:18px}
.hero{position:relative;color:#fff;background:#1e1d1b center/cover no-repeat;padding:120px 0 64px;min-height:640px}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,17,15,.82) 0%,rgba(18,17,15,.55) 50%,rgba(18,17,15,.25) 100%)}
.hero.plain{background:radial-gradient(1200px 600px at 85% 10%,#3a3630 0%,#1e1d1b 60%)}
.hero.plain:after{content:"";position:absolute;inset:0;opacity:.18;background:repeating-radial-gradient(circle at 80% 30%,transparent 0 22px,rgba(176,141,87,.55) 23px 24px)}
.hero.plain:before{display:none}
.hero-grid{position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:start}
.hero p.lead{font-size:1.12rem;max-width:34em;color:rgba(255,255,255,.92)}
.hero .btns{display:flex;flex-wrap:wrap;gap:12px;margin:26px 0 22px}
.hero .btn-line{color:#fff}
.ticks{list-style:none;padding:0;margin:0;display:grid;gap:6px;font-size:.95rem;color:rgba(255,255,255,.9)}
.ticks li:before{content:"✓";color:var(--gold);margin-right:10px;font-weight:700}
.card{background:#fff;color:var(--ink);padding:28px;border-radius:3px;box-shadow:0 24px 60px rgba(0,0,0,.28)}
.card h3{margin-bottom:4px}.card .sub{color:var(--mut);font-size:.9rem;margin:0 0 16px}
form .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
form label{display:block;font-size:.78rem;font-weight:600;letter-spacing:.04em;margin:12px 0 5px;color:var(--char)}
form input,form select,form textarea{width:100%;min-height:46px;padding:10px 12px;border:1px solid var(--line);background:var(--ivory);font:inherit;font-size:16px;color:var(--ink);border-radius:2px}
form input:focus,form select:focus,form textarea:focus{outline:2px solid var(--gold);outline-offset:0;border-color:var(--gold)}
.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.seg{position:relative}.seg input{position:absolute;left:0;top:0;width:1px;height:1px;min-height:0;opacity:0;pointer-events:none}
form{position:relative;overflow:hidden}
.seg label{margin:0;display:flex;align-items:center;justify-content:center;text-align:center;min-height:46px;border:1px solid var(--line);background:var(--ivory);font-size:.85rem;cursor:pointer;padding:6px}
.seg input:checked+label{border-color:var(--gold);background:#F6EEDD;color:var(--gold-d)}
.seg input:focus-visible+label{outline:2px solid var(--gold)}
.consent{display:flex;gap:10px;align-items:flex-start;font-size:.78rem;color:var(--mut);margin-top:14px}
.consent input{width:18px;min-height:18px;margin-top:2px;flex:none}
form .btn{width:100%;margin-top:16px}
.formmsg{font-size:.9rem;margin-top:12px;display:none}.formmsg.ok{display:block;color:var(--ok)}.formmsg.err{display:block;color:var(--err)}
.hp{position:absolute;left:0;top:0;width:1px;height:1px;min-height:0;padding:0;border:0;opacity:0;overflow:hidden;clip:rect(0 0 0 0)}
.chips{display:flex;flex-wrap:wrap;gap:8px;position:relative}
.chips input{position:absolute;left:0;top:0;width:1px;height:1px;min-height:0;opacity:0;pointer-events:none}
.chips label{margin:0;padding:9px 12px;border:1px solid var(--line);background:var(--ivory);font-size:.82rem;cursor:pointer;min-height:40px;display:flex;align-items:center}
.chips label:before{content:"";width:14px;height:14px;border:1px solid var(--mut);margin-right:8px;border-radius:2px}
.chips input:checked+label{border-color:var(--gold);background:#F6EEDD;color:var(--gold-d)}
.chips input:checked+label:before{background:var(--gold);border-color:var(--gold);box-shadow:inset 0 0 0 2px #F6EEDD}
.chips input:focus-visible+label{outline:2px solid var(--gold)}
.packhead{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:end}.packhead p{color:var(--char);margin:0 0 .6em}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:30px}
.tile{display:flex;flex-direction:column;gap:6px;padding:26px 22px;background:#fff;border:1px solid var(--line);text-decoration:none;transition:border-color .2s,transform .2s}
.tile:hover{border-color:var(--gold);transform:translateY(-2px)}
.tile b{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.6rem;font-weight:500}.tile span{color:var(--mut);font-size:.9rem}
.tile i{font-style:normal;font-weight:600;font-size:.88rem;color:var(--gold-d);margin-top:10px}
@media (max-width:960px){.packhead{grid-template-columns:1fr;gap:6px}.tiles{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.tiles{gap:10px}.tile{padding:18px 14px}.tile b{font-size:1.35rem}}
.facts{background:var(--char);color:#fff}
.facts .wrap{display:grid;grid-template-columns:repeat(4,1fr)}
.facts div{padding:26px 18px;border-left:1px solid rgba(255,255,255,.12)}.facts div:first-child{border-left:0}
.facts b{display:block;font-family:"Cormorant Garamond",serif;font-size:2.1rem;font-weight:500;color:var(--gold);line-height:1.1}
.facts span{font-size:.85rem;color:rgba(255,255,255,.8)}
section.s{padding:84px 0}section.cream{background:var(--cream)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.split p{color:var(--char)}
.split img{width:100%;aspect-ratio:4/3;object-fit:cover}
.units{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:32px}
.unit{background:#fff;border:1px solid var(--line);padding:28px}
.unit .beds{display:block;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:8px}
.unit p{margin:0 0 18px;color:var(--mut);font-size:.95rem}
.unit a{font-weight:600;font-size:.9rem;color:var(--gold-d);text-decoration:none}
.gal{display:grid;grid-template-columns:2fr 1fr 1fr;grid-auto-rows:220px;gap:10px;margin-top:32px}
.gal img{width:100%;height:100%;object-fit:cover}.gal img:first-child{grid-row:span 2}
.gal img:nth-child(4){grid-column:span 2}
.center{text-align:center}.narrow{max-width:760px;margin:0 auto}
.svc{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin:36px 0 30px;text-align:left}
.svc div{border-top:2px solid var(--gold);padding-top:16px}.svc b{display:block;font-size:1.02rem;margin-bottom:6px}
.svc p{margin:0;color:var(--mut);font-size:.92rem}
.dark{background:var(--ink);color:#fff}.dark .svc p{color:rgba(255,255,255,.72)}.dark .btn-line{color:#fff}
.btnrow{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.creds{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:22px 0 0;padding:0;list-style:none}
.creds li{border:1px solid var(--line);padding:8px 14px;font-size:.88rem;background:#fff}
.mark{display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:center;max-width:820px;margin:0 auto}
.mark .mono{width:92px;height:92px;border-color:var(--gold);color:var(--gold);font-size:2.2rem}
.foot{background:#141311;color:rgba(255,255,255,.7);font-size:.82rem;padding:40px 0 110px}
.foot p{margin:0 0 10px;max-width:900px}.foot a{color:#fff}
.permit{display:inline-block;border:1px dashed rgba(255,255,255,.35);padding:6px 12px;margin:6px 0 14px;color:#fff}
.cbar{position:fixed;left:0;right:0;bottom:0;z-index:20;display:none;grid-template-columns:1fr 1fr;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(251,248,242,.96);border-top:1px solid var(--line);backdrop-filter:blur(6px)}
.cbar .btn{min-height:46px;padding:0 10px}.cbar .btn-line{color:var(--ink)}
@media (max-width:960px){
 .hero{padding:104px 0 40px;min-height:0}
 .hero:before{background:linear-gradient(180deg,rgba(18,17,15,.55) 0%,rgba(18,17,15,.82) 60%,rgba(18,17,15,.92) 100%)}
 .hero-grid,.split{grid-template-columns:1fr;gap:30px}
 .facts .wrap{grid-template-columns:1fr 1fr}.facts div{border-left:0;border-top:1px solid rgba(255,255,255,.12)}
 .facts div:nth-child(-n+2){border-top:0}.facts div:nth-child(even){border-left:1px solid rgba(255,255,255,.12)}
 .units,.svc{grid-template-columns:1fr 1fr}
 .gal{grid-template-columns:1fr 1fr;grid-auto-rows:160px}.gal img:first-child{grid-column:span 2;grid-row:auto}.gal img:nth-child(4){grid-column:span 2}
 section.s{padding:60px 0}
 .toplinks .btn-line{display:none}
 .cbar{display:grid}
}
@media (max-width:560px){
 .wrap{padding:0 16px}.card{padding:22px 18px}
 form .row,.units,.svc{grid-template-columns:1fr}
 .seg{grid-template-columns:1fr 1fr}
 .brand small{display:none}.toplinks .btn{min-height:42px;padding:0 14px;font-size:.85rem}
 .mark{grid-template-columns:1fr;text-align:center}.mark .mono{margin:0 auto}
 .facts b{font-size:1.7rem}
}
"""

FONTS_LOCAL = """
@font-face{font-family:"Cormorant Garamond";font-style:normal;font-weight:500;font-display:swap;src:url(/fonts/cormorant-garamond-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Cormorant Garamond";font-style:italic;font-weight:500;font-display:swap;src:url(/fonts/cormorant-garamond-latin-500-italic.woff2) format("woff2")}
@font-face{font-family:Inter;font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/inter-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/inter-latin-600-normal.woff2) format("woff2")}
"""

WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.6 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1a17 17 0 0 1-1.8-.7 13.6 13.6 0 0 1-5.2-4.6c-.4-.5-1.2-1.7-1.2-3.2s.8-2.3 1.1-2.6c.3-.3.6-.4.8-.4h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.7-.1l1-1.2c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.6.3.1.2.1.8-.2 1.5Z"/></svg>'

JS = r"""
(function(){
var CFG=window.LP||{};
var q=new URLSearchParams(location.search),utm={};
['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid','gclid'].forEach(function(k){var v=q.get(k);if(v)utm[k]=v});
function ga(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(e){}}
document.querySelectorAll('[data-intent]').forEach(function(a){a.addEventListener('click',function(){
  var r=document.querySelector('input[name=intent][value="'+a.getAttribute('data-intent')+'"]');if(r){r.checked=true;r.dispatchEvent(new Event('change'))}
  var w=a.getAttribute('data-want');if(w){document.querySelectorAll('input[name=want]').forEach(function(c){c.checked=(c.value===w)})}
  ga('cta_click',{page:CFG.page,cta:a.textContent.trim()})})});
document.querySelectorAll('a[href^="https://wa.me"]').forEach(function(a){a.addEventListener('click',function(){ga('whatsapp_click',{page:CFG.page})})});
document.querySelectorAll('a[href^="tel:"]').forEach(function(a){a.addEventListener('click',function(){ga('call_click',{page:CFG.page})})});
var f=document.getElementById('lead');if(!f)return;
var buyF=f.querySelectorAll('.buyonly'),sellF=f.querySelectorAll('.sellonly');
function sync(){var v=(f.querySelector('input[name=intent]:checked')||{}).value||'Buy';
  buyF.forEach(function(e){e.hidden=(v==='Sell')});sellF.forEach(function(e){e.hidden=(v==='Buy')});}
f.querySelectorAll('input[name=intent]').forEach(function(r){r.addEventListener('change',sync)});sync();
f.addEventListener('submit',function(ev){
  ev.preventDefault();var msg=f.querySelector('.formmsg');msg.className='formmsg';
  if(f._honey.value)return;
  var d={};new FormData(f).forEach(function(v,k){if(k==='_honey')return;v=String(v).trim();d[k]=d[k]?d[k]+', '+v:v});
  var digits=(d.phone||'').replace(/\D/g,'');
  if(!d.name||digits.length<8){msg.textContent='Please add your name and a phone number with country code.';msg.className='formmsg err';return}
  if(!f.consent.checked){msg.textContent='Please tick the box so Mark can contact you.';msg.className='formmsg err';return}
  if(d.intent==='Buy'){delete d.unit}else if(d.intent==='Sell'){delete d.budget;delete d.want}
  d.page=CFG.page;d.url=location.href.split('?')[0];d.submitted=new Date().toISOString();Object.keys(utm).forEach(function(k){d[k]=utm[k]});
  var payload=Object.assign({_subject:'New '+CFG.page+' lead: '+d.intent+' · '+d.name,_template:'table',_captcha:'false'},d);
  try{fetch(CFG.formsubmit,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(payload),keepalive:true}).catch(function(){})}catch(e){}
  if(CFG.sheet){try{fetch(CFG.sheet,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(d),keepalive:true}).catch(function(){})}catch(e){}}
  ga('generate_lead',{page:CFG.page,intent:d.intent});
  var t='Hello Mark, I am interested in '+CFG.page+'.\n'+
    'Name: '+d.name+'\nI want to: '+d.intent+
    (d.type?'\nType: '+d.type:'')+(d.budget?'\nBudget: '+d.budget:'')+(d.unit?'\nMy unit: '+d.unit:'')+(d.timeline?'\nTimeline: '+d.timeline:'')+
    (d.intent==='Sell'?'\nPlease send me a free valuation.':'\nPlease send: '+(d.want||'floor plans, prices and payment plan')+'.');
  msg.innerHTML='Thank you, '+d.name.split(' ')[0].replace(/[<>&]/g,'')+'. Mark has your details and will contact you shortly. WhatsApp is opening so you can reach him now.';msg.className='formmsg ok';
  f.querySelector('button[type=submit]').textContent='Sent ✓';
  setTimeout(function(){window.open(CFG.wa+'?text='+encodeURIComponent(t),'_blank','noopener')},350);
});
})();
"""

def img_src(name, inline):
    if not inline: return f"/images/lp/{name}" if name.startswith("athlon-") else f"/images/{name}"
    p = os.path.join(IMG, "lp", name) if name.startswith("athlon-") else os.path.join(IMG, name)
    with open(p, "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()

def wa(text): return WA + "?text=" + quote(text)

def build(p, inline=False):
    name, short, slug = p["name"], p["short"], p["slug"]
    hero_style = f' style="background-image:url({img_src(p["hero"], inline)})"' if p["hero"] else ""
    hero_cls = "hero" if p["hero"] else "hero plain"
    wa_buy = wa(f"Hello Mark, I am interested in {name}. Please send floor plans, prices and payment plan.")
    wa_sell = wa(f"Hello Mark, I own a property in {name}. I would like a free valuation.")
    opts = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    facts = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in p["facts"])
    units = "".join(f'<div class="unit"><span class="beds">{esc(b)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p><a href="#enquire" data-intent="Buy">Floor plans &amp; prices →</a></div>' for t, b, d in p["units"])
    gal = ""
    if p["gallery"]:
        gal = '<div class="gal">' + "".join(f'<img src="{img_src(f, inline)}" alt="{esc(a)}" loading="lazy">' for f, a in p["gallery"]) + "</div>"
    split_img = f'<img src="{img_src(p["split"][0], inline)}" alt="{esc(p["split"][1])}" loading="lazy">' if p.get("split") else \
        f'<div class="unit" style="background:var(--char);color:#fff;border:0"><span class="beds">Owners &amp; buyers</span><h3 style="color:#fff">Looking for a specific phase or size?</h3><p style="color:rgba(255,255,255,.75)">Tell Mark the phase, bedrooms and budget you want. He will send the homes available now, with floor plans and payment plan.</p><a href="#enquire" data-intent="Buy" style="color:var(--gold)">Send my requirements →</a></div>'
    gal_sec = f'<section class="s" style="padding-top:0"><div class="wrap">{gal}</div></section>' if gal else ""
    svc = "".join(f"<div><b>{esc(a)}</b><p>{esc(b)}</p></div>" for a, b in SERVICES)
    creds = ""
    if p["creds"]:
        creds = '<ul class="creds">' + "".join(f"<li>{esc(c)}</li>" for c in p["creds"]) + "</ul>"
    permit = f"DLD advertising permit (Trakheesi): {esc(PERMIT)}" if PERMIT else "DLD advertising permit (Trakheesi): <b>[PERMIT NUMBER + QR TO ADD BEFORE ADS RUN]</b>"
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Inter:wght@400;600&display=swap" rel="stylesheet">') if inline else ""
    ga = "" if inline else (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>'
          f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>")
    cfg = json.dumps({"page": name, "wa": WA, "formsubmit": "" if inline else FORMSUBMIT, "sheet": "" if inline else SHEET_URL})
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p["short"] + " Landing Preview") if inline else esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#1E1D1B">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["desc"])}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{fonts}<style>{"" if inline else FONTS_LOCAL}{CSS}</style>
{ga}<script>window.LP={cfg}</script>
</head>
<body>
<header class="top"><div class="wrap">
 <a class="brand" href="#top" aria-label="Mark Darsy, Villa Specialist"><span class="mono">MD</span><span><b>Mark Darsy</b><small>Villa Specialist · BRN {BRN}</small></span></a>
 <nav class="toplinks"><a class="btn btn-line" href="tel:{TEL}">{PHONE}</a><a class="btn btn-wa" href="{wa_buy}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a></nav>
</div></header>
<main id="top">
<section class="{hero_cls}"{hero_style} role="img" aria-label="{esc(p["hero_alt"])}">
 <div class="wrap hero-grid">
  <div>
   <span class="eyebrow">{esc(p["eyebrow"])}</span>
   <h1>{p["h1"]}</h1>
   <p class="lead">{esc(PITCH)}</p>
   <div class="btns"><a class="btn btn-gold" href="#enquire" data-intent="Buy">Get brochure, floor plans &amp; prices</a><a class="btn btn-line" href="#enquire" data-intent="Sell">Free valuation for owners</a></div>
   <ul class="ticks"><li>Floor plans, prices and payment plan sent on WhatsApp</li><li>Resale and available units in {esc(short)}</li><li>Owners: free valuation and free premium listing</li></ul>
  </div>
  <div class="card" id="enquire">
   <h3>Get the {esc(short)} details</h3>
   <p class="sub">Mark replies personally on WhatsApp or by phone.</p>
   <form id="lead" novalidate>
    <label id="lb-int">I want to</label>
    <div class="seg" role="radiogroup" aria-labelledby="lb-int">
     <input type="radio" id="i-buy" name="intent" value="Buy" checked><label for="i-buy">Buy</label>
     <input type="radio" id="i-sell" name="intent" value="Sell"><label for="i-sell">Sell / Rent out</label>
     <input type="radio" id="i-re" name="intent" value="Sell &amp; reinvest"><label for="i-re">Sell &amp; reinvest</label>
    </div>
    <label for="f-name">Full name</label><input id="f-name" name="name" autocomplete="name" required>
    <div class="row">
     <div><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+971 5X XXX XXXX" required></div>
     <div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
    </div>
    <div class="row">
     <div><label for="f-type">Property type</label><select id="f-type" name="type">{opts(p["types"])}</select></div>
     <div class="buyonly"><label for="f-budget">Budget</label><select id="f-budget" name="budget">{opts(p["budgets"])}</select></div>
     <div class="sellonly" hidden><label for="f-unit">Your unit / plot no.</label><input id="f-unit" name="unit" placeholder="e.g. villa or plot number"></div>
    </div>
    <div class="buyonly"><label id="lb-want">Send me</label>
    <div class="chips" role="group" aria-labelledby="lb-want">
     <input type="checkbox" id="w1" name="want" value="Brochure" checked><label for="w1">Brochure</label>
     <input type="checkbox" id="w2" name="want" value="Floor plans" checked><label for="w2">Floor plans</label>
     <input type="checkbox" id="w3" name="want" value="Price list" checked><label for="w3">Price list</label>
     <input type="checkbox" id="w4" name="want" value="Payment plan" checked><label for="w4">Payment plan</label>
    </div></div>
    <label for="f-time">Timeline</label><select id="f-time" name="timeline"><option>Now – within 1 month</option><option>1 – 3 months</option><option>3 – 6 months</option><option>Just researching</option></select>
    <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label class="consent"><input type="checkbox" name="consent" value="yes" checked> I agree that Mark Darsy may contact me by phone, WhatsApp or email about this enquiry.</label>
    <button class="btn btn-gold" type="submit">Send it to my WhatsApp</button>
    <p class="formmsg" role="status" aria-live="polite"></p>
   </form>
  </div>
 </div>
</section>
<section class="facts" aria-label="Key facts"><div class="wrap">{facts}</div></section>

<section class="s"><div class="wrap split">
 <div><span class="eyebrow">About {esc(short)}</span><h2>{esc(p["about_h"])}</h2><p>{esc(p["about"])}</p>
  <div class="btns" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-gold" href="#enquire" data-intent="Buy">Ask for available units</a><a class="btn btn-wa" href="{wa_buy}" target="_blank" rel="noopener">{WA_ICON}WhatsApp Mark</a></div></div>
 <div>{split_img}</div>
</div></section>

<section class="s pack"><div class="wrap">
 <div class="packhead"><div><span class="eyebrow">Free on WhatsApp</span><h2>Get the full <em>{esc(short)}</em> pack.</h2></div>
 <p>Choose what you need. Mark sends it to your WhatsApp.</p></div>
 <div class="tiles">
  <a class="tile" href="#enquire" data-intent="Buy" data-want="Brochure"><b>Brochure</b><span>Developer brochure, PDF</span><i>Get brochure →</i></a>
  <a class="tile" href="#enquire" data-intent="Buy" data-want="Floor plans"><b>Floor plans</b><span>Every layout and size</span><i>Get floor plans →</i></a>
  <a class="tile" href="#enquire" data-intent="Buy" data-want="Price list"><b>Price list</b><span>Units available now</span><i>Get price list →</i></a>
  <a class="tile" href="#enquire" data-intent="Buy" data-want="Payment plan"><b>Payment plan</b><span>Remaining payments by unit</span><i>Get payment plan →</i></a>
 </div>
</div></section>
<section class="s cream"><div class="wrap">
 <span class="eyebrow">Homes</span><h2>Choose your home in <em>{esc(short)}</em>.</h2>
 <p style="max-width:40em;color:var(--char)">{esc(PITCH)}</p>
 <div class="units">{units}</div>
</div></section>
{gal_sec.replace('<section class="s" style="padding-top:0">','<section class="s">') if gal_sec else ""}
<section class="s dark"><div class="wrap center">
 <span class="eyebrow">For owners</span><h2>{esc(p["owner_h"])}<br><em>Sell, rent out or reinvest.</em></h2>
 <p class="narrow" style="color:rgba(255,255,255,.8)">Find out what your home is worth today and how fast it can sell or rent, with no cost and no obligation.</p>
 <div class="svc">{svc}</div>
 <div class="btnrow"><a class="btn btn-gold" href="#enquire" data-intent="Sell">Get my free valuation</a><a class="btn btn-wa" href="{wa_sell}" target="_blank" rel="noopener">{WA_ICON}WhatsApp Mark</a></div>
</div></section>

<section class="s"><div class="wrap">
 <div class="mark"><span class="mono">MD</span><div><span class="eyebrow">Your advisor</span><h2 style="margin-bottom:.3em">Mark Darsy, Villa Specialist</h2>
 <p style="margin:0;color:var(--char)">Dubai villa and townhouse specialist for buyers, sellers and landlords. One point of contact for viewings, offers, payment plans, NOCs and transfer. Broker registration (BRN) {BRN}.</p></div></div>
 {creds}
 <div class="btnrow" style="margin-top:30px"><a class="btn btn-gold" href="#enquire" data-intent="Buy">Get floor plans &amp; prices</a><a class="btn btn-line" href="tel:{TEL}">Call {PHONE}</a></div>
</div></section>
</main>
<footer class="foot"><div class="wrap">
 <p><b style="color:#fff">Mark Darsy, Villa Specialist</b> · BRN {BRN} · <a href="tel:{TEL}">{PHONE}</a> · <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></p>
 <p class="permit">{permit}</p>
 <p>Independent broker marketing. {name} is developed by its master developer; this page is not affiliated with or endorsed by the developer. Availability, prices, specifications, payment plans and handover dates must be verified against the selected property's documents before any decision. {esc(p["img_note"])}</p>
 <p>Your details are used only to answer your enquiry and are never sold. Reply STOP on WhatsApp at any time to opt out. <a href="https://palmjebelali-resale.com/privacy">Privacy</a></p>
 <p>© 2026 Mark Darsy</p>
</div></footer>
<nav class="cbar" aria-label="Contact Mark"><a class="btn btn-line" href="tel:{TEL}">Call Mark</a><a class="btn btn-wa" href="{wa_buy}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a></nav>
<script>{JS}</script>
</body>
</html>
"""

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        d = sys.argv[2]; os.makedirs(d, exist_ok=True)
        for p in PAGES:
            with open(os.path.join(d, f"{p['slug']}.html"), "w", encoding="utf-8") as fh: fh.write(build(p, inline=True))
            print("preview", p["slug"])
    else:
        for p in PAGES:
            dd = os.path.join(OUT, p["slug"]); os.makedirs(dd, exist_ok=True)
            with open(os.path.join(dd, "index.html"), "w", encoding="utf-8") as fh: fh.write(build(p))
            print("wrote", "/lp/" + p["slug"])
