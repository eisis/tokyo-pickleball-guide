// ============================================================
// 掲載申請の承認・見送りの通知（GitHub Actions の court-review.yml から呼ばれる）
//   POST /api/court-review  （Authorization: Bearer <SUBMIT_SECRET>）
//   { meta: PRに埋め込んだ暗号文, slug: 公開されるページ, merged: true/false }
//   merged=true  → 申請者に掲載完了メール、台帳を「完了」に
//   merged=false → 台帳を「対応不要」に（申請者へのメールは送らない。必要なら info@ から個別に連絡）
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
    const pageUrl = slug ? `${SITE_URL}/courts/${slug}/` : SITE_URL;

    if (merged) {
      const isNew = meta.mode === 'new';
      await sendMail({
        to: meta.email,
        reply_to: process.env.CONTACT_TO,
        subject: `【${SITE_NAME}】「${meta.facility}」の${isNew ? '掲載' : '掲載内容の更新'}が完了しました（${meta.id}）`,
        html: mailLayout(`
          <p>${esc(meta.name)} 様</p>
          <p>お待たせしました。「${esc(meta.facility)}」の${isNew ? '掲載' : '掲載内容の更新'}が完了しました。</p>
          ${mailButton(pageUrl, 'コートのページを見る')}
          <p>料金や営業時間が変わったとき、写真を差し替えたいときは、下のページからいつでも更新をお申し込みいただけます。</p>
          <p><a href="${SITE_URL}/owners/${slug ? `?court=${encodeURIComponent(slug)}` : ''}" style="color:#0e8a8f">掲載内容を更新する</a></p>
          <p>大会・練習会・体験会などのイベントも無料で掲載できます。<a href="${SITE_URL}/contact/?type=event" style="color:#0e8a8f">イベントの掲載はこちら</a></p>
          <p style="margin-top:20px;color:#5b6b73;font-size:13px">Instagram・X（@pickleballtokyo）でも新しいコートを紹介しています。<br>このメールにそのまま返信すると ${esc(process.env.CONTACT_TO || '')} に届きます。</p>`),
      });
    }

    try {
      await sheetUpdate('コート掲載申請', meta.id, merged ? { ステータス: '完了', 公開日時: nowJst() } : { ステータス: '対応不要' });
    } catch (e) { console.error('sheet update failed', e.message); }

    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error(e);
    return res.status(400).json({ ok: false, error: String(e.message || e).slice(0, 200) });
  }
}
