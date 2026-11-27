#!/usr/bin/env python3
"""Mark Darsy, Villa Specialist: multi-community lead-generation website.

Builds a standalone static site into villa-specialist/ (to be served on Mark's new domain).
Reuses the landing-page template from tools/landing.py.

  python3 tools/villaspecialist.py                 -> villa-specialist/
  python3 tools/villaspecialist.py --preview DIR   -> self-contained single pages for review

Set DOMAIN once the domain is bought, and LIVE = True only after Mark approves going live
(until then every page carries noindex).
"""
import copy, html, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import landing as L

DOMAIN = ""      # e.g. "villaspecialist.com" once bought
LIVE = False     # True = indexable by Google
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "villa-specialist")
IMGS = os.path.join(ROOT, "site", "images")

ATH = next(p for p in L.PAGES if p["slug"] == "athlon")
PJA = next(p for p in L.PAGES if p["slug"] == "palm-jebel-ali")
NAS = next(p for p in L.PAGES if p["slug"] == "nad-al-sheba-gardens")

# Athlon clusters: 3-bed townhouse sizes from DLD transfer records Mark tracks (Athlon 3BR owners file, 23 Nov 2026)
CLUSTERS = [
    ("delphi", "Delphi", "2,294–2,298", "1,805–1,981"),
    ("olympia", "Olympia", "2,278–2,281", "1,805–1,809"),
    ("theon", "Theon", "2,278–2,281", "1,805–1,997"),
    ("diagon", "Diagon", "2,278–2,281", "1,969–2,074"),
    ("leon", "Leon", "2,294–2,297", "1,808–2,138"),
]

NAV = [("/athlon/", "Athlon"), ("/palm-jebel-ali/", "Palm Jebel Ali"), ("/nad-al-sheba-gardens/", "Nad Al Sheba"), ("/#owners", "Owners")]

EXTRA_CSS = """
.mnav{display:flex;gap:22px;margin-left:auto;margin-right:18px}
.mnav a{color:#fff;text-decoration:none;font-size:.9rem;font-weight:600;opacity:.9}
.mnav a:hover{opacity:1;color:var(--gold)}
.crumbs{position:relative;z-index:2;font-size:.8rem;margin-bottom:14px;color:rgba(255,255,255,.75)}
.crumbs a{color:rgba(255,255,255,.9)}
@media (max-width:960px){.mnav{display:none}}
"""

def nav_html():
    return '<nav class="mnav" aria-label="Communities">' + "".join(f'<a href="{h}">{n}</a>' for h, n in NAV) + "</nav>"

def site_page(p, path, crumbs=None):
    q = copy.deepcopy(p)
    q["home_href"] = "/"
    q["nav"] = nav_html()
    q["privacy"] = "/privacy/"
    q["robots"] = "index, follow" if LIVE else "noindex, follow"
    if DOMAIN:
        q["head_extra"] = f'\n<link rel="canonical" href="https://{DOMAIN}{path}">'
    if crumbs:
        trail = " / ".join(f'<a href="{h}">{html.escape(n)}</a>' for h, n in crumbs)
        q["eyebrow_html"] = trail
    return q

def render(q, inline):
    out = L.build(q, inline=inline)
    out = out.replace("</style>", EXTRA_CSS + "</style>", 1)
    if q.get("eyebrow_html"):
        out = out.replace('<span class="eyebrow">', f'<div class="crumbs">{q["eyebrow_html"]}</div><span class="eyebrow">', 1)
    if q["slug"] == "":
        out = out.replace("Dubai villas and townhouses is developed by its master developer; this page is not affiliated with or endorsed by the developer.",
                          "Each community shown is developed by its master developer; this site is not affiliated with or endorsed by any developer.")
        out = out.replace("Get the Dubai villas details", "Tell Mark what you need")
    if not inline:
        # site images live at /img/ on the new domain
        out = out.replace("/images/lp/", "/img/").replace("/images/", "/img/")
    return out

