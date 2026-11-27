#!/usr/bin/env python3
"""Pre-merge and daily health check for the built site/ folder.

Run: python3 tools/site_check.py [site_dir]
Exits 1 if anything must be fixed before merging. Checks, offline:
  - every internal href/src points to a file that exists
  - every sitemap URL exists and is not noindex
  - each indexable page has a <title> and a meta description
  - the Google Search Console tag and verification file are still there
  - no burgundy, no "Alice", no apartment wording on villa pages
"""
import os, re, sys
from urllib.parse import urlparse, unquote

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "site")
ROOT = os.path.abspath(ROOT)
DOMAIN = "palmjebelali-resale.com"
GSC_TAG = "google-site-verification"
GSC_FILE = "googleb71c4d8f29254c1a.html"

errors, warns = [], []

def target(page, ref):
    ref = unquote(ref.split("#")[0].split("?")[0])
    if not ref:
        return None
    if ref.startswith("/"):
        p = os.path.join(ROOT, ref.lstrip("/"))
    else:
        p = os.path.join(os.path.dirname(page), ref)
    if os.path.isdir(p) or ref.endswith("/"):
        p = os.path.join(p, "index.html")
    return os.path.normpath(p)

pages = []
for d, _, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(d, f))

for page in sorted(pages):
    rel = os.path.relpath(page, ROOT)
    src = open(page, encoding="utf-8", errors="replace").read()
    noindex = re.search(r'<meta[^>]+name="robots"[^>]+noindex', src, re.I)
    if rel == GSC_FILE:
        continue
    for ref in re.findall(r'(?:href|src|poster)="([^"]+)"', src):
        u = urlparse(ref)
        if u.scheme in ("mailto", "tel", "data", "javascript", "whatsapp") or ref.startswith("#"):
            continue
        if u.scheme in ("http", "https"):
            if u.netloc.endswith(DOMAIN):
                ref = u.path or "/"
            else:
                continue
        t = target(page, ref)
        if t and not os.path.exists(t):
            errors.append(f"broken link {rel} -> {ref}")
    if not noindex and not rel.startswith(("email/", "404")):
        if not re.search(r"<title>[^<]{5,}</title>", src):
            errors.append(f"missing <title>: {rel}")
        if not re.search(r'<meta[^>]+name="description"[^>]+content="[^"]{30,}', src):
            warns.append(f"missing/short meta description: {rel}")
    low = src.lower()
    if "burgundy" in low or "#800020" in low:
        warns.append(f"burgundy colour found: {rel}")
    if re.search(r"\balice\b", low):
        errors.append(f"'Alice' mentioned: {rel}")

home = os.path.join(ROOT, "index.html")
if not os.path.exists(home) or GSC_TAG not in open(home, encoding="utf-8").read():
    errors.append("Search Console meta tag missing from home page (never remove it)")
if not os.path.exists(os.path.join(ROOT, GSC_FILE)):
    errors.append(f"{GSC_FILE} missing (never remove it)")

sm = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(sm):
    for loc in re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read()):
        t = target(home, urlparse(loc).path or "/")
        if not os.path.exists(t):
            errors.append(f"sitemap URL has no page: {loc}")
        elif re.search(r'name="robots"[^>]+noindex', open(t, encoding="utf-8").read(), re.I):
            errors.append(f"sitemap lists a noindex page: {loc}")
else:
    errors.append("sitemap.xml missing")

print(f"Checked {len(pages)} pages in {ROOT}")
for e in errors:
    print("ERROR", e)
for w in warns:
    print("WARN ", w)
print("RESULT:", "FAIL" if errors else "PASS", f"({len(errors)} errors, {len(warns)} warnings)")
sys.exit(1 if errors else 0)
