// ============================================================
// 送客計測API（Vercel Serverless Function）
//   POST /api/track  … 予約・空き状況・地図・イベント申込リンクのクリックを、受付台帳の「送客ログ」タブに1行ずつ記録する
//   個人を特定する情報（IP・名前など）は記録しない
// ============================================================

const KINDS = { booking: '予約', availability: '空き状況', map: '地図', event_entry: 'イベント申込', event_detail: 'イベント詳細' };
const BOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|headless|lighthouse/i;

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  try {
    const ua = String(req.headers['user-agent'] || '');
    if (BOT.test(ua)) return res.status(204).end();

    const raw = typeof req.body === 'string' ? req.body : Buffer.isBuffer(req.body) ? req.body.toString() : JSON.stringify(req.body || {});
    const b = JSON.parse(raw || '{}');
    const kind = KINDS[b.kind];
    const courtId = String(b.courtId || '').slice(0, 80);
    const eventId = String(b.eventId || '').slice(0, 80);
    const isEvent = String(b.kind || '').startsWith('event_');
    if (!kind || !/^[a-z0-9-]+$/.test(isEvent ? eventId : courtId)) return res.status(204).end();

    const url = process.env.SHEET_WEBHOOK_URL;
    if (!url) return res.status(204).end();

    const row = {
      日時: new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' }),
      コートID: courtId,
      コート名: String(b.courtName || '').slice(0, 100),
      イベントID: isEvent ? eventId : '',
      イベント名: isEvent ? String(b.eventName || '').slice(0, 100) : '',
      クリック種別: kind,
      クリック場所: String(b.from || '').slice(0, 20),
      遷移先URL: String(b.url || '').slice(0, 300),
      元のページ: String(b.page || '').slice(0, 200),
      端末: /Mobi|Android|iPhone/i.test(ua) ? 'スマホ' : 'PC・タブレット',
    };
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ secret: process.env.SHEET_WEBHOOK_SECRET, sheet: '送客ログ', headers: Object.keys(row), row }),
      redirect: 'follow',
    });
    return res.status(204).end();
  } catch (e) {
    console.error('track failed', e);
    return res.status(204).end();
  }
}
