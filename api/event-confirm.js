// ============================================================
// 承認済みの主催者が、メールの「このイベントを公開する」ボタンを押したときの処理
//   GET  /api/event-confirm?t=…  → 確認画面（ボタン）を出すだけ。何も公開しない
//         （メールのセキュリティ機能がリンクを自動で開いても、勝手に公開されないように）
//   POST /api/event-confirm      → 公開待ちのブランチを main に取り込む → Vercel が自動で公開
// t は event-submit.js が暗号化した { id, branch, slug, title, message, exp }
// ============================================================
import { SITE_NAME, SITE_URL, esc, unseal, sheetUpdate, nowJst } from './_lib/common.js';
import { mergeBranch, deleteBranch } from './_lib/github.js';

export default async function handler(req, res) {
  const t = String((req.method === 'POST' ? req.body?.t : req.query?.t) || '');
  let meta;
  try {
    meta = unseal(t);
    if (!/^event\/[a-z0-9-]+$/.test(meta.branch) || !/^[a-z0-9-]+$/.test(meta.slug)) throw new Error('bad token');
  } catch {
    return page(res, 400, 'リンクが正しくありません', '<p>お手数ですが、届いたメールのボタンからもう一度お試しください。</p>');
  }
  const pageUrl = `${SITE_URL}/events/${meta.slug}/`;

  if (Date.now() > Number(meta.exp)) {
    await deleteBranch(meta.branch); // 期限切れの公開待ちは片付ける
    return page(res, 410, '公開の期限が切れています', `<p>「${esc(meta.title)}」の公開ボタンの期限が過ぎました。お手数ですが、<a href="${SITE_URL}/events/submit/">掲載フォーム</a>からもう一度お申し込みください。</p>`);
  }

  if (req.method === 'GET') {
    return page(res, 200, 'このイベントを公開しますか？', `
      <p>「<b>${esc(meta.title)}</b>」を ${SITE_NAME} に公開します。</p>
      <form method="post"><input type="hidden" name="t" value="${esc(t)}"><button type="submit">公開する</button></form>
      <p class="sub">お心当たりのない場合は、このページを閉じてください（公開されません）。</p>`);
  }
  if (req.method !== 'POST') return res.status(405).end();

  try {
    const result = await mergeBranch(meta.branch, meta.message || `イベント掲載：${meta.title}（${meta.id}）`);
    if (result === 'missing') {
      return page(res, 200, 'すでに処理済みです', `<p>このイベントは公開済みか、取り下げられています。</p><p><a class="btn" href="${pageUrl}">イベントのページを見る</a></p>`);
    }
    try { await sheetUpdate('イベント掲載申請', meta.id, { ステータス: '公開済み（主催者が確認）', 公開日時: nowJst() }); } catch (e) { console.error('sheet update failed', e.message); }
    return page(res, 200, '公開しました', `<p>「${esc(meta.title)}」を公開しました。1〜2分ほどでページに反映されます。</p><p><a class="btn" href="${pageUrl}">イベントのページを見る</a></p>`);
  } catch (e) {
    console.error('confirm failed', e);
    return page(res, 500, '公開できませんでした', '<p>時間をおいてもう一度お試しいただくか、受付メールにそのまま返信してお知らせください。</p>');
  }
}

function page(res, status, title, inner) {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  return res.status(status).send(`<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)}｜${SITE_NAME}</title>
<style>body{font-family:-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif;color:#1f3540;background:#faf7f0;margin:0;padding:40px 16px;line-height:1.8}main{max-width:520px;margin:0 auto;background:#fff;border:1px solid #e6dfcf;border-radius:14px;padding:28px}h1{font-size:1.3rem;margin:0 0 12px}button,.btn{display:inline-block;background:#0e8a8f;color:#fff;border:0;font:inherit;font-weight:700;padding:12px 26px;border-radius:999px;text-decoration:none;cursor:pointer}.sub{color:#5b6b73;font-size:.9rem}a{color:#0e8a8f}</style></head>
<body><main><h1>${esc(title)}</h1>${inner}<p class="sub" style="margin-top:24px"><a href="${SITE_URL}/">${SITE_NAME}</a></p></main></body></html>`);
}
