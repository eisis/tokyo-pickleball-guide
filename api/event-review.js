// ============================================================
// イベント掲載申請の承認・見送りの通知（GitHub Actions の event-review.yml から呼ばれる）
//   POST /api/event-review  （Authorization: Bearer <SUBMIT_SECRET>）
//   { meta: PRに埋め込んだ暗号文, slug: 公開されるページ, merged: true/false }
// ============================================================
import { SITE_NAME, SITE_URL, sendMail, mailButton, mailLayout, esc, unseal, safeEqual, sheetUpdate, nowJst } from './_lib/common.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  const auth = String(req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!process.env.SUBMIT_SECRET || !safeEqual(auth, process.env.SUBMIT_SECRET)) return res.status(403).json({ ok: false });

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const meta = unseal(body.meta);
    const slug = /^[a-z0-9][a-z0-9-]*$/.test(String(body.slug || '')) ? body.slug : '';
    const merged = body.merged === true;
    const pageUrl = slug ? `${SITE_URL}/events/${slug}/` : `${SITE_URL}/events/`;

    if (merged) {
      await sendMail({
        to: meta.email,
        reply_to: process.env.CONTACT_TO,
        subject: `【${SITE_NAME}】「${meta.title}」を公開しました（${meta.id}）`,
        html: mailLayout(`
          <p>${esc(meta.name)} 様</p>
          <p>お待たせしました。「${esc(meta.title)}」をイベントページに公開しました。</p>
          ${mailButton(pageUrl, 'イベントのページを見る')}
          ${meta.trusted ? '<p>次回からは、このメールアドレスでお申し込みいただくと、確認なしですぐに公開されます。</p>' : ''}
          <p>次の開催日は <a href="${SITE_URL}/events/submit/" style="color:#0e8a8f">掲載フォーム</a> からいつでも追加できます。日程の変更・中止は、このメールに返信してお知らせください。</p>`),
      });
    }
    try {
      await sheetUpdate('イベント掲載申請', meta.id, merged ? { ステータス: '公開済み', 公開日時: nowJst() } : { ステータス: '見送り' });
    } catch (e) { console.error('sheet update failed', e.message); }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error(e);
    return res.status(400).json({ ok: false, error: String(e.message || e).slice(0, 200) });
  }
}
