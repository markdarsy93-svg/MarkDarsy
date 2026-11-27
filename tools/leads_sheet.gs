/**
 * Landing-page leads -> Google Sheet (account markdarsy93@gmail.com)
 *
 * Setup (once, about 2 minutes):
 * 1. Open the "Landing Page Leads (Athlon, PJA, Nad Al Sheba)" Google Sheet
 *    https://docs.google.com/spreadsheets/d/1CXwXl10uD5-xJ7gO3HJ5Q0lw15X4BBYWptpdn1xRz1Y/edit > Extensions > Apps Script.
 * 2. Paste this whole file over the default code, click Save.
 * 3. Deploy > New deployment > type "Web app".
 *    Execute as: Me.  Who has access: Anyone.  Click Deploy, then Allow.
 * 4. Copy the Web app URL (ends in /exec) and set SHEET_URL in tools/landing.py.
 *
 * Each enquiry from /lp/athlon, /lp/palm-jebel-ali and /lp/nad-al-sheba-gardens appends one row.
 */
var HEADERS = ['Received (Dubai)', 'Page', 'Intent', 'Name', 'Phone', 'Email', 'Property type', 'Budget',
  'Unit / plot', 'Timeline', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'fbclid', 'gclid', 'URL', 'Status', 'Notes'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var d = JSON.parse(e.postData.contents || '{}');
    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sh.getLastRow() === 0) { sh.appendRow(HEADERS); sh.setFrozenRows(1); }
    var clean = function (v) { v = String(v || '').slice(0, 300); return /^[=+\-@]/.test(v) ? "'" + v : v; };
    var when = Utilities.formatDate(new Date(), 'Asia/Dubai', 'yyyy-MM-dd HH:mm');
    sh.appendRow([when, clean(d.page), clean(d.intent), clean(d.name), clean(d.phone), clean(d.email), clean(d.type),
      clean(d.budget), clean(d.unit), clean(d.timeline), clean(d.utm_source), clean(d.utm_medium), clean(d.utm_campaign),
      clean(d.utm_content), clean(d.fbclid), clean(d.gclid), clean(d.url), 'New', '']);
    return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