def cluster_page(slug, name, bua, plot):
    p = copy.deepcopy(ATH)
    p.update(
        slug=f"athlon/{slug}", name=f"{name} at Athlon", short=name,
        title=f"{name} Townhouses, Athlon by Aldar | Mark Darsy, Villa Specialist",
        desc=f"{name} cluster at Athlon by Aldar, Dubailand: 3-bed townhouses. Ask Mark Darsy for available units, floor plans, prices and payment plan, or a free valuation of your {name} home.",
        eyebrow=f"Athlon by Aldar · {name} cluster",
        h1=f"{name} at Athlon.<br><em>3-bed townhouses.</em>",
        hero="athlon-townhouses.webp", hero_alt=f"Athlon 4-plex townhouses, developer render",
        facts=[("3 bed", "townhouses"), (f"{bua}", "sq ft built-up (DLD records)"), (f"{plot}", "sq ft plot (DLD records)"), ("Athlon", "by Aldar, Dubailand")],
        about_h=f"{name}, one of Athlon's townhouse clusters.",
        about=(f"{name} is a cluster of 4-plex townhouses inside Athlon by Aldar. The 3-bedroom townhouses Mark tracks here are about {bua} sq ft built-up "
               f"on plots of about {plot} sq ft, according to DLD transfer records. Residents share Athlon's 4.6 km trail-running loop, 3.7 km cycling loop, "
               f"2.2 km family loop and seven clubhouses. Ask Mark which {name} units are available now, including single-row and corner positions."),
        units=[("3-bed townhouse", f"{name} · about {bua} sq ft", "Ground floor living and kitchen, three bedrooms upstairs. Floor plan on request."),
               ("Resale units", "Available now", f"Owners in {name} selling below or near the original price. Ask for the current list."),
               ("Owners", f"Own in {name}?", "Free valuation and free premium listing to sell or rent out your townhouse.")],
        split=("athlon-masterplan.webp", "Athlon master plan aerial view, developer render"),
        types=["3-bed townhouse", "Not sure yet"],
        owner_h=f"Own a townhouse in {name}?",
        links=("Other Athlon clusters.", [(c[1], "3-bed townhouses", f"/athlon/{c[0]}/") for c in CLUSTERS if c[0] != slug]),
    )
    return p

def home_page():
    p = copy.deepcopy(ATH)
    p.update(
        slug="", name="Dubai villas and townhouses", short="Dubai villas",
        title="Mark Darsy, Villa Specialist | Dubai Villas & Townhouses for Sale",
        desc="Mark Darsy, Villa Specialist (BRN 52456): villas and townhouses in Athlon, Palm Jebel Ali and Nad Al Sheba Gardens. Floor plans, prices and payment plans on WhatsApp. Free valuation for owners.",
        eyebrow="Mark Darsy · Villa Specialist · Dubai",
        h1="Villas &amp; townhouses in Dubai.<br><em>Buy, sell or reinvest.</em>",
        hero="palm-jebel-ali-beach-villas.webp", hero_alt="Palm Jebel Ali beach villas, developer image",
        facts=[("3", "communities covered in depth"), ("3–7", "bedrooms"), ("Free", "valuation for owners"), ("BRN", "52456, RERA-registered broker")],
        about_h="One specialist for villas, from first call to transfer.",
        about=("Mark Darsy focuses on villas and townhouses: Athlon by Aldar, Palm Jebel Ali by Nakheel and Nad Al Sheba Gardens by Meraas. "
               "Buyers get the brochure, floor plans, prices and payment plan on WhatsApp, with honest advice on position and value. "
               "Owners get a free valuation and a free premium listing to sell, rent out or sell and reinvest."),
        units=[("Athlon by Aldar", "Dubailand · 3–6 bed", "Active-living community: townhouses, standard and premium villas.", "/athlon/"),
               ("Palm Jebel Ali", "Nakheel · 5–7 bed", "Frond villas and beachfront homes, resale and new releases.", "/palm-jebel-ali/"),
               ("Nad Al Sheba Gardens", "Meraas · 3–7 bed", "Gated family villas and townhouses around a swimmable lagoon.", "/nad-al-sheba-gardens/")],
        no_pack=True, units_eyebrow="Communities", units_h="Choose your <em>community</em>.",
        split=("athlon-villa-street.webp", "Athlon villa street, developer render"),
        gallery=[],
        types=["Townhouse", "3-bed villa", "4-bed villa", "5-bed villa", "6-bed+ villa", "Not sure yet"],
        budgets=["Under AED 3M", "AED 3M – 5M", "AED 5M – 10M", "AED 10M – 20M", "AED 20M+"],
        owner_h="Own a villa or townhouse in Dubai?",
        links=("Athlon clusters.", [(c[1], "3-bed townhouses at Athlon", f"/athlon/{c[0]}/") for c in CLUSTERS]),
    )
    return p

