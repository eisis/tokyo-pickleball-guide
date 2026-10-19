// ============================================================
// お問い合わせAPI（Vercel Serverless Function）
//   GET  /api/contact  → フォーム定義を返す（画面がこれを読んで組み立てる）
//   POST /api/contact  → 検証 → 台帳(スプレッドシート)保存 → メール通知・自動返信
//
// 必要な環境変数（Vercel > Settings > Environment Variables）
//   RESEND_API_KEY        Resend のAPIキー
//   CONTACT_TO            通知先（info@pickleball-tokyo.com）
//   CONTACT_FROM          送信元（Pickleball Tokyo <noreply@pickleball-tokyo.com>）
//   TURNSTILE_SITE_KEY    Cloudflare Turnstile サイトキー（公開してよい）
//   TURNSTILE_SECRET_KEY  Cloudflare Turnstile シークレットキー
//   SHEET_WEBHOOK_URL     Google Apps Script のURL
//   SHEET_WEBHOOK_SECRET  Apps Script と共有する合言葉
// ============================================================

import { COMMON_FIELDS, TYPES, getType } from './_lib/contact-types.js';
import { SITE_NAME, verifyTurnstile, clientIp, makeReceiptId, nowJst, sheetAppend, sendMail, mailLayout, mailReady, fmt, esc } from './_lib/common.js';
const MIN_FILL_MS = 3000; // 3秒未満で送信されたらボットとみなす

export default async function handler(req, res) {
  if (req.method === 'GET') return sendConfig(res);
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});

    // 1) ボット対策：ハニーポット・送信速度
    if (body.website) return res.status(200).json({ ok: true, id: 'PT-IGNORED' }); // ボットには成功を装う
    if (body.startedAt && Date.now() - Number(body.startedAt) < MIN_FILL_MS) {
      return res.status(400).json({ ok: false, error: '送信が早すぎます。もう一度お試しください。' });
    }

    // 2) Turnstile 検証
    if (!(await verifyTurnstile(body.turnstileToken, clientIp(req)))) {
      return res.status(400).json({ ok: false, error: '認証に失敗しました。ページを再読み込みしてお試しください。' });
    }

    // 3) 種別と入力値の検証
    const type = getType(body.type);
    if (!type) return res.status(400).json({ ok: false, error: 'お問い合わせ種別が不正です。' });

    const fields = [...COMMON_FIELDS, ...type.fields];
    const { values, errors } = validate(fields, body.data || {});
    for (const f of fields) {
      if (f.confirmOf && !errors[f.name] && values[f.name] !== values[f.confirmOf]) errors[f.name] = 'メールアドレスが一致しません。';
    }
    if (body.agree !== true) errors.agree = 'プライバシーポリシーへの同意が必要です。';
    if (Object.keys(errors).length) return res.status(400).json({ ok: false, error: '入力内容をご確認ください。', fieldErrors: errors });

    // 4) 受付番号
    const id = makeReceiptId();
    const receivedAt = nowJst();
    // 確認用の項目は記録・メールに含めない
    const record = { id, receivedAt, type, fields: fields.filter((f) => !f.confirmOf), values, source: String(body.source || '').slice(0, 300) };

    // 5) 台帳保存とメール送信（台帳失敗でもメールは送る）
    const [sheet, notify] = await Promise.allSettled([saveToSheet(record), sendNotification(record)]);
    if (notify.status === 'rejected' && sheet.status === 'rejected') {
      console.error('both failed', notify.reason, sheet.reason);
      return res.status(500).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
    }
    if (sheet.status === 'rejected') console.error('sheet failed', sheet.reason);
    if (notify.status === 'rejected') console.error('notify failed', notify.reason);

    // 自動返信（失敗しても受付は成立）
    try { await sendAutoReply(record); } catch (e) { console.error('autoreply failed', e); }

    return res.status(200).json({ ok: true, id });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
  }
}

// ---------------- 定義の配信 ----------------
function sendConfig(res) {
  res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
  res.status(200).json({
    // メール送信の設定が揃うまでは「準備中」を表示する
    ready: mailReady(),
    turnstileSiteKey: process.env.TURNSTILE_SITE_KEY || '',
    common: COMMON_FIELDS,
    // href のある種別は専用ページへ移動する（例：コート掲載 → /owners/）
    types: TYPES.filter((t) => t.enabled !== false).map(({ id, label, description, icon, fields, href }) => ({ id, label, description, icon, fields: fields || [], href })),
  });
}

