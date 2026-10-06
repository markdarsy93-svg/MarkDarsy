#!/usr/bin/env python3
"""Static site generator for palmjebelali-resale.com"""
import json, os, html
from urllib.parse import quote

SITE = "https://palmjebelali-resale.com"
OUT = os.path.join(os.path.dirname(__file__), "site")
PHONE = "+971 58 541 4999"
TEL = "+971585414999"
WA = "https://wa.me/971585414999"
VER = "10"
ADDRESS = "Regalia Tower, 1st Floor, Business Bay, Dubai, UAE"
MAPS = "https://www.google.com/maps/search/?api=1&query=Regalia+Tower+Business+Bay+Dubai"

def wa(text): return WA + "?text=" + quote(text)
def esc(s): return html.escape(s, quote=True)

OG = {  # image: (w,h)
    "palm-jebel-ali-villa.webp": (2000, 1296),
    "palm-jebel-ali-beach-villas.webp": (2000, 1296),
    "pja-beach-villas-evening.webp": (2200, 1133),
    "palm-jebel-ali-frond-villas.webp": (2000, 1157),
    "pja-aerial-progress-overview-v1.webp": (1313, 1591),
    "pja-fronds-masterplan.webp": (2200, 1133),
}

NAV = [
    ("/dubai-property-atlas", "Property Atlas"),
    ("/beach-collection-resale", "Beach Collection"),
    ("/coral-collection-resale", "Coral Collection"),
    ("/palm-jebel-ali-position-guide", "Position Guide"),
    ("/sell-your-palm-jebel-ali-villa", "Sell"),
]

WA_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-11.8 7L4 20l1.5-4.1A8 8 0 1 1 20 11.5Z"/><path d="M9 9.5c.3 2.2 2.3 4.2 4.5 4.5l1-1.2 2 .9c-.2 1-1.2 1.8-2.3 1.7-3.5-.4-6.2-3.1-6.6-6.6-.1-1.1.7-2.1 1.7-2.3l.9 2-1.2 1Z" fill="currentColor" stroke="none"/></svg>'

LD = {
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "name": "Mark Darsy",
    "alternateName": "Palm Jebel Ali Resale",
    "url": SITE + "/",
    "image": SITE + "/images/mark-darsy-authentic-advisor-v2.webp",
    "telephone": TEL,
    "email": "mark@palmjebelali-resale.com",
    "areaServed": {"@type": "Place", "name": "Palm Jebel Ali, Dubai, United Arab Emirates"},
    "address": {"@type": "PostalAddress", "streetAddress": "Regalia Tower, 1st Floor", "addressLocality": "Business Bay, Dubai", "addressCountry": "AE"},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=Regalia+Tower+Business+Bay+Dubai",
    "knowsAbout": ["Palm Jebel Ali resale villas", "Beach Collection", "Coral Collection", "Off-plan villa resale"],
}