def pages():
    ath = copy.deepcopy(ATH)
    ath["links"] = ("Athlon by <em>cluster</em>.", [(c[1], "3-bed townhouses", f"/athlon/{c[0]}/") for c in CLUSTERS])
    out = [("/", site_page(home_page(), "/")),
           ("/athlon/", site_page(ath, "/athlon/", [("/", "Home")])),
           ("/palm-jebel-ali/", site_page(PJA, "/palm-jebel-ali/", [("/", "Home")])),
           ("/nad-al-sheba-gardens/", site_page(NAS, "/nad-al-sheba-gardens/", [("/", "Home")]))]
    for c in CLUSTERS:
        out.append((f"/athlon/{c[0]}/", site_page(cluster_page(*c), f"/athlon/{c[0]}/", [("/", "Home"), ("/athlon/", "Athlon")])))
    return out

PRIVACY = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Privacy | Mark Darsy, Villa Specialist</title><meta name="robots" content="noindex">
<style>body{margin:0;background:#FBF8F2;color:#1E1D1B;font:16px/1.7 system-ui,sans-serif}main{max-width:720px;margin:0 auto;padding:48px 20px}a{color:#8C6D3F}</style></head>
<body><main><p><a href="/">← Mark Darsy, Villa Specialist</a></p><h1>Privacy</h1>
<p>When you send an enquiry, your name, phone, email and the details you choose are sent to Mark Darsy (BRN 52456) by email and kept in his enquiry sheet, only to answer your enquiry about buying, selling or renting a property.</p>
<p>Your details are never sold or shared with other agencies. Reply STOP on WhatsApp, or email to ask, and your details are removed and you are not contacted again.</p>
<p>The site uses Google Analytics to count visits and enquiries. No other tracking is used.</p>
<p>Contact: WhatsApp <a href="https://wa.me/971585414999">+971 58 541 4999</a>.</p></main></body></html>"""

def build_site():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "img"))
    used = set()
    for path, q in pages():
        h = render(q, inline=False)
        used |= set(re.findall(r"/img/([\w.-]+\.webp)", h))
        d = os.path.join(OUT, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f: f.write(h)
        print("wrote", path)
    for n in used:
        src = os.path.join(IMGS, "lp", n) if os.path.exists(os.path.join(IMGS, "lp", n)) else os.path.join(IMGS, n)
        shutil.copy(src, os.path.join(OUT, "img", n))
    os.makedirs(os.path.join(OUT, "privacy"))
    with open(os.path.join(OUT, "privacy", "index.html"), "w", encoding="utf-8") as f: f.write(PRIVACY)
    shutil.copy(os.path.join(ROOT, "site", "favicon.svg"), OUT)
    os.makedirs(os.path.join(OUT, "fonts"))
    for fn in os.listdir(os.path.join(ROOT, "site", "fonts")):
        shutil.copy(os.path.join(ROOT, "site", "fonts", fn), os.path.join(OUT, "fonts", fn))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\n" + ("Allow: /\n" if LIVE else "Disallow:\n") + (f"Sitemap: https://{DOMAIN}/sitemap.xml\n" if DOMAIN else ""))
    if DOMAIN:
        with open(os.path.join(OUT, "CNAME"), "w") as f: f.write(DOMAIN + "\n")
        with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                    "".join(f"<url><loc>https://{DOMAIN}{p}</loc></url>\n" for p, _ in pages()) + "</urlset>\n")
    with open(os.path.join(OUT, ".nojekyll"), "w") as f: f.write("")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        d = sys.argv[2]; os.makedirs(d, exist_ok=True)
        for path, q in pages():
            name = (path.strip("/").replace("/", "-") or "home") + ".html"
            with open(os.path.join(d, name), "w", encoding="utf-8") as f: f.write(render(q, inline=True))
            print("preview", name)
    else:
        build_site()