// ---------------- 検証 ----------------
// 項目の normalize / pattern（contact-types.js で指定）。画面とサーバーで同じ規則を使う
function normalizeValue(f, v) {
  if (f.normalize === 'digits') return v.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0)).replace(/[\s\-‐－ー―〒]/g, '');
  return v;
}
function validate(fields, raw) {
  const values = {};
  const errors = {};
  for (const f of fields) {
    let v = raw[f.name];
    if (f.type === 'checkbox') {
      v = Array.isArray(v) ? v.filter((x) => f.options.includes(x)) : [];
      if (f.required && v.length === 0) errors[f.name] = '1つ以上選択してください。';
      values[f.name] = v;
      continue;
    }
    v = typeof v === 'string' || typeof v === 'number' ? normalizeValue(f, String(v).trim()) : '';
    if (!v) {
      if (f.required) errors[f.name] = '必須項目です。';
      values[f.name] = '';
      continue;
    }
    if (f.maxLength && v.length > f.maxLength) errors[f.name] = `${f.maxLength}文字以内で入力してください。`;
    if ((f.type === 'select' || f.type === 'radio') && !f.options.includes(v)) errors[f.name] = '選択肢から選んでください。';
    if (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) errors[f.name] = 'メールアドレスの形式が正しくありません。';
    if (f.type === 'url' && !/^https?:\/\/\S+$/.test(v)) errors[f.name] = 'http(s):// から始まるURLを入力してください。';
    if (f.type === 'tel' && !/^[0-9+\-() ]{8,20}$/.test(v)) errors[f.name] = '電話番号の形式が正しくありません。';
    if (f.pattern && !new RegExp(f.pattern).test(v)) errors[f.name] = f.patternMessage || '入力の形式が正しくありません。';
    if (/https?:\/\//i.test(v) && f.type !== 'url' && f.type !== 'textarea') errors[f.name] = 'URLは入力できません。';
    if (f.type === 'number') {
      const n = Number(v);
      if (!Number.isInteger(n) || (f.min != null && n < f.min) || (f.max != null && n > f.max)) errors[f.name] = `${f.min}〜${f.max}の数字で入力してください。`;
    }
    values[f.name] = v;
  }
  return { values, errors };
}



// ---------------- 台帳（Google スプレッドシート） ----------------
async function saveToSheet({ id, receivedAt, type, fields, values, source }) {
  // 1項目1列。列名＝項目名。種別ごとに別タブ（台帳側で列が足りなければ自動で追加される）
  const row = { 受付番号: id, 受付日時: receivedAt, ステータス: '未対応' };
  for (const f of fields) row[f.label] = fmt(values[f.name]);
  row['送信元ページ'] = source;
  row['担当メモ'] = '';
  await sheetAppend(type.sheetName || type.label, row);
}

// ---------------- メール（Resend） ----------------

function sendNotification({ id, receivedAt, type, fields, values, source }) {
  const subjectTail = values[type.subjectField] ? ` / ${values[type.subjectField]}` : '';
  return sendMail({
    to: process.env.CONTACT_TO,
    reply_to: values.email, // そのまま返信すれば問い合わせ者に届く
    subject: `【${type.label}】${values.name}様${subjectTail}（${id}）`,
    html: mailLayout(`
      <p style="margin:0 0 4px">受付番号：<b>${esc(id)}</b></p>
      <p style="margin:0 0 16px;color:#5b6b73">受付日時：${esc(receivedAt)}${source ? `<br>送信元ページ：${esc(source)}` : ''}</p>
      ${table(fields, values)}`),
  });
}

function sendAutoReply({ id, type, fields, values }) {
  return sendMail({
    to: values.email,
    reply_to: process.env.CONTACT_TO,
    subject: `【${SITE_NAME}】お問い合わせを受け付けました（${id}）`,
    html: mailLayout(`
      <p>${esc(values.name)} 様</p>
      <p>${SITE_NAME} へのお問い合わせありがとうございます。<br>以下の内容で受け付けました。内容を確認のうえ、通常3営業日以内にご連絡いたします。</p>
      ${type.autoReplyNote ? `<p>${esc(type.autoReplyNote)}</p>` : ''}
      <p style="margin:16px 0 4px">受付番号：<b>${esc(id)}</b>／種別：${esc(type.label)}</p>
      ${table(fields, values)}
      <p style="margin-top:20px;color:#5b6b73;font-size:13px">このメールは送信専用アドレスから自動送信しています。<br>ご返信の際はこのメールにそのまま返信してください（${esc(process.env.CONTACT_TO || '')} に届きます）。</p>`),
  });
}

function table(fields, values) {
  const rows = fields
    .map((f) => `<tr><th style="text-align:left;vertical-align:top;padding:8px 12px;background:#f3efe6;white-space:nowrap;font-weight:600">${esc(f.label)}</th><td style="padding:8px 12px;white-space:pre-wrap">${esc(fmt(values[f.name])) || '<span style="color:#9aa">（未入力）</span>'}</td></tr>`)
    .join('');
  return `<table style="border-collapse:collapse;width:100%;font-size:14px;border:1px solid #e6dfcf">${rows}</table>`;
}


