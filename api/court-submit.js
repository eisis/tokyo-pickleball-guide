// ============================================================
// コート掲載申請API（Vercel Serverless Function）
//   GET  /api/court-submit  → フォームが使えるかどうか（設定の確認）
//   POST /api/court-submit  → 検証 → GitHub に承認待ちの変更（PR）を作成 → 受付台帳 → メール通知・自動返信
//
// 流れ：申請 → PR（Vercel がプレビューを自動で作る）→ 運営者が中身を確認して Merge → 本番に公開
//       → GitHub Actions（court-review.yml）が /api/court-review を呼び、申請者に掲載完了メール
//
// 必要な環境変数（お問い合わせフォームの設定に加えて）
//   GITHUB_SUBMIT_TOKEN  このリポジトリだけの Contents / Pull requests 読み書き権限を持つトークン
//   SUBMIT_SECRET        申請者の連絡先の暗号化と、GitHub Actions からの呼び出し確認に使う合言葉
//   ※ GITHUB_SUBMIT_TOKEN が未設定でも受付はできる（台帳とメールにだけ残り、PRは作られない）
// ============================================================
import {
  SITE_NAME, SITE_URL, mailReady, verifyTurnstile, clientIp, makeReceiptId, todayJst, nowJst,
  sheetAppend, sendMail, mailTable, mailButton, mailLayout, esc, seal,
} from './_lib/common.js';
import { ALL_FIELDS, PHOTO_LIMIT, OPERATOR_ROLES, COOP_OPTIONS } from './_lib/court-form.js';
import { githubReady, readFile, fileExists, createPullRequest } from './_lib/github.js';
import { parseCourtFile, serializeCourt, patchCourtFile, toCourtData, diffCourt, slugify, resolveMapUrl, emailMatchesSite } from './_lib/court-markdown.js';

const MIN_FILL_MS = 8000; // 8秒未満で送信されたらボットとみなす（項目が多いので長め）
const SHEET = 'コート掲載申請';
const COURT_DIR = 'src/content/courts';
const IMAGE_DIR = 'public/images/courts';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
    return res.status(200).json({ ready: mailReady(), turnstileSiteKey: process.env.TURNSTILE_SITE_KEY || '' });
  }
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method Not Allowed' });

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});

    // 1) ボット対策
    if (body.website) return res.status(200).json({ ok: true, id: 'PT-IGNORED' });
    if (body.startedAt && Date.now() - Number(body.startedAt) < MIN_FILL_MS) {
      return res.status(400).json({ ok: false, error: '送信が早すぎます。もう一度お試しください。' });
    }
    if (!(await verifyTurnstile(body.turnstileToken, clientIp(req)))) {
      return res.status(400).json({ ok: false, error: '認証に失敗しました。ページを再読み込みしてお試しください。' });
    }

    // 2) 入力の検証
    const mode = body.mode === 'update' ? 'update' : 'new';
    const courtId = mode === 'update' ? String(body.courtId || '') : '';
    if (mode === 'update' && !/^[a-z0-9][a-z0-9-]{0,60}$/.test(courtId)) {
      return res.status(400).json({ ok: false, error: '更新するコートを選んでください。', fieldErrors: { courtId: '更新するコートを選んでください。' } });
    }
    const { values, errors } = validate(mode, body.data || {});
    const photos = Array.isArray(body.photos) ? body.photos : [];
    const photoErr = checkPhotos(photos);
    if (photoErr) errors.photos = photoErr;
    if (photos.length && !(values.photoRights || []).includes('ok')) errors.photoRights = '写真を送る場合は、権利の確認にチェックしてください。';
    if (body.agree !== true) errors.agree = '掲載基準とプライバシーポリシーへの同意が必要です。';
    if (Object.keys(errors).length) return res.status(400).json({ ok: false, error: '入力内容をご確認ください。', fieldErrors: errors });

    const id = makeReceiptId();
    const outOfArea = values.prefecture === 'other';
    const operator = OPERATOR_ROLES.includes(values.role);
    const domainMatch = operator && emailMatchesSite(values.email, values.officialUrl);

    // 3) GitHub に承認待ちの変更を作る（設定がない・エリア外のときは作らない）
    let pr = null;
    let prError = '';
    let slug = courtId;
    let existing = null;
    if (githubReady() && !outOfArea) {
      try {
        if (mode === 'update') {
          const text = await readFile(`${COURT_DIR}/${courtId}.md`);
          if (!text) return res.status(400).json({ ok: false, error: '更新するコートが見つかりませんでした。', fieldErrors: { courtId: 'このコートは見つかりませんでした。' } });
          existing = { ...parseCourtFile(text), text };
        } else {
          slug = await uniqueSlug(values, id);
        }
        pr = await openPullRequest({ id, mode, slug, values, photos, existing, operator, domainMatch });
      } catch (e) {
        console.error('github failed', e);
        prError = String(e.message || e).slice(0, 200);
      }
    }

    // 4) 台帳とメール（PRの成否に関係なく必ず残す）
    const record = { id, receivedAt: nowJst(), mode, courtId, slug, values, photos: photos.length, pr, prError, outOfArea, operator, domainMatch, source: String(body.source || '').slice(0, 300) };
    const [sheet, notify] = await Promise.allSettled([saveToSheet(record), sendNotification(record)]);
    if (sheet.status === 'rejected') console.error('sheet failed', sheet.reason);
    if (notify.status === 'rejected') console.error('notify failed', notify.reason);
    if (sheet.status === 'rejected' && notify.status === 'rejected' && !pr) {
      return res.status(500).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
    }
    try { await sendAutoReply(record); } catch (e) { console.error('autoreply failed', e); }

    return res.status(200).json({ ok: true, id, mode, outOfArea });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
  }
}

