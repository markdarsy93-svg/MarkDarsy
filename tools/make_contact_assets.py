#!/usr/bin/env python3
"""One-off: builds the contact-card photo and QR code committed under site/images.
Needs Pillow and qrcode (pip install pillow qrcode). Re-run only if contact details change."""
import os, sys
from PIL import Image
import qrcode
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gen

im = Image.open(os.path.join(gen.OUT, "images", "mark-darsy-authentic-advisor-v2.webp")).convert("RGB")
w, h = im.size; s = min(w, h)
im = im.crop(((w - s) // 2, 0, (w - s) // 2 + s, s)).resize((240, 240), Image.LANCZOS)
im.save(os.path.join(gen.OUT, "images", "mark-darsy-contact.jpg"), quality=82, optimize=True)

# The QR holds the vCard itself, so a phone camera offers "Add to Contacts" without opening the site.
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=0)
qr.add_data(gen.vcard(photo=False)); qr.make(fit=True)
m = qr.get_matrix(); n = len(m); d = ""
for y, row in enumerate(m):
    x = 0
    while x < n:
        if row[x]:
            e = x
            while e < n and row[e]: e += 1
            d += f"M{x} {y}h{e - x}v1h-{e - x}z"; x = e
        else: x += 1
with open(os.path.join(gen.OUT, "images", "mark-darsy-contact-qr.svg"), "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {n + 4} {n + 4}" shape-rendering="crispEdges"><rect x="-2" y="-2" width="{n + 4}" height="{n + 4}" fill="#fff"/><path fill="#1D1B18" d="{d}"/></svg>')
print("ok", qr.version)
