import { chromium } from 'playwright';
const base = 'http://127.0.0.1:8080';
const pages = ['/', '/dubai-property-atlas/', '/beach-collection-resale/', '/coral-collection-resale/', '/palm-jebel-ali-position-guide/', '/sell-your-palm-jebel-ali-villa/', '/palm-jebel-ali-resale-guide/', '/privacy/', '/nope'];
const sizes = { mobile: { width: 390, height: 844 }, desktop: { width: 1440, height: 900 } };
const browser = await chromium.launch();
const report = [];
for (const [label, vp] of Object.entries(sizes)) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('requestfailed', r => errs.push('failed ' + r.url()));
  page.on('response', r => { if (r.status() >= 400 && !r.url().endsWith('/nope')) errs.push(r.status() + ' ' + r.url()); });
  for (const p of pages) {
    await page.goto(base + p, { waitUntil: 'networkidle' });
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')); });
    await page.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))); await page.waitForTimeout(400);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    const broken = await page.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src));
    report.push({ label, p, overflow, broken });
    const name = (p === '/' ? 'home' : p.replace(/\//g, '')) + '-' + label;
    await page.screenshot({ path: `shots/${name}.png`, fullPage: true });
  }
  report.push({ label, errors: [...new Set(errs)] });
  await ctx.close();
}
await browser.close();
console.log(JSON.stringify(report, null, 1));
import fs from 'fs'; fs.writeFileSync('shots/report.json', JSON.stringify(report, null, 1));