def head(path, title, desc, img, home=False):
    w, h = OG[img]
    url = SITE + (path if path != "/" else "/")
    t = esc(title); dsc = esc(desc)
    pre = '<link rel="preload" href="/images/palm-jebel-ali-villa.webp" as="image" fetchpriority="high">' if home else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{dsc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FBF8F2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Palm Jebel Ali Resale">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{dsc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/{img}">
<meta property="og:image:type" content="image/webp">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{dsc}">
<meta name="twitter:image" content="{SITE}/images/{img}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<link rel="stylesheet" href="/assets/site.css?v={VER}">
<script type="application/ld+json">{json.dumps(LD)}</script>
</head>'''

def header(path, home=False):
    links = "".join(
        f'<a href="{h}"{" aria-current=page" if h == path else ""}>{n}</a>' for h, n in NAV)
    cls = "hdr home" if home else "hdr"
    return f'''<body>
<a class="sr" href="#main">Skip to content</a>
<header class="{cls}">
 <div class="wrap hdr-in">
  <a class="brand" href="/" aria-label="Mark Darsy, Palm Jebel Ali Resale, home"><span class="mono">MD</span><span><b>Mark Darsy</b><small>Palm Jebel Ali Resale</small></span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="/#contact">Request shortlist</a></nav>
 </div>
</header>
<main id="main">'''

def footer(extra=""):
    return f'''</main>
<footer class="ftr">
 <div class="wrap">
  <div class="ftr-grid">
   <div>
    <a class="brand" href="/"><span class="mono">MD</span><span><b>Mark Darsy</b><small>Palm Jebel Ali resale specialist</small></span></a>
    <p style="margin-top:22px">{ADDRESS}<br><a href="{MAPS}" target="_blank" rel="noopener">Get directions</a></p>
    <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:mark@palmjebelali-resale.com">mark@palmjebelali-resale.com</a><br><a href="{WA}" target="_blank" rel="noopener">WhatsApp Mark</a></p>
   </div>
   <nav aria-label="Villas"><a href="/dubai-property-atlas">Property Atlas</a><a href="/beach-collection-resale">Beach Villas</a><a href="/coral-collection-resale">Coral Villas</a><a href="/palm-jebel-ali-position-guide">Position Guide</a></nav>
   <nav aria-label="Services"><a href="/sell-your-palm-jebel-ali-villa">Sell a Villa</a><a href="/palm-jebel-ali-resale-guide">Buyer Guide</a><a href="/#contact">Request a shortlist</a><a href="/privacy">Privacy</a></nav>
  </div>
  <p class="disc">Independent broker marketing. Availability, specifications, payment obligations and market figures must be verified against the selected property's documents before any decision. Sales figure based on Mark Darsy's transaction records. Villa and lifestyle images are developer conceptual imagery, not a specific resale villa; aerial photographs supplied by Mark Darsy. Drive times, construction and planned figures as published by <a href="https://www.nakheel.com/en/media-centre/press-releases/news-detail/2026/08/20/nakheel-unveils-limited-collection-of-44-beachfront-villas-on-palm-jebel-ali-s-frond-f" target="_blank" rel="noopener">Nakheel, 20 August 2026</a>, subject to change. Palm Jebel Ali and Nakheel names, trademarks and project imagery remain their owners' property.</p>
  <p class="disc" style="border:0;padding-top:0">© 2026 Mark Darsy</p>
 </div>
</footer>
<a class="wa" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp Mark">{WA_ICON}</a>
{extra}
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
'''

def img(name, alt, eager=False, cls=""):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="eager"'
    return f'<img src="/images/{name}" alt="{esc(alt)}" {load}{(" class=" + cls) if cls else ""}>'

def page(path, title, desc, ogimg, body, home=False, extra=""):
    return head(path, title, desc, ogimg, home) + "\n" + header(path, home) + body + footer(extra)

def write(route, content):
    d = OUT if route == "/" else os.path.join(OUT, route.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)

def opts(items, selected=None):
    return "".join(f'<option{" selected" if i == selected else ""}>{esc(i)}</option>' for i in items)

FRONDS = ["Frond " + c for c in "ABCDEFGHIJKLMNOP"]

def field(label, inner, full=False):
    return f'<div class="field{" full" if full else ""}"><label>{label}</label>{inner}</div>'

def sel(name, items, selected=None):
    return f'<select name="{name}">{opts(items, selected)}</select>'

def cta_band(title, text, msg, btn="Continue on WhatsApp", dark=True):
    return f'''<section class="{"sec-dark" if dark else "sec-cream"}"><div class="wrap narrow center reveal">
<span class="eyebrow">Private advisory</span><h2>{title}</h2><p class="lead" style="margin:0 auto">{text}</p>
<div class="btns" style="justify-content:center"><a class="btn btn-gold" href="{wa(msg)}" target="_blank" rel="noopener">{btn}</a></div></div></section>'''

def steps(items, h="h2"):
    out = ['<div class="steps">']
    for i, it in enumerate(items, 1):
        t, ptxt = it[0], it[1]
        ul = it[2] if len(it) > 2 else None
        ex = '<span class="ex">Illustrative comparison — not a live listing or completed transaction</span>' if t.startswith("Example") else ""
        lis = ("<ul>" + "".join(f"<li>{x}</li>" for x in ul) + "</ul>") if ul else ""
        out.append(f'<div class="step reveal"><span class="num">{i:02d}</span><div><{h}>{t}</{h}>{ex}<p>{ptxt}</p>{lis}</div></div>')
    out.append("</div>")
    return "".join(out)

def continue_links(links):
    a = "".join(f'<a class="btn btn-line" href="{h}">{t}</a>' for h, t in links)
    return f'<section style="padding-top:0"><div class="wrap"><span class="eyebrow">Continue your comparison</span><div class="btns" style="margin-top:0">{a}</div></div></section>'

# ---------------------------------------------------------------- data
LISTINGS = [
    # id, frond, beds, title, price, area_label, area, plot, orientation
    ("e", "E", 5, "Five-bedroom beachfront villa", 18_000_000, "Advertised area", 7565, "To confirm", "To confirm"),
    ("n", "N", 6, "Six-bedroom sunset-facing villa", 18_000_000, "Advertised BUA", 7727, "7,429 sq ft", "Sunset"),
    ("d", "D", 6, "Pacific Breeze · sunset outlook", 21_000_000, "Advertised area", 7578, "To confirm", "Sunset"),
    ("c", "C", 6, "Bluejay · high-number position", 25_000_000, "Built-up area", 8293, "7,374.46 sq ft", "Sunrise"),
    ("m", "M", 7, "Seven-bedroom beachfront residence", 49_000_000, "Advertised BUA", 11632, "To confirm", "To confirm"),
    # added 6 Oct 2026 (advertised asking prices; availability unconfirmed)
    ("p1", "P", 6, "Blue Horizon · six-bedroom villa", 25_000_000, "Built-up area", 7391, "7,390.72 sq ft", "To confirm"),
    ("l1", "L", 6, "Six-bedroom beach villa", 23_500_000, "Advertised area", 7373, "To confirm", "To confirm"),
    ("b1", "B", 6, "Six-bedroom beach villa", 19_100_000, "Built-up area", 7308, "7,373 sq ft", "To confirm"),
    ("b2", "B", 6, "Six-bedroom contemporary villa", 18_600_000, "Advertised area", 7562, "To confirm", "To confirm"),
    ("k1", "K", 7, "Seven-bedroom Coral villa", 35_908_800, "Built-up area", 11448, "13,094 sq ft", "To confirm"),
    ("k2", "K", 7, "Seven-bedroom beach mansion · large plot", 49_278_800, "Built-up area", 11448, "21,246 sq ft", "To confirm"),
    ("k3", "K", 5, "Indigo Ocean · high-number position", 21_500_000, "Advertised area", 7434, "To confirm", "To confirm"),
    ("c1", "C", 5, "Five-bedroom beach villa", 19_500_000, "Advertised area", 7569, "To confirm", "To confirm"),
    ("c2", "C", 6, "Coral Dune · high-number position", 50_000_000, "Built-up area", None, "20,775 sq ft (advertised)", "Sunset"),
    ("d1", "D", 6, "Six-bedroom villa · high number", 20_000_000, "Advertised area", 7589, "To confirm", "Sunset"),
    ("n1", "N", 6, "Six-bedroom sunset villa", 19_808_800, "Advertised area", 7374, "To confirm", "Sunset"),
    ("l2", "L", 5, "Five-bedroom beach villa", 20_698_800, "Advertised area", 7606, "To confirm", "To confirm"),
    ("l3", "L", 6, "Six-bedroom villa · sunset outlook", 18_800_000, "Built-up area", 7883, "7,427 sq ft", "Sunset"),
    ("f1", "F", 7, "Seven-bedroom beach mansion · 30/70 plan", 53_909_000, "Built-up area", None, "To confirm", "To confirm"),
    ("o1", "O", 7, "Hibiscus layout · seven-bedroom Coral villa", 32_500_000, "Built-up area", 12007, "13,087 sq ft", "To confirm"),
    ("m1", "M", 7, "Redwood · seven-bedroom Coral villa", 34_500_000, "Built-up area", 12165, "13,098 sq ft", "Sunrise"),
]
PSF = [round(l[4] / l[6]) for l in LISTINGS if l[6]]
PSF_MIN, PSF_MAX = min(PSF), max(PSF)
PRICE_MIN, PRICE_MAX = min(l[4] for l in LISTINGS), max(l[4] for l in LISTINGS)

BEACH = [("Blue Horizon", "7,307.73"), ("Pacific Breeze", "7,676.93"), ("Cyan Sky", "7,722.35"),
         ("Bluejay", "8,293.27"), ("Ocean Whisper", "8,314.91")]
BEACH_MORE = [("Cobalt", "approx. 7,800 · pending confirmation"), ("Baia Luna", None), ("Crystal Springs", None),
              ("Wave Crest", None), ("Indigo Ocean", None)]
ARCH = {"Cyan Sky": "NAGA Architects", "Wave Crest": "LW Design Group", "Ocean Whisper": "SAOTA", "Bluejay": "SAOTA", "Coral Dune": "NAGA Architects", "Sunset Mirage": "NAGA Architects", "Amber Reef": "SAOTA", "Red Aurora": "SAOTA", "Redwood": "LW Design Group", "Porcelain Roses": "LOCI Architecture"}
def arch(n): return f'<span class="small">Architect: {ARCH[n]}</span>' if n in ARCH else ''
CORAL_MORE = ["Red Aurora", "Redwood", "Porcelain Roses", "Amber Reef"]


FEATURED = [("n", "palm-jebel-ali-frond-villas.webp"), ("c", "pja-beach-villas-frontage.webp"), ("m1", "pja-beach-villas-evening.webp")]
def featured():
    out = ""
    by = {l[0]: l for l in LISTINGS}
    for lid, im in FEATURED:
        _, fr, beds, title, price, alab, area, plot, ori = by[lid]
        msg = f"Hello Mark, please confirm availability, price and remaining developer payments for this Palm Jebel Ali villa:\nFrond {fr} · {title} · {beds} bedrooms · AED {price:,}"
        out += f'''<a class="fv reveal" href="{wa(msg)}" target="_blank" rel="noopener"><div class="ph">{img(im, "Palm Jebel Ali collection imagery")}<span class="fv-tag">Frond {fr} · {beds} bedrooms</span></div>
 <div class="fv-body"><h3>{esc(title)}</h3><div class="price">AED {price:,}</div>
 <div class="fv-spec"><span>{f"{area:,} sq ft" if area else "Area to confirm"}</span><span>{"Plot " + plot if plot != "To confirm" else "Plot to confirm"}</span><span>{ori if ori != "To confirm" else "Orientation to confirm"}</span></div>
 <span class="link">Ask Mark about this villa</span></div></a>'''
    return out

# ---------------------------------------------------------------- HOME
def home():
    body = f'''
<section class="hero" aria-label="Palm Jebel Ali resale villas">
 <img class="poster" src="/images/palm-jebel-ali-villa.webp" alt="" aria-hidden="true">
 <video autoplay muted loop playsinline preload="auto" poster="/images/palm-jebel-ali-villa.webp" aria-hidden="true" tabindex="-1">
  <source src="/videos/coral-dune-hero.mp4" type="video/mp4">
 </video>
 <div class="wrap">
  <span class="eyebrow">Beach &amp; Coral Collection</span>
  <h1>Palm Jebel Ali.<em>Resale villas.</em></h1>
  <p>Palm Jebel Ali resale villas, selected for position and value.</p>
  <div class="btns"><a class="btn btn-gold" href="/dubai-property-atlas">Browse villa listings</a><a class="btn btn-light" href="/sell-your-palm-jebel-ali-villa">Sell your villa</a></div>
 </div>
</section>

<section id="advisor"><div class="wrap intro">
 <figure class="portrait reveal">{img("mark-darsy-authentic-advisor-v2.webp", "Mark Darsy, Palm Jebel Ali resale specialist")}<figcaption>Mark Darsy · Dubai</figcaption></figure>
 <div class="reveal">
  <span class="eyebrow">The service</span>
  <h2>Up to three options, <em>compared properly.</em></h2>
  <p class="lead">The shortlist is the service. You receive current pricing, frond position, orientation, plot relationship and the seller's remaining developer payments for the villas that genuinely match your brief — nothing more, nothing generic.</p>
  <div class="stats">
   <div><b>AED 200M+</b><span>Palm Jebel Ali sales advised on</span></div>
   <div><b>Direct</b><span>Acquisitions purchased directly from Nakheel</span></div>
   <div><b>VIP</b><span>Access to selected developer stock and releases</span></div>
  </div>
  <div class="btns"><a class="btn" href="#contact">Request your shortlist</a><a class="btn btn-line" href="{wa("Hello Mark, I would like to discuss Palm Jebel Ali resale villas.")}" target="_blank" rel="noopener">WhatsApp Mark</a></div>
 </div>
</div></section>

<section class="sec-cream featured"><div class="wrap">
 <div class="sec-head row reveal"><div><span class="eyebrow">Selected resale villas</span><h2>Three to <em>start with.</em></h2></div><a class="link" href="/dubai-property-atlas">View all {len(LISTINGS)} listings</a></div>
 <div class="feat">{featured()}</div>
 <p class="small feat-note">Collection imagery shown. Villa-specific plans and photographs are shared on request.</p>
</div></section>

<section><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">What decides value</span><h2>Position before floor plan.</h2>
 <p class="lead">Two villas of the same design can differ sharply in privacy, outlook and resale appeal. Every option is compared on the same four checks.</p></div>
 <div class="g4 checks">
  <div class="card reveal"><span class="num">A</span><h3>Frond &amp; side</h3><p>Frond letter, sunrise or sunset side, distance from the spine and proximity to the tip.</p></div>
  <div class="card reveal"><span class="num">B</span><h3>Outlook &amp; privacy</h3><p>Orientation, water perspective, neighbouring plots and the long-term view corridor.</p></div>
  <div class="card reveal"><span class="num">C</span><h3>Villa &amp; plot</h3><p>Design, internal layout, plot relationship, frontage and practical family use.</p></div>
  <div class="card reveal"><span class="num">D</span><h3>Payment position</h3><p>Amount paid, outstanding developer balance, instalment dates and transfer requirements.</p></div>
 </div>
 <div class="btns"><a class="btn btn-line" href="/palm-jebel-ali-position-guide">Open the Position Guide</a><a class="link" href="/palm-jebel-ali-resale-guide" style="align-self:center">Market snapshot &amp; Golden Visa</a></div>
</div></section>

<section class="sec-cream"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">The collections</span><h2>Two villa collections. <em>One shoreline.</em></h2></div>
 <div class="coll">
  <a class="reveal" href="/beach-collection-resale"><div class="ph">{img("palm-jebel-ali-beach-villas.webp", "Palm Jebel Ali Beach Collection villas on the shoreline")}</div><div class="body"><span class="tag">Beach Collection</span><h3>Beach Villas</h3><div class="meta"><span>5–6 bedrooms</span><span>approx. 7,300–8,500 sq ft</span><span>10 designs</span></div><span class="link">Compare Beach designs</span></div></a>
  <a class="reveal" href="/coral-collection-resale"><div class="ph">{img("pja-beach-villas-evening.webp", "Palm Jebel Ali Coral Collection villa at evening")}</div><div class="body"><span class="tag">Coral Collection</span><h3>Coral Villas</h3><div class="meta"><span>6–7 bedrooms</span><span>approx. 11,500–12,500 sq ft</span><span>6 designs</span></div><span class="link">Compare Coral designs</span></div></a>
 </div>
</div></section>

<section><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">Project progress</span><h2>From masterplan to <em>waterfront reality.</em></h2>
 <p class="lead">Real aerial views of Palm Jebel Ali taking shape. Nakheel states that a phased handover of the first villas is scheduled to begin in late 2026 and continue through 2027.</p></div>
 <div class="aerials">
  <figure class="reveal"><div class="ph">{img("pja-aerial-progress-overview-v2.webp", "Aerial overview of Palm Jebel Ali fronds and surrounding water")}</div><figcaption><b>The complete palm</b><span class="small">Fronds and emerging waterfront neighbourhoods.</span></figcaption></figure>
  <figure class="reveal"><div class="ph">{img("pja-aerial-progress-fronds-v2.webp", "Closer aerial view of villa rows along Palm Jebel Ali fronds")}</div><figcaption><b>Waterfront rows emerging</b><span class="small">The scale and spacing of the villa fronds.</span></figcaption></figure>
 </div>
 <div class="facts-row reveal">
  <div><b>728</b><span>villas on Fronds K–P in internal and external finishing</span></div>
  <div><b>544</b><span>villas on Fronds A–F at various construction stages</span></div>
  <div><b>AED 13bn+</b><span>in construction and infrastructure contracts awarded</span></div>
 </div>
</div></section>

<section class="sec-cream"><div class="wrap loc">
 <div class="reveal"><div class="ph map">{img("pja-connectivity-map-v2.webp", "Developer location map showing Palm Jebel Ali in relation to Dubai landmarks and airports")}</div></div>
 <div class="reveal"><span class="eyebrow">Location</span><h2>Island privacy, within reach of the city.</h2>
  <div class="times"><div><span>Bluewaters Island</span><b>23 min</b></div><div><span>DWC Airport</span><b>25 min</b></div><div><span>Mall of the Emirates</span><b>27 min</b></div><div><span>Palm Jumeirah</span><b>28 min</b></div><div><span>Burj Al Arab</span><b>30 min</b></div><div><span>DXB Airport</span><b>40 min</b></div></div>
  <div class="facts"><div><b>7</b><span>islands planned</span></div><div><b>120 km</b><span>planned coastline</span></div><div><b>90+ km</b><span>planned beachfront</span></div></div>
 </div>
</div></section>

<section style="padding:0"><div class="strip">
 <div class="ph">{img("palm-jebel-ali-frond-villas.webp", "Villa-lined fronds on Palm Jebel Ali")}</div>
 <div class="ph">{img("pja-beach-villas-frontage.webp", "Contemporary villas opening towards the beach")}</div>
 <div class="ph">{img("palm-jebel-ali-beach-villas.webp", "Beachfront villas on Palm Jebel Ali")}</div>
 <div class="ph">{img("pja-beach-villas-evening.webp", "Palm Jebel Ali villa at evening")}</div>
</div></section>

<section class="sec-dark"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">From brief to transfer</span><h2>A clear, protected transaction.</h2></div>
 <div class="process reveal">
  <div><span class="num">I</span><h3>Private consultation</h3><p>Position, budget, payment preference and non-negotiables.</p></div>
  <div><span class="num">II</span><h3>Curated shortlist</h3><p>Up to three suitable villas, including discreet stock when available.</p></div>
  <div><span class="num">III</span><h3>Evaluate &amp; view</h3><p>Documents, position and payment structure compared side by side.</p></div>
  <div><span class="num">IV</span><h3>Convey &amp; transfer</h3><p>NOC, document checks and trustee-office appointment coordinated to completion.</p></div>
 </div>
</div></section>

<section class="sec-cream"><div class="wrap g2" style="align-items:center">
 <div class="reveal"><span class="eyebrow">For owners</span><h2>Selling a Palm Jebel Ali villa?</h2></div>
 <div class="reveal"><p class="lead">A confidential resale review, property-specific positioning for serious buyers and coordinated support through transfer.</p><div class="btns"><a class="btn" href="/sell-your-palm-jebel-ali-villa">Request a confidential review</a></div></div>
</div></section>

<section id="contact"><div class="wrap contact">
 <div class="reveal"><span class="eyebrow">Your shortlist</span><h2>Build your private shortlist.</h2>
  <p class="lead">Three details are enough. WhatsApp opens with your brief — press Send to share it with Mark.</p>
  <div class="direct"><span class="small">Direct WhatsApp</span><a href="{WA}" target="_blank" rel="noopener">{PHONE}</a></div>
  <div class="direct"><span class="small">Email</span><p style="margin:6px 0 18px;font:500 22px/1.35 var(--serif)"><a href="mailto:mark@palmjebelali-resale.com" style="font:inherit;display:inline;margin:0">mark@palmjebelali-resale.com</a></p></div>
  <div class="direct"><span class="small">Office</span><p style="margin:6px 0 4px;font:500 22px/1.35 var(--serif)">Regalia Tower, 1st Floor<br>Business Bay, Dubai, UAE</p><a class="link" href="{MAPS}" target="_blank" rel="noopener" style="font:600 13px var(--sans);display:inline-block;margin:6px 0 0">Get directions</a></div>
  <div class="btns" style="margin-top:26px"><a class="btn btn-line" href="tel:{TEL}">Call Mark</a></div>
 </div>
 <form class="form reveal" data-wa="Hello Mark, here is my Palm Jebel Ali brief:">
  {field("Your name", '<input name="name" autocomplete="name" required>')}
  {field("Phone number", '<input name="phone" type="tel" autocomplete="tel" inputmode="tel">')}
  {field("I am looking to", sel("goal", ["Buy a villa", "Sell my villa", "Evaluate an opportunity", "Invest"]), True)}
  <details class="more full"><summary>Add preferences <span>optional</span></summary><div class="form">
  {field("Collection", sel("coll", ["Beach or Coral — open", "Beach Collection", "Coral Collection"]))}
  {field("Preferred frond", sel("frond", ["Flexible"] + FRONDS + ["Not sure"]))}
  {field("Orientation", sel("ori", ["Flexible", "Sunrise", "Sunset", "Not sure"]))}
  {field("Bedrooms", sel("beds", ["Flexible", "5 bedrooms", "6 bedrooms", "7 bedrooms"]))}
  {field("Budget", sel("budget", ["To discuss", "Below AED 20M", "AED 20M–25M", "AED 25M–30M", "AED 30M–40M", "AED 40M–50M", "AED 50M+"]))}
  {field("Seller payment position", sel("paid", ["Flexible", "40% paid", "60% paid", "80% paid", "Not sure"]))}
  {field("Timing", sel("timing", ["Exploring options", "Within 1 month", "1–3 months", "3–6 months"]))}
  {field("Comments", '<textarea name="notes" placeholder="Anything else Mark should know"></textarea>', True)}
  </div></details>
  <div class="full"><button class="btn btn-gold" type="submit" style="width:100%">Prepare my WhatsApp brief</button></div>
 </form>
</div></section>
'''
    return page("/", "Palm Jebel Ali Resale Villas | Mark Darsy",
                "Palm Jebel Ali resale villas compared by frond, orientation, plot, outlook and remaining developer payments. A private shortlist of up to three options with Mark Darsy.",
                "palm-jebel-ali-villa.webp", body, home=True)

# ---------------------------------------------------------------- BEACH
def beach():
    cards = ""
    for i, (n, a) in enumerate(BEACH, 1):
        cards += f'<article class="design reveal" id="{n.lower().replace(" ", "-")}"><span class="num">{i:02d}</span><h3>{n}</h3><span class="small">6 bedrooms · Beach Collection</span>{arch(n)}<div class="area">{a} sq ft</div><span class="small">Indicative built-up area</span><a class="btn btn-line" href="{wa(f"Hello Mark, please send me current {n} resale opportunities on Palm Jebel Ali with price and payment position.")}" target="_blank" rel="noopener">Ask Mark about {n}</a></article>'
    more = ""
    for j, (n, a) in enumerate(BEACH_MORE, len(BEACH) + 1):
        area = f'<div class="area tbc">{a} sq ft</div>' if a else '<div class="area tbc">Area to confirm</div>'
        more += f'<article class="design reveal" id="{n.lower().replace(" ", "-")}"><span class="num">{j:02d}</span><h3>{n}</h3><span class="small">Beach Collection</span>{arch(n)}{area}<a class="btn btn-line" href="{wa(f"Hello Mark, please send me the {n} floor plan and any current resale opportunities.")}" target="_blank" rel="noopener">Ask Mark about {n}</a></article>'
    body = f'''
<section class="phero"><div class="wrap phero-grid">
 <div class="reveal"><span class="eyebrow">Palm Jebel Ali · Beach Collection</span><h1>Beach villas selected beyond the floor plan.</h1>
  <p class="lead">Compare each opportunity by design, position, orientation, plot relationship and the seller's remaining payment obligations — not the floor plan alone.</p>
  <div class="btns"><a class="btn btn-gold" href="{wa("Hello Mark, please send me a private shortlist of Palm Jebel Ali Beach Collection resale villas with current pricing and payment positions.")}" target="_blank" rel="noopener">Request current options</a><a class="btn btn-line" href="/dubai-property-atlas">See villa listings</a></div></div>
 <figure class="reveal">{img("palm-jebel-ali-beach-villas.webp", "Palm Jebel Ali Beach Collection villa facing the shoreline", eager=True)}</figure>
</div></section>

<section class="sec-cream" id="designs"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">The designs</span><h2>Ten Beach designs, ordered by size.</h2>
 <p class="lead">Approx. 7,300–8,500 sq ft across five- and six-bedroom designs. Areas are indicative collection references; different releases may use revised plans.</p></div>
 <div class="designs">{cards}{more}</div>
 <p class="note">Confirm bedrooms, layout and exact area against the selected villa's SPA and developer floor plan before making an offer. Developer reference: <a href="https://www.nakheel.com/en/media-centre/press-releases/news-detail/2025/05/06/on-palm-jebel-ali--the-beach-collection-is-set-to-take-luxury-coastal-living-to-new-heights" target="_blank" rel="noopener">Nakheel, Beach Collection, 6 May 2025</a>.</p>
</div></section>

<section><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">How to compare</span><h2>From design name to a sound decision.</h2></div>
 {steps([
   ("Start with the exact design and release", "A design name is not a complete specification. Identify the villa number and release, then match the floor plan, documented built-up area, plot area and façade.", ["Bedrooms, circulation and family space", "Pool, garden and shoreline relationship", "Documented area rather than rounded marketing figures"]),
   ("Compare two villas on the same framework", "Separate what is documented, what the seller reports and what still needs checking. A lower headline price is then assessed, not assumed to be better value.", ["Frond, orientation and position along the frond", "Plot relationship, outlook and neighbouring terraces", "Seller price, paid amount, outstanding balance and instalment dates"]),
   ("Example: same design, different position", "Two villas share a design, but one sits closer to the spine and the other closer to the tip. A buyer prioritising daily access may prefer the first; one seeking a particular outlook may investigate the second. Neither position establishes a premium without plot evidence and comparable pricing."),
   ("Example: price and cash timing are different questions", "Two seller prices look similar, yet the villas have different amounts paid and different next instalment dates. Compare the amount payable at transfer, outstanding developer obligations and transaction costs separately."),
   ("Turn the comparison into a current shortlist", "Share your budget, frond and orientation preferences, timing and payment-position preference. Mark returns up to three suitable options with the relevant details for each."),
 ])}
</div></section>
{continue_links([("/palm-jebel-ali-position-guide", "Compare frond and position"), ("/coral-collection-resale", "Explore Coral Villas"), ("/palm-jebel-ali-resale-guide", "Understand the resale process")])}
{cta_band("Compare the strongest Beach Villa opportunities.", "Share your budget, preferred position and timing. You receive a focused shortlist — not a generic property list.", "Hello Mark, please send me a private shortlist of Palm Jebel Ali Beach Collection resale villas with current pricing and payment positions.")}
'''
    return page("/beach-collection-resale", "Palm Jebel Ali Beach Villas Resale | Mark Darsy",
                "Compare Palm Jebel Ali Beach Collection resale villas — ten designs from approx. 7,300 to 8,500 sq ft — by frond position, orientation and developer payment obligations.",
                "palm-jebel-ali-beach-villas.webp", body)

# ---------------------------------------------------------------- CORAL
def coral():
    wide = ""
    for i, (slug, n, a, im) in enumerate([("coral-dune", "Coral Dune", "11,635.14", "coral-dune-floorplan.jpg"),
                                           ("sunset-mirage", "Sunset Mirage", "11,701.12", "sunset-mirage-floorplan.jpg")], 1):
        wide += f'''<article class="design wide reveal" id="{slug}"><div><span class="num">{i:02d}</span><h3>{n}</h3><span class="small">6 bedrooms · Coral Collection</span>{arch(n)}<div class="area">{a} sq ft</div><span class="small">Brochure built-up area · indicative developer plan</span><br><a class="btn btn-line" href="{wa(f"Hello Mark, please send me current {n} resale opportunities on Palm Jebel Ali with price and payment position.")}" target="_blank" rel="noopener">Ask Mark about {n}</a></div><figure>{img(im, f"{n} indicative developer floor plan showing floors and area schedule")}</figure></article>'''
    more = ""
    for j, n in enumerate(CORAL_MORE, 3):
        more += f'<article class="design reveal" id="{n.lower().replace(" ", "-")}"><span class="num">{j:02d}</span><h3>{n}</h3><span class="small">Coral Collection</span>{arch(n)}<div class="area tbc">Area to confirm</div><a class="btn btn-line" href="{wa(f"Hello Mark, please send me the {n} floor plan and any current resale opportunities.")}" target="_blank" rel="noopener">Ask Mark about {n}</a></article>'
    body = f'''
<section class="phero"><div class="wrap phero-grid">
 <div class="reveal"><span class="eyebrow">Palm Jebel Ali · Coral Collection</span><h1>Grand-scale waterfront villas, evaluated individually.</h1>
  <p class="lead">Palm Jebel Ali's larger coastal residences. The right purchase depends on the exact design, documented area, frond position, outlook and payment structure.</p>
  <div class="btns"><a class="btn btn-gold" href="{wa("Hello Mark, please send me the current Palm Jebel Ali Coral Collection resale opportunities and floor plans.")}" target="_blank" rel="noopener">Request current options</a><a class="btn btn-line" href="/dubai-property-atlas">See villa listings</a></div></div>
 <figure class="reveal">{img("pja-beach-villas-evening.webp", "Large Palm Jebel Ali waterfront villa at sunset", eager=True)}</figure>
</div></section>

<section class="sec-cream" id="designs"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">The designs</span><h2>Six Coral designs at a glance.</h2>
 <p class="lead">Approx. 11,500–12,500 sq ft. Published releases include six- and seven-bedroom Coral designs; confirm the size and bedroom count of the specific resale villa.</p></div>
 <div class="designs">{wide}{more}</div>
 <p class="note">Plans are indicative; final dimensions, orientation, materials and specifications are governed by the individual SPA. Architects as named by Nakheel for the latest release. Developer reference: <a href="https://www.nakheel.com/en/media-centre/press-releases/news-detail/2026/08/20/four-studios--one-shoreline--inside-the-latest-release-from-palm-jebel-ali-s-beach---coral-collections" target="_blank" rel="noopener">Nakheel, Beach &amp; Coral release, 20 August 2026</a>.</p>
</div></section>

<section><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">How to compare</span><h2>At this scale, the plot matters as much as the house.</h2></div>
 {steps([
   ("Confirm the individual specification", "Coral design names describe a collection, not an interchangeable product. Identify the release and exact villa, then check bedrooms, built-up area, plot dimensions, façade and floor plan against the documents.", ["Official floor plan and villa reference", "Documented built-up and plot areas", "Layout and bedroom relationships"]),
   ("Look beyond total square footage", "Compare the width of the plot facing the shoreline, garden and pool arrangement, usable outdoor space and how principal rooms open towards the water."),
   ("Assess privacy and the view corridor", "Review side setbacks, adjacent villa layouts, facing windows and terraces. Study the outlook against the current masterplan and site evidence rather than assuming a render guarantees a view.", ["Separation from neighbouring villas", "Shoreline frontage and beach relationship", "Visible and planned elements within the outlook"]),
   ("Example: similar scale, different usability", "Two Coral villas have similar built-up areas but different plot proportions and neighbouring terraces. One may suit large-scale entertaining; the other may need a closer privacy review."),
   ("Price the complete acquisition commitment", "Review the agreed seller price, amount already paid, outstanding balance and dated instalment schedule together with transaction costs. Verify seller authority and transfer requirements before committing."),
   ("Source opportunities with a clear brief", "Availability is confirmed villa by villa, including opportunities shared privately with owner permission when available. An introduction to a collection is not a promise of current inventory."),
 ])}
</div></section>
{continue_links([("/palm-jebel-ali-position-guide", "Evaluate plot and position"), ("/beach-collection-resale", "Compare Beach Villas"), ("/palm-jebel-ali-resale-guide", "Review the resale process")])}
{cta_band("Build a private Coral Villa comparison.", "A focused comparison of current opportunities based on position, documentation and payment obligations.", "Hello Mark, please send me the current Palm Jebel Ali Coral Collection resale opportunities and floor plans.")}
'''
    return page("/coral-collection-resale", "Palm Jebel Ali Coral Villas Resale | Mark Darsy",
                "Palm Jebel Ali Coral Collection resale villas, approx. 11,500–12,500 sq ft — compare Coral Dune, Sunset Mirage and other designs by scale, position, layout and payment obligations.",
                "pja-beach-villas-evening.webp", body)

# ---------------------------------------------------------------- ATLAS
FRONDS_LISTED = sorted({l[1] for l in LISTINGS})
PINS = {"C": (60.5, 37), "D": (63.5, 44), "E": (66, 51), "M": (39, 52), "N": (37, 45)}

def atlas():
    cards = ""
    for lid, fr, beds, title, price, alab, area, plot, ori in LISTINGS:
        psf = round(price / area) if area else None
        area_txt = f"{area:,} sq ft" if area else "To confirm"
        psf_txt = f"Asking price · approx. AED {psf:,} per sq ft" if psf else "Asking price · area to confirm"
        summary = f"Frond {fr} · {title} · {beds} bedrooms · AED {price:,}"
        cards += f'''<article class="lst" data-id="{lid}" data-frond="{fr}" data-beds="{beds}" data-price="{price}" data-summary="{esc(summary)}">
 <div class="lst-top"><span>Frond {fr}</span><span>{beds} bedrooms</span></div>
 <div class="lst-body"><span class="tag">Off-plan resale</span><h3>{esc(title)}</h3>
 <div class="price">AED {price:,}</div><div class="price-sub">{psf_txt}</div>
 <div class="spec"><div><span>{alab}</span>{area_txt}</div><div><span>Plot</span>{plot}</div><div><span>Orientation</span>{ori}</div><div><span>Developer payments</span>Statement required</div></div>
 <a class="tel" href="tel:{TEL}">Mark Darsy · <b>{PHONE}</b></a>
 <div class="acts"><a class="btn ask" href="{WA}" target="_blank" rel="noopener">Ask Mark about this villa</a><button class="btn btn-line add" type="button" aria-pressed="false">Add to shortlist</button></div></div>
</article>'''
    pins = ""
    chips = "".join(f'<li>Frond {f} · {sum(1 for l in LISTINGS if l[1]==f)} listed</li>' for f in FRONDS_LISTED)
    body = f'''
<section class="phero" style="padding-bottom:30px"><div class="wrap">
 <span class="eyebrow">Property Atlas · Palm Jebel Ali only</span>
 <h1>Palm Jebel Ali villa listings.</h1>
 <p class="lead">Filter by bedrooms and frond, sort by price and shortlist villas. Send your shortlist to Mark to confirm availability, plot and remaining developer payments.</p>
</div></section>

<section id="listings" style="padding-top:20px"><div class="wrap">
 <div class="filters">
  <div class="field"><label for="f-beds">Bedrooms</label><select id="f-beds"><option value="all">All</option><option value="5">5 bedrooms</option><option value="6">6 bedrooms</option><option value="7">7 bedrooms</option></select></div>
  <div class="field"><label for="f-frond">Frond</label><select id="f-frond"><option value="all">All</option>{"".join(f'<option value="{f}">Frond {f}</option>' for f in FRONDS_LISTED)}</select></div>
  <div class="field"><label for="f-sort">Price</label><select id="f-sort"><option value="asc">Lowest first</option><option value="desc">Highest first</option></select></div>
  <span class="count" id="f-count" aria-live="polite"></span>
 </div>
 <div class="listings" id="listings-grid">{cards}</div>
 <p class="note">Asking prices, areas and availability are subject to confirmation. Price per sq ft is the asking price divided by the stated area, not a valuation.</p>
</div></section>

<section class="sec-cream"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">Where they sit</span><h2>The listed fronds on the island plan.</h2></div>
 <ul class="names reveal" style="justify-content:center;margin-bottom:28px">{chips}</ul>
 <div class="mp reveal">{img("pja-fronds-masterplan.webp", "Palm Jebel Ali conceptual frond masterplan")}{pins}</div>
 <p class="note center">Developer's conceptual masterplan. Exact villa positions, orientation and outlook require the individual plot plan.</p>
</div></section>

<section id="estimator"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">Plan your commitment</span><h2>Purchase costs &amp; remaining payments.</h2>
 <p class="lead">Estimate the main costs on a quoted price. Off-plan assignments need a separate transaction breakdown from the developer statement.</p></div>
 <div class="calc" id="calc">
  <div class="form" style="align-content:start">
   {field('Agreed / quoted price (AED)', '<input id="c-price" inputmode="numeric" placeholder="e.g. 21,000,000">', True)}
   {field('DLD fee allocation', '<select id="c-dld"><option value="4">4% — buyer bears full fee</option><option value="2">2% — buyer share only</option></select>')}
   {field('Agreed brokerage (%)', '<input id="c-brk" inputmode="decimal" value="2">')}
   {field('Other quoted costs (AED)', '<input id="c-oth" inputmode="numeric" placeholder="NOC, legal, bank…">', True)}
   <p class="small full">DLD states 2% seller + 2% buyer; allocation depends on your agreement (<a href="https://dubailand.gov.ae/en/eservices/property-sale-registration/" target="_blank" rel="noopener">DLD source</a>). VAT estimated at 5% on brokerage. Includes an AED 520 title allowance. Mortgage, NOC and assignment-specific charges are excluded unless entered.</p>
  </div>
  <div class="calc-out">
   <dl><div><dt>Price</dt><dd id="o-price"></dd></div><div><dt>DLD transfer fee</dt><dd id="o-dld"></dd></div><div><dt>Brokerage</dt><dd id="o-brk"></dd></div><div><dt>VAT on brokerage</dt><dd id="o-vat"></dd></div><div><dt>Title allowance</dt><dd id="o-title"></dd></div><div><dt>Other costs</dt><dd id="o-oth"></dd></div><div class="tot"><dt>Estimated total</dt><dd id="o-tot"></dd></div></dl>
   <h3 style="margin-top:30px;font-size:24px">Developer balance illustration</h3>
   <div class="form">{field('Original contract price (AED)', '<input id="b-price" inputmode="numeric">')}{field('Percentage paid', '<select id="b-paid"><option>20</option><option selected>40</option><option>60</option><option>80</option><option>100</option></select>')}</div>
   <dl style="margin-top:12px"><div><dt>Paid to developer</dt><dd id="o-paid"></dd></div><div><dt>Remaining developer balance</dt><dd id="o-bal"></dd></div></dl>
   <p class="small" style="margin-top:12px">Illustration only — request the developer statement and dated payment schedule for the exact villa.</p>
  </div>
 </div>
</div></section>

<section class="sec-dark"><div class="wrap g2" style="align-items:center">
 <div class="reveal"><span class="eyebrow">Two villas in mind?</span><h2>Compare the positions side by side.</h2><p class="lead">Frond, orientation, position along the frond, outlook, neighbours and payment status — in one structured comparison.</p><div class="btns"><a class="btn btn-gold" href="/palm-jebel-ali-position-guide#compare-positions">Open the comparison tool</a></div></div>
 <div class="advisor reveal">{img("mark-darsy-authentic-advisor-v2.webp", "Mark Darsy, Palm Jebel Ali resale specialist")}<div><span class="eyebrow">Your advisor</span><h3>Mark Darsy</h3><p>Palm Jebel Ali resale specialist · AED 200M+ in Palm Jebel Ali sales.</p><p class="small">Regalia Tower, 1st Floor, Business Bay, Dubai · <a href="{MAPS}" target="_blank" rel="noopener" style="color:var(--gold-lt)">Directions</a></p><p><a href="tel:{TEL}" style="font:500 26px var(--serif);text-decoration:none;color:var(--on-dark)">{PHONE}</a></p><a class="link" href="{wa("Hello Mark, please advise on my Palm Jebel Ali villa shortlist and payment obligations.")}" target="_blank" rel="noopener">WhatsApp Mark</a></div></div>
</div></section>
'''
    bar = f'''<div class="shortbar" role="region" aria-label="Your shortlist"><div class="wrap"><div><b>Your shortlist</b><span id="bar-n">0 villas selected</span></div><button class="btn btn-gold" id="bar-send" type="button">Send to Mark</button></div></div>'''
    return page("/dubai-property-atlas", "Palm Jebel Ali Villa Listings | Mark Darsy",
                "Palm Jebel Ali villas for resale by frond, bedrooms and asking price. Shortlist villas, estimate purchase costs and confirm remaining developer payments with Mark Darsy.",
                "palm-jebel-ali-villa.webp", body, extra=bar)

# ---------------------------------------------------------------- POSITION GUIDE
def position():
    nv = "Not verified"
    def opt(o):
        return f'''<fieldset><legend>Option {o[-1]}</legend>
 {field("Villa reference (optional)", f'<input name="{o}-ref">')}
 {field("Frond", sel(f"{o}-frond", [nv] + FRONDS))}
 {field("Orientation", sel(f"{o}-ori", [nv, "Sunrise", "Sunset"]))}
 {field("Position along frond", sel(f"{o}-pos", [nv, "Closer to spine", "Mid-frond", "Closer to tip"]))}
 {field("Outlook", sel(f"{o}-out", [nv, "Open-water outlook", "Water towards neighbouring frond", "Other outlook"]))}
 {field("Neighbour relationship", sel(f"{o}-nb", [nv, "Separation reviewed", "Needs closer review"]))}
 {field("Developer amount paid", sel(f"{o}-paid", [nv, "40%", "60%", "80%", "Other — confirm documents"]))}
</fieldset>'''
    body = f'''
<section class="phero"><div class="wrap phero-grid">
 <div class="reveal"><span class="eyebrow">Palm Jebel Ali buying intelligence</span><h1>The villa is only half the decision.</h1>
  <p class="lead">Two villas with the same design can offer different privacy, outlook, access and resale appeal. Compare the individual position — not an unsupported frond ranking.</p>
  <div class="btns"><a class="btn btn-gold" href="#compare-positions">Compare two positions</a></div></div>
 <figure class="reveal">{img("pja-fronds-masterplan.webp", "Palm Jebel Ali conceptual masterplan showing villa fronds", eager=True)}</figure>
</div></section>

<section class="sec-cream" id="compare-positions"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">Position comparison</span><h2>Put two opportunities side by side.</h2>
 <p class="lead">Enter what you know. Unverified details stay visible instead of becoming assumptions. This is a starting brief, not a valuation.</p></div>
 <div id="cmp">
  <div class="form" style="margin-bottom:20px;max-width:420px">{field("What matters most?", '<select id="cmp-pri"><option>Balanced comparison</option><option>Privacy</option><option>Outlook</option><option>Daily access</option><option>Cash and instalment timing</option></select>', True)}</div>
  <div class="cmp">{opt("o1")}{opt("o2")}</div>
  <div class="cmp-res"><div class="table-wrap"><table><thead><tr><th>Comparison</th><th>Option 1</th><th>Option 2</th></tr></thead><tbody id="cmp-body"></tbody></table></div>
   <p class="small" id="cmp-todo" style="margin-top:16px"></p>
   <button class="btn btn-gold" id="cmp-send" type="button">Discuss these positions with Mark</button></div>
 </div>
</div></section>

<section><div class="wrap">
 {steps([
   ("Why identical designs deserve different evaluations", "A floor plan explains the house. It does not explain the neighbour relationship, daily access, orientation or outlook of its plot. Start with your priorities, then assess the evidence for each villa rather than ranking an entire frond."),
   ("Four position variables to check", "Use the same questions for every option so comparisons stay consistent.", ["Frond and access: where the plot sits and how it connects to the spine", "Side and orientation: the actual compass orientation of main rooms, garden and pool", "Position along the frond: closer to the spine, mid-frond or closer to the tip", "Plot, neighbours and outlook: separation, shoreline relationship and view corridor"]),
   ("How the variables interact", "No single feature settles the choice. A position nearer the tip may mean a longer drive along the frond, while orientation changes how the garden and pool suit your routine. A promising outlook still needs a review of nearby plots."),
   ("Example: access versus outlook", "Option 1 is closer to the spine with a documented sunset orientation. Option 2 is closer to the tip, but its neighbouring terraces and exact outlook still need review. A daily-access priority favours investigating Option 1 first; an outlook priority calls for more evidence on Option 2 — it does not establish that Option 2 is worth more."),
   ("How this becomes your shortlist", "Budget, use, timing and non-negotiables come first. Suitable villas are then compared by unit identity, layout and plot information, and up to three options are presented with the differences that matter and the checks still outstanding.", ["Confirm the property reference and documents", "Compare position and usable layout together", "Record missing evidence and obtain clarification", "Review payment and transfer structure alongside the villa"]),
   ("Add the transaction overlay", "A favourable position still needs a clear acquisition structure: seller price, paid amount, outstanding developer balance, future instalments and transfer requirements."),
 ])}
</div></section>
{continue_links([("/beach-collection-resale", "Apply to Beach Villas"), ("/coral-collection-resale", "Apply to Coral Villas"), ("/dubai-property-atlas", "See current listings")])}
{cta_band("Request a plot-level evaluation.", "Share the villa or your shortlist. Mark compares position, orientation and payment information before you proceed.", "Hello Mark, I would like a Palm Jebel Ali frond and position evaluation for a villa I am considering.")}
'''
    return page("/palm-jebel-ali-position-guide", "Palm Jebel Ali Frond & Position Guide | Mark Darsy",
                "How frond, orientation, position along the frond, outlook, neighbouring plots and payment obligations affect a Palm Jebel Ali villa decision — with a two-villa comparison tool.",
                "pja-fronds-masterplan.webp", body)

# ---------------------------------------------------------------- SELL
def sell():
    body = f'''
<section class="phero"><div class="wrap phero-grid">
 <div class="reveal"><span class="eyebrow">For Palm Jebel Ali owners</span><h1>Give buyers a reason to choose your villa.</h1>
  <p class="lead">Similar listings make villas hard to tell apart. Clear documentation and property-specific positioning help qualified buyers understand your villa's value.</p>
  <div class="btns"><a class="btn btn-gold" href="#seller-enquiry">Request a resale review</a><a class="btn btn-line" href="tel:{TEL}">Call Mark</a></div></div>
 <figure class="reveal">{img("palm-jebel-ali-frond-villas.webp", "Palm Jebel Ali villas positioned along a waterfront frond", eager=True)}</figure>
</div></section>

<section class="sec-cream" id="seller-enquiry"><div class="wrap contact">
 <div class="reveal"><span class="eyebrow">Confidential seller enquiry</span><h2>Start with your villa's details.</h2>
  <p class="lead">Choose “Not sure” when a detail needs checking. WhatsApp opens with your brief — press Send to share it privately with Mark.</p>
  <div class="direct"><span class="small">Speak with Mark directly</span><a href="{wa("Hello Mark, I own a Palm Jebel Ali villa and would like a confidential resale review.")}" target="_blank" rel="noopener">{PHONE}</a></div></div>
 <form class="form reveal" data-wa="Hello Mark, I own a Palm Jebel Ali villa and would like a confidential resale review:">
  {field("Your name", '<input name="name" autocomplete="name" required>')}
  {field("Phone number", '<input name="phone" type="tel" autocomplete="tel">')}
  {field("Villa collection", sel("coll", ["Not sure", "Beach Collection", "Coral Collection"]))}
  {field("Frond", sel("frond", ["Not sure"] + FRONDS))}
  {field("Orientation", sel("ori", ["Not sure", "Sunrise", "Sunset"]))}
  {field("Developer amount paid", sel("paid", ["Not sure", "40%", "60%", "80%", "Other — see details"]))}
  {field("Asking price band", sel("price", ["To discuss", "Below AED 20M", "AED 20M–25M", "AED 25M–30M", "AED 30M–40M", "AED 40M–50M", "AED 50M+"]))}
  {field("Preferred sale timing", sel("timing", ["Exploring options", "Within 1 month", "1–3 months", "3–6 months"]))}
  {field("Villa details", '<textarea name="notes" placeholder="Design, villa number if comfortable, anything buyers should know"></textarea>', True)}
  <div class="full"><button class="btn btn-gold" type="submit" style="width:100%">Prepare my seller enquiry</button><p class="small" style="margin-top:12px">This starts a private discussion. Marketing channels and any appointment are agreed separately.</p></div>
 </form>
</div></section>

<section><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">How your sale is handled</span><h2>Positioned for serious buyers.</h2></div>
 {steps([
   ("Confidential resale review", "Review of the SPA, payment plan, unit details, plot relationship and the comparable evidence available — a practical positioning opinion, not an automated estimate."),
   ("Property-specific presentation", "The exact design, area, orientation, frond position, view relationship and payment status, with verified facts kept separate from developer renders."),
   ("Controlled buyer communication", "Presentation through agreed channels, answers to material buyer questions and clear feedback on genuine interest."),
   ("Negotiation and coordinated transfer", "Support through negotiation and the agreed transaction process, including documents, NOC steps and trustee-office arrangements."),
 ])}
</div></section>
{continue_links([("/palm-jebel-ali-position-guide", "Understand your villa's position"), ("/dubai-property-atlas", "See current asking prices")])}
'''
    return page("/sell-your-palm-jebel-ali-villa", "Sell Your Palm Jebel Ali Villa | Mark Darsy",
                "Confidential Palm Jebel Ali resale guidance for owners: document review, pricing context, property-specific positioning and coordinated transfer support.",
                "palm-jebel-ali-frond-villas.webp", body)

# ---------------------------------------------------------------- GUIDE
def guide():
    psf_note = f"AED {PSF_MIN:,}–{PSF_MAX:,}"
    body = f'''
<section class="phero"><div class="wrap phero-grid">
 <div class="reveal"><span class="eyebrow">Palm Jebel Ali resale guide</span><h1>Understand the property, payment and process.</h1>
  <p class="lead">A resale decision combines the villa itself with the seller's contract and payment position. These are the checks to complete before an offer.</p>
  <div class="btns"><a class="btn btn-gold" href="{wa("Hello Mark, I would like you to review a Palm Jebel Ali resale opportunity and its payment position.")}" target="_blank" rel="noopener">Review an opportunity</a></div></div>
 <figure class="reveal">{img("pja-aerial-progress-overview-v2.webp", "Aerial project view of Palm Jebel Ali fronds", eager=True)}</figure>
</div></section>
<section style="padding-top:20px"><div class="wrap">
 {steps([
   ("Match the exact property", "Confirm the unit and plot identity, design, bedrooms, documented areas, frond position and supporting developer documents. Do not rely only on portal descriptions or generic floor plans."),
   ("Review the seller's position", "Understand how much has been paid, what remains outstanding, when future instalments fall due and whether current transfer conditions are satisfied."),
   ("Compare total acquisition commitments", "Review the asking price, seller premium, outstanding developer balance, registration and transfer costs together, so your immediate cash requirement and future obligations are clear before negotiation."),
   ("Verify authority and current requirements", "Check the seller's authority and supporting documents, then confirm current developer, NOC and Dubai Land Department requirements for the transaction."),
   ("Coordinate the transfer", "Once terms are agreed, the conveyance process coordinates documents, NOC requirements and the trustee-office transfer. Scope and sequence depend on the transaction and current official requirements."),
 ])}
 <div class="btns"><a class="btn btn-line" href="/dubai-property-atlas#estimator">Estimate purchase costs</a><a class="btn btn-line" href="/palm-jebel-ali-position-guide">Compare positions</a></div>
</div></section>
<section class="sec-dark" id="investors"><div class="wrap">
 <div class="sec-head reveal"><span class="eyebrow">Investor snapshot</span><h2>What the current resale market is asking.</h2>
 <p class="lead">Figures below are calculated from the villas currently presented in the Property Atlas. They describe advertised asking prices, not valuations or achieved sales.</p></div>
 <div class="kpis reveal">
  <div><b>{psf_note}</b><span>Asking price per sq ft across current listings (advertised price ÷ advertised area)</span></div>
  <div><b>AED {PRICE_MIN/1e6:.0f}M–{PRICE_MAX/1e6:.0f}M</b><span>Asking price range · 5 to 7 bedrooms</span></div>
  <div><b>40–80%</b><span>Typical seller payment positions to compare — the remaining balance follows the developer schedule</span></div>
 </div>
 <div class="g2 reveal">
  <div><h3>How off-plan resale works</h3><p>On a resale of an under-construction villa, the seller has already paid part of the developer price. You pay the agreed seller price at transfer and take over the remaining instalments. Two villas with similar headline prices can require very different cash today — so the amount payable at transfer and the future developer obligations are compared separately.</p><a class="link" href="/dubai-property-atlas#estimator">Estimate purchase costs</a></div>
  <div><h3>Two waterfront markets</h3><div class="table-wrap"><table>
   <thead><tr><th>Compare</th><th>Palm Jumeirah</th><th>Palm Jebel Ali</th></tr></thead>
   <tbody>
    <tr><td>Market stage</td><td>Established, completed island</td><td>Under development</td></tr>
    <tr><td>Pricing evidence</td><td>Completed sales by villa, plot and condition</td><td>Exact design, frond and seller payment position</td></tr>
    <tr><td>Ownership costs</td><td>Condition, running costs, renovation</td><td>Instalments, outstanding balance, transfer costs</td></tr>
    <tr><td>Timing</td><td>Occupancy and agreed possession</td><td>The unit's contractual delivery schedule</td></tr>
   </tbody></table></div></div>
 </div>
<div class="card reveal mt"><span class="eyebrow">Residency</span><h3>Golden Visa eligibility.</h3><p>The UAE 10-year Golden Visa for property investors applies to property valued at AED 2 million or more, subject to approval by the relevant authorities — every villa on this site is above that threshold. Nakheel and Meraas sales centres now offer Golden Visa facilitation for new and existing customers. Off-plan and resale eligibility conditions are set by the authorities and should be confirmed for the specific villa.</p><span class="small">Source: <a href="https://www.nakheel.com/media-centre/press-release/news-detail/2026/06/29/meraas-and-nakheel-enhance-customer-experience-with-dedicated-golden-visa-facilitation" target="_blank" rel="noopener" style="color:var(--gold-lt)">Nakheel, 29 June 2026</a></span></div>
  <div class="card reveal mt" style="margin-bottom:0"><span class="eyebrow">Official verification</span><h3>Verify the project, then evaluate the opportunity.</h3><p>Dubai Land Department's Project Status Enquiry shows a project's completion percentage and details by land number, project number or name.</p>
  <div class="btns" style="margin-top:8px"><a class="btn btn-line" href="https://realestateims.dubailand.gov.ae/Reports/IPMR.aspx?ZFIGbn%2b90aXPn%2f9TDVXDB1I6ghBWCGCQqictduCJuqk%3d" target="_blank" rel="noopener">Open DLD project record</a><a class="btn btn-line" href="https://dubailand.gov.ae/en/eservices/real-estate-project-status-landing/" target="_blank" rel="noopener">DLD Project Status</a></div></div>
  <p class="note">No figure on this website is a forecast of returns or appreciation. Asking prices, areas and availability are subject to confirmation against the individual villa's documents.</p>
</div></section>
{cta_band("Review a Palm Jebel Ali opportunity privately.", "Send the villa details. Mark identifies the key property and payment questions before you commit.", "Hello Mark, I would like you to review a Palm Jebel Ali resale opportunity and its payment position.", dark=False)}
'''
    return page("/palm-jebel-ali-resale-guide", "Palm Jebel Ali Resale Buying Guide | Mark Darsy",
                "A practical guide to Palm Jebel Ali resale checks: seller documents, developer payments, total acquisition cost, NOC coordination and transfer.",
                "pja-aerial-progress-overview-v1.webp", body)

# ---------------------------------------------------------------- PRIVACY
def privacy():
    secs = [("Information you may provide", "Your name, telephone number, property interest, budget or asking price, timing and any property details you choose to share."),
            ("How it is used", "To respond to your enquiry, assess suitable property opportunities, discuss a potential sale and coordinate related professional support. Your information is not sold as a contact list."),
            ("WhatsApp and external services", "The enquiry forms open WhatsApp with a prepared message. Information is shared only after you choose to press Send in WhatsApp. External platforms process information under their own terms and privacy policies. This website does not store form entries."),
            ("Accuracy and retention", "Property requirements and availability change. You may ask for your enquiry information to be corrected or deleted, subject to any legitimate transaction, compliance or record-keeping obligations."),
            ("Contact", f'For privacy questions, contact Mark Darsy on <a href="tel:{TEL}">{PHONE}</a>.')]
    s = "".join(f'<h2 style="font-size:30px;margin-top:40px">{h}</h2><p>{t}</p>' for h, t in secs)
    body = f'''<section class="phero"><div class="wrap narrow"><span class="eyebrow">Privacy</span><h1 style="font-size:clamp(40px,6vw,64px)">How your enquiry information is handled.</h1>
<p class="lead">When you contact Mark through this website or WhatsApp, the information you provide is used to respond to your property enquiry, prepare relevant options and coordinate requested real estate services.</p>{s}</div></section>'''
    return page("/privacy", "Privacy Notice | Palm Jebel Ali Resale",
                "How enquiry information shared with Mark Darsy through palmjebelali-resale.com and WhatsApp is used and handled.",
                "palm-jebel-ali-villa.webp", body)

def notfound():
    body = f'''<section class="phero" style="min-height:70vh;display:flex;align-items:center"><div class="wrap narrow"><span class="eyebrow">Page not found</span><h1>This villa has moved on.</h1>
<p class="lead">The page you were looking for isn't here. Browse the current listings or ask Mark directly.</p>
<div class="btns"><a class="btn btn-gold" href="/dubai-property-atlas">Browse villa listings</a><a class="btn btn-line" href="/">Home</a><a class="btn btn-line" href="{WA}" target="_blank" rel="noopener">WhatsApp Mark</a></div></div></section>'''
    html_ = head("/404", "Page Not Found | Palm Jebel Ali Resale", "The requested page could not be found.", "palm-jebel-ali-villa.webp").replace('<link rel="canonical" href="https://palmjebelali-resale.com/404">', '<meta name="robots" content="noindex">')
    return html_ + "\n" + header("") + body + footer()

def redirect(to):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{to}"><meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}")</script></head><body><a href="{to}">Continue</a></body></html>'''

ROUTES = ["/", "/dubai-property-atlas", "/beach-collection-resale", "/coral-collection-resale",
          "/palm-jebel-ali-position-guide", "/sell-your-palm-jebel-ali-villa", "/palm-jebel-ali-resale-guide", "/privacy"]

if __name__ == "__main__":
    write("/", home()); write("/beach-collection-resale", beach()); write("/coral-collection-resale", coral())
    write("/dubai-property-atlas", atlas()); write("/palm-jebel-ali-position-guide", position())
    write("/sell-your-palm-jebel-ali-villa", sell()); write("/palm-jebel-ali-resale-guide", guide()); write("/privacy", privacy())
    with open(os.path.join(OUT, "404.html"), "w") as f: f.write(notfound())
    for src, to in [("/dubai-property-atlas/designs/coral-dune", "/coral-collection-resale#coral-dune"),
                    ("/dubai-property-atlas/designs/sunset-mirage", "/coral-collection-resale#sunset-mirage"),
                    ("/dubai-property-atlas/communities/palm-jebel-ali", "/palm-jebel-ali-position-guide")]:
        write(src, redirect(to))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    sm = "".join(f"<url><loc>{SITE}{r if r != '/' else '/'}</loc><lastmod>2026-10-06</lastmod><priority>{'1.0' if r == '/' else '0.8'}</priority></url>" for r in ROUTES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    if os.environ.get("CUSTOM_DOMAIN"):
        with open(os.path.join(OUT, "CNAME"), "w") as f: f.write(os.environ["CUSTOM_DOMAIN"] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1D1B18"/><rect x="5" y="5" width="54" height="54" fill="none" stroke="#A9874F" stroke-width="2"/><text x="32" y="41" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="#F3ECDF">MD</text></svg>')
    base = os.environ.get("BASE_PATH", "").rstrip("/")
    if base:  # preview under a sub-path (e.g. github.io/MarkDarsy)
        import glob
        for fp in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True) + [os.path.join(OUT, "assets", "site.css")]:
            t = open(fp, encoding="utf-8").read()
            for a in ('href="/', 'src="/', 'poster="/', 'url(/', 'url=/', 'replace("/', 'action="/'):
                t = t.replace(a + "/", a.replace("/", "\x00") + "/").replace(a, a[:-1] + base + "/").replace(a.replace("/", "\x00") + "/", a + "/")
            open(fp, "w", encoding="utf-8").write(t)
    print("built", PSF_MIN, PSF_MAX, "base=" + (base or "/"))