// ---------------- 検証 ----------------
const optValues = (f) => (f.options || []).map((o) => o.v);
function visible(f, mode, raw) {
  if (f.only && f.only !== mode) return false;
  if (f.showIf) {
    return Object.entries(f.showIf).every(([k, want]) => {
      const v = raw[k];
      if (want === '*') return Array.isArray(v) ? v.length > 0 : !!v;
      return want.includes(v);
    });
  }
  return true;
}

function validate(mode, raw) {
  const values = {};
  const errors = {};
  for (const f of ALL_FIELDS) {
    if (f.type === 'photos') continue;
    let v = raw[f.name];
    if (!visible(f, mode, raw)) { values[f.name] = f.type === 'checkbox' ? [] : ''; continue; }
    if (f.type === 'checkbox') {
      v = Array.isArray(v) ? [...new Set(v.filter((x) => optValues(f).includes(x)))] : [];
      if (f.required && !v.length) errors[f.name] = '1つ以上選択してください。';
      values[f.name] = v;
      continue;
    }
    v = typeof v === 'string' || typeof v === 'number' ? String(v).trim() : '';
    if (!v) {
      if (f.required) errors[f.name] = '必須項目です。';
      values[f.name] = '';
      continue;
    }
    if (f.maxLength && v.length > f.maxLength) errors[f.name] = `${f.maxLength}文字以内で入力してください。`;
    if ((f.type === 'select' || f.type === 'radio') && !optValues(f).includes(v)) errors[f.name] = '選択肢から選んでください。';
    if (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) errors[f.name] = 'メールアドレスの形式が正しくありません。';
    if (f.type === 'url' && !/^https?:\/\/[^\s"<>]+$/.test(v)) errors[f.name] = 'http(s):// から始まるURLを入力してください。';
    if (f.type === 'tel' && !/^[0-9+\-() ]{8,20}$/.test(v)) errors[f.name] = '電話番号の形式が正しくありません。';
    if (f.type === 'date' && !/^\d{4}-\d{2}-\d{2}$/.test(v)) errors[f.name] = '日付の形式が正しくありません。';
    if (f.type === 'number') {
      const n = Number(v);
      if (!Number.isInteger(n) || (f.min != null && n < f.min) || (f.max != null && n > f.max)) errors[f.name] = `${f.min}〜${f.max}の数字で入力してください。`;
    }
    values[f.name] = v;
  }
  if (!errors.emailConfirm && values.email !== values.emailConfirm) errors.emailConfirm = 'メールアドレスが一致しません。';
  if (!errors.environment && !values.environment?.length) errors.environment = '1つ以上選択してください。';
  return { values, errors };
}

function checkPhotos(photos) {
  if (photos.length > PHOTO_LIMIT.max) return `写真は${PHOTO_LIMIT.max}枚までです。`;
  for (const p of photos) {
    if (typeof p !== 'string') return '写真を読み込めませんでした。';
    const buf = Buffer.from(p, 'base64');
    if (buf.length > PHOTO_LIMIT.maxBytes) return '写真のサイズが大きすぎます。';
    if (!(buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff)) return '写真を読み込めませんでした。別の写真でお試しください。';
  }
  return '';
}

// ---------------- PR ----------------
async function uniqueSlug(values, id) {
  let base = slugify(values.nameEn);
  if (!base && values.officialUrl) {
    try { base = slugify(new URL(values.officialUrl).hostname.replace(/^www\./, '').split('.')[0]); } catch {}
  }
  if (!base || base.length < 3) base = `court-${id.slice(3, 11)}`;
  for (let i = 0; i < 20; i++) {
    const s = i ? `${base}-${i + 1}` : base;
    if (!(await fileExists(`${COURT_DIR}/${s}.md`))) return s;
  }
  return `${base}-${id.slice(-4).toLowerCase()}`;
}

async function openPullRequest({ id, mode, slug, values, photos, existing, operator, domainMatch }) {
  const tag = id.slice(-4).toLowerCase();
  const imageNames = photos.map((_, i) => (mode === 'update' ? `${slug}-${tag}${i ? `-${i + 1}` : ''}.jpg` : `${slug}${i ? `-${i + 1}` : ''}.jpg`));
  const images = imageNames.map((n) => `/images/courts/${n}`);
  const location = values.mapUrl ? await resolveMapUrl(values.mapUrl) : null;

  const { data, body, notes } = toCourtData(values, existing, { today: todayJst(), location, images });
  if (domainMatch || existing?.data?.ownerVerified) data.ownerVerified = true;
  else delete data.ownerVerified;
  if (values.mapUrl && !location && !data.location) notes.push('Googleマップのリンクから位置を読み取れませんでした。');
  if (operator && !domainMatch && !existing?.data?.ownerVerified) {
    notes.push('「運営者掲載」の表示：申請者のメールが公式サイトと同じドメインではないため付けていません。運営者本人と確認できたら `ownerVerified: true` を追加してください。');
  }
  if (!values.officialUrl && !existing?.data?.officialUrl) notes.push('公式サイトが未入力です。予約ページで内容を確認してください。');

  const md = existing ? patchCourtFile(existing.text, existing.data, data, body) : serializeCourt(data, body);
  const files = [{ path: `${COURT_DIR}/${slug}.md`, content: md }, ...photos.map((b64, i) => ({ path: `${IMAGE_DIR}/${imageNames[i]}`, base64: b64 }))];

  const isNew = mode === 'new';
  const changes = existing ? diffCourt(existing.data, data) : [];
  if (existing && body !== existing.body) changes.push({ key: '本文', before: '（変更前）', after: '（変更あり）' });
  const checkUrl = values.officialUrl || values.bookingUrl;
  const coop = (values.coop || []).length;

  const prBody = [
    `${isNew ? '新しいコートの掲載申請' : `掲載中のコート「${data.name}」の更新申請`}です。受付番号 **${id}**`,
    '',
    `- 施設：${data.name}（${values.areaJa}）`,
    `- ページ：\`/courts/${slug}/\``,
    `- 写真：${photos.length}枚`,
    `- 運営者掲載：${data.ownerVerified ? 'あり（メールのドメインが公式サイトと一致）' : 'なし'}`,
    coop ? `- 空き状況・予約連携の相談：**あり**（内容は受付台帳とメールを参照）` : '',
    '',
    '### 確認すること',
    `- [ ] 内容が公式情報と一致している（${checkUrl}）`,
    photos.length ? '- [ ] 写真が施設のもので、不適切な写り込みがない' : '',
    '- [ ] 下の Vercel のプレビューで、コートのページとカードの見た目に問題がない',
    ...notes.map((n) => `- [ ] ${n}`),
    '',
    changes.length ? '### 変更点\n\n| 項目 | 変更前 | 変更後 |\n|---|---|---|\n' + changes.map((c) => `| ${c.key} | ${cell(c.before)} | ${cell(c.after)} |`).join('\n') : '',
    '',
    '### 承認のしかた',
    '問題なければ **Merge pull request** を押すと公開され、申請者に掲載完了のメールが自動で届きます。',
    '直したいところは「Files changed」から編集できます。見送る場合は **Close pull request**（メールは送られないので、必要なら info@ から連絡）。',
    '',
    `<!-- pt-meta:${seal({ id, mode, email: values.email, name: values.contactName, facility: data.name })} -->`,
  ].filter((l) => l !== '').join('\n').replace(/\n(###)/g, '\n\n$1');

  return createPullRequest({
    branch: `submit/${id.toLowerCase()}`,
    title: `${isNew ? '掲載申請' : '掲載更新'}：${data.name}（${id}）`,
    message: `${isNew ? '掲載申請' : '掲載更新'}：${data.name}（${id}）`,
    body: prBody,
    files,
    labels: [isNew ? '掲載申請' : '掲載更新'],
  });
}
const cell = (s) => String(s).replace(/\|/g, '\\|').replace(/\n/g, ' ').slice(0, 160);

// ---------------- 台帳・メール ----------------
const label = (f, v) => {
  if (Array.isArray(v)) return v.map((x) => label(f, x)).join('、');
  const o = (f.options || []).find((o) => o.v === v);
  return o ? o.label : v || '';
};
const rows = (values, filter = () => true) =>
  ALL_FIELDS.filter((f) => f.type !== 'photos' && !f.confirmOf && filter(f)).map((f) => [f.label, label(f, values[f.name])]);

function saveToSheet(r) {
  const row = {
    受付番号: r.id, 受付日時: r.receivedAt, ステータス: '未対応', 申請の種類: r.mode === 'new' ? '新規掲載' : '掲載更新',
    施設名: r.values.name, ページ: r.outOfArea ? '（エリア外）' : `/courts/${r.slug}/`,
    承認画面: r.pr ? r.pr.url : r.prError ? `作成失敗：${r.prError}` : '（未作成）',
    連携相談: label(ALL_FIELDS.find((f) => f.name === 'coop'), r.values.coop),
    連携ステータス: (r.values.coop || []).length ? '未対応' : '',
  };
  for (const [k, v] of rows(r.values)) if (!(k in row)) row[k] = v;
  row['写真'] = `${r.photos}枚`;
  row['運営者確認'] = r.domainMatch ? 'メールのドメインが公式サイトと一致' : r.operator ? '未確認' : '運営者以外';
  row['送信元ページ'] = r.source;
  row['担当メモ'] = '';
  return sheetAppend(SHEET, row);
}

function coopBlock(values, forStaff) {
  const picked = COOP_OPTIONS.filter((o) => (values.coop || []).includes(o.v));
  if (!picked.length) return '';
  const timing = label(ALL_FIELDS.find((f) => f.name === 'coopTiming'), values.coopTiming);
  return `<div style="background:#eef8f7;border-radius:10px;padding:14px 16px;margin:16px 0">
    <p style="margin:0 0 6px;font-weight:700">${forStaff ? '空き状況・予約連携の相談あり' : 'ご相談いただいた内容'}</p>
    <ul style="margin:0;padding-left:20px">${picked.map((o) => `<li>${esc(o.label)}</li>`).join('')}</ul>
    ${timing ? `<p style="margin:8px 0 0">時期：${esc(timing)}</p>` : ''}
    ${values.coopNote ? `<p style="margin:8px 0 0;white-space:pre-wrap">${esc(values.coopNote)}</p>` : ''}</div>`;
}

function sendNotification(r) {
  const kind = r.mode === 'new' ? '新規掲載' : '掲載更新';
  const status = r.outOfArea
    ? '<p>掲載エリア外のため、承認画面は作っていません。エリアを広げるときの候補として台帳に記録しました。</p>'
    : r.pr
      ? `<p>承認待ちの変更を作りました。GitHub の画面で Vercel のプレビューを開いて見た目を確認し、問題なければ Merge してください。申請者に掲載完了メールが自動で届きます。</p>${mailButton(r.pr.url, '承認画面を開く（GitHub）')}`
      : `<p style="color:#a23224">承認画面（GitHub の PR）を作れませんでした${r.prError ? `：${esc(r.prError)}` : '（GITHUB_SUBMIT_TOKEN が未設定）'}。内容は台帳に残っています。</p>`;
  return sendMail({
    to: process.env.CONTACT_TO,
    reply_to: r.values.email,
    subject: `【${kind}】${r.values.name}（${r.id}）${(r.values.coop || []).length ? '［連携相談あり］' : ''}`,
    html: mailLayout(`
      <p style="margin:0 0 4px">受付番号：<b>${esc(r.id)}</b>／${kind}</p>
      <p style="margin:0 0 12px;color:#5b6b73">受付日時：${esc(r.receivedAt)}／写真：${r.photos}枚／運営者確認：${r.domainMatch ? 'メールのドメインが公式サイトと一致' : r.operator ? '未確認' : '運営者以外'}</p>
      ${status}
      ${coopBlock(r.values, true)}
      ${mailTable(rows(r.values))}`),
  });
}

function sendAutoReply(r) {
  const isNew = r.mode === 'new';
  const next = r.outOfArea
    ? '<p>現在 Pickleball Tokyo は東京・神奈川・千葉・埼玉のコートを掲載しています。掲載エリアを広げる際に、あらためてご連絡いたします。</p>'
    : `<p>このあとの流れ</p>
       <ol style="margin:0 0 12px;padding-left:20px">
         <li>担当が内容を確認します（通常3営業日以内）。確認のためにご連絡する場合があります。</li>
         <li>${isNew ? '掲載' : '更新'}が完了したら、ページのURLをメールでお知らせします。</li>
         ${(r.values.coop || []).length ? '<li>ご相談いただいた内容について、担当から個別にご連絡します。</li>' : ''}
       </ol>`;
  return sendMail({
    to: r.values.email,
    reply_to: process.env.CONTACT_TO,
    subject: `【${SITE_NAME}】${isNew ? '掲載' : '掲載内容の更新'}のお申し込みを受け付けました（${r.id}）`,
    html: mailLayout(`
      <p>${esc(r.values.contactName)} 様</p>
      <p>${SITE_NAME} への${isNew ? '掲載' : '掲載内容の更新'}のお申し込み、ありがとうございます。以下の内容で受け付けました。</p>
      ${next}
      ${coopBlock(r.values, false)}
      <p style="margin:16px 0 4px">受付番号：<b>${esc(r.id)}</b></p>
      ${mailTable(rows(r.values, (f) => f.name !== 'bookingSystemOther'))}
      <p style="margin-top:20px;color:#5b6b73;font-size:13px">このメールは送信専用アドレスから自動送信しています。<br>ご返信の際はこのメールにそのまま返信してください（${esc(process.env.CONTACT_TO || '')} に届きます）。<br><a href="${SITE_URL}/owners/" style="color:#0e8a8f">${SITE_URL.replace('https://', '')}/owners/</a></p>`),
  });
}
