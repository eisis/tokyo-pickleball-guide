// ============================================================
// フォーム共通の部品（お問い合わせ・コート掲載申請で使い回す）
//   ロボット確認（Turnstile）／受付番号／受付台帳（スプレッドシート）／メール（Resend）／暗号化
// ============================================================
import crypto from 'node:crypto';

export const SITE_NAME = 'Pickleball Tokyo';
export const SITE_URL = 'https://www.pickleball-tokyo.com';

export const mailReady = () => Boolean(process.env.RESEND_API_KEY && process.env.CONTACT_TO && process.env.CONTACT_FROM);

// ---------------- ロボット確認 ----------------
export async function verifyTurnstile(token, ip) {
  const secret = process.env.TURNSTILE_SECRET_KEY;
  if (!secret) return true; // 未設定時（ローカル確認用）はスキップ
  if (!token) return false;
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ secret, response: token, remoteip: ip || '' }),
  });
  const j = await r.json();
  return j.success === true;
}

export const clientIp = (req) => (req.headers['x-forwarded-for'] || '').split(',')[0].trim();

// ---------------- 受付番号・日付 ----------------
export function makeReceiptId() {
  const d = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10).replace(/-/g, '');
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let s = '';
  for (let i = 0; i < 4; i++) s += chars[crypto.randomInt(chars.length)];
  return `PT-${d}-${s}`;
}
export const todayJst = () => new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
export const nowJst = () => new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });

// ---------------- 受付台帳（Google スプレッドシート） ----------------
// row は { 列名: 値 }。タブがなければ作られ、足りない列は右端に追加される（docs/contact/Code.gs）
export async function sheetAppend(sheet, row) {
  return sheetCall({ sheet, headers: Object.keys(row), row });
}
// 受付番号の行の列を書き換える（台帳スクリプトが setCells に対応している場合）
export async function sheetUpdate(sheet, id, cells) {
  return sheetCall({ action: 'update', sheet, id, cells });
}
async function sheetCall(payload) {
  const url = process.env.SHEET_WEBHOOK_URL;
  if (!url) throw new Error('SHEET_WEBHOOK_URL not set');
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret: process.env.SHEET_WEBHOOK_SECRET, ...payload }),
    redirect: 'follow',
  });
  const text = await r.text();
  if (!r.ok || !text.includes('"ok":true')) throw new Error('sheet: ' + text.slice(0, 200));
}

// ---------------- メール（Resend） ----------------
export async function sendMail(payload) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: process.env.CONTACT_FROM, ...payload }),
  });
  if (!r.ok) throw new Error('resend: ' + (await r.text()).slice(0, 200));
}

/** rows: [[見出し, 値], ...] */
export function mailTable(rows) {
  const tr = rows
    .map(([k, v]) => `<tr><th style="text-align:left;vertical-align:top;padding:8px 12px;background:#f3efe6;white-space:nowrap;font-weight:600">${esc(k)}</th><td style="padding:8px 12px;white-space:pre-wrap">${v ? esc(v) : '<span style="color:#9aa">（未入力）</span>'}</td></tr>`)
    .join('');
  return `<table style="border-collapse:collapse;width:100%;font-size:14px;border:1px solid #e6dfcf">${tr}</table>`;
}

export function mailButton(href, label) {
  return `<p style="margin:18px 0"><a href="${esc(href)}" style="display:inline-block;background:#0e8a8f;color:#fff;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:999px">${esc(label)}</a></p>`;
}

export function mailLayout(inner) {
  return `<div style="font-family:-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif;color:#1f3540;max-width:600px;margin:0 auto">
    <div style="background:#0e8a8f;color:#fff;padding:14px 20px;border-radius:10px 10px 0 0;font-weight:700">${SITE_NAME}</div>
    <div style="border:1px solid #e6dfcf;border-top:0;padding:20px;border-radius:0 0 10px 10px;line-height:1.7">${inner}</div>
    <p style="text-align:center;color:#8a9aa1;font-size:12px"><a href="${SITE_URL}" style="color:#0e8a8f">${SITE_URL.replace('https://', '')}</a></p></div>`;
}

export const fmt = (v) => (Array.isArray(v) ? v.join('、') : v == null ? '' : String(v));
export const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// ---------------- 暗号化 ----------------
// 公開リポジトリの PR に、申請者の連絡先を「鍵がないと読めない形」で入れておき、
// 承認（Merge）されたときに掲載完了メールを送るために使う。鍵は SUBMIT_SECRET。
function key() {
  const s = process.env.SUBMIT_SECRET;
  if (!s) throw new Error('SUBMIT_SECRET not set');
  return crypto.createHash('sha256').update(s).digest();
}
export function seal(obj) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv('aes-256-gcm', key(), iv);
  const enc = Buffer.concat([c.update(JSON.stringify(obj), 'utf8'), c.final()]);
  return Buffer.concat([iv, c.getAuthTag(), enc]).toString('base64url');
}
export function unseal(token) {
  const buf = Buffer.from(String(token), 'base64url');
  const d = crypto.createDecipheriv('aes-256-gcm', key(), buf.subarray(0, 12));
  d.setAuthTag(buf.subarray(12, 28));
  return JSON.parse(Buffer.concat([d.update(buf.subarray(28)), d.final()]).toString('utf8'));
}
export function safeEqual(a, b) {
  const x = Buffer.from(String(a || '')), y = Buffer.from(String(b || ''));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}
