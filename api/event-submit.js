// ============================================================
// イベント掲載API（Vercel Serverless Function）
//   GET  /api/event-submit  → フォームが使えるかどうか
//   POST /api/event-submit  → 検証 → 公開（または承認待ち）→ 受付台帳 → メール通知・自動返信
//
// 公開のしかたは、申請者の「信頼度」で分ける
//   承認済みの主催者（organizers/*.md が trusted: true で、メールのキーが一致）
//     → 公開待ちのブランチを作り、主催者のメールアドレスに「公開する」ボタンを送る
//        ボタンを押すと /api/event-confirm が main に取り込み、即時公開（1〜2分）
//        （メールアドレスを知っているだけの第三者が、承認済みの主催者になりすまして即時公開できないように）
//   はじめての主催者・情報提供
//     → 承認待ちの変更（PR）を作る。Merge で公開＋主催者のファイルが作られ、次回から即時公開になる
//        → GitHub Actions（event-review.yml）が /api/event-review を呼び、申請者に公開のお知らせ
//
// 環境変数はコート掲載申請と同じ（GITHUB_SUBMIT_TOKEN・SUBMIT_SECRET・RESEND_*・SHEET_*）
// ============================================================
import {
  SITE_NAME, SITE_URL, mailReady, verifyTurnstile, clientIp, makeReceiptId, todayJst, nowJst,
  sheetAppend, sendMail, mailTable, mailButton, mailLayout, esc, seal,
} from './_lib/common.js';
import { ALL_FIELDS, ORGANIZER_ROLES, DATE_LIMIT } from './_lib/event-form.js';
import { githubReady, readFile, fileExists, listDir, createPullRequest, createBranch } from './_lib/github.js';
import { emailKey, parseFrontmatter, slugify, organizerSlugBase, serializeEvent, serializeOrganizer } from './_lib/event-markdown.js';

const MIN_FILL_MS = 6000;
const CONFIRM_DAYS = 7; // 承認済みの主催者が「公開する」ボタンを押せる期限
const SHEET = 'イベント掲載申請';
const EVENT_DIR = 'src/content/events';
const ORG_DIR = 'src/content/organizers';
const COURT_DIR = 'src/content/courts';

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
    const today = todayJst();
    const { values, errors } = validate(body.data || {}, today);
    if (body.agree !== true) errors.agree = '掲載基準とプライバシーポリシーへの同意が必要です。';
    let courtName = '';
    if (!errors.court && values.court !== 'other' && githubReady()) {
      const text = await readFile(`${COURT_DIR}/${values.court}.md`);
      if (!text) errors.court = 'このコートは見つかりませんでした。';
      else courtName = parseFrontmatter(text).data.name || '';
    }
    if (Object.keys(errors).length) return res.status(400).json({ ok: false, error: '入力内容をご確認ください。', fieldErrors: errors });

    const id = makeReceiptId();
    const isOrganizer = ORGANIZER_ROLES.includes(values.role);
    const r = { id, receivedAt: nowJst(), values, courtName, isOrganizer, mode: 'review', slug: '', orgSlug: '', orgName: values.organizerName, link: null, ghError: '', source: String(body.source || '').slice(0, 300) };

    // 3) 公開（承認済みの主催者）または承認待ちの変更を作る
    if (githubReady()) {
      try {
        await publish(r, today);
      } catch (e) {
        console.error('github failed', e);
        r.ghError = String(e.message || e).slice(0, 200);
      }
    }

    // 4) 台帳とメール（GitHubの成否に関係なく必ず残す）
    const [sheet, notify] = await Promise.allSettled([saveToSheet(r), sendNotification(r)]);
    if (sheet.status === 'rejected') console.error('sheet failed', sheet.reason);
    if (notify.status === 'rejected') console.error('notify failed', notify.reason);
    if (sheet.status === 'rejected' && notify.status === 'rejected' && !r.link) {
      return res.status(500).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
    }
    try { await sendAutoReply(r); } catch (e) { console.error('autoreply failed', e); }

    return res.status(200).json({ ok: true, id, mode: r.link ? r.mode : 'review' });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
  }
}

// ---------------- 検証 ----------------
const optValues = (f) => (f.options || []).map((o) => o.v);
const visible = (f, raw) => !f.showIf || Object.entries(f.showIf).every(([k, want]) => want.includes(raw[k]));

function validate(raw, today) {
  const values = {};
  const errors = {};
  const maxDay = new Date(Date.parse(today) + DATE_LIMIT.daysAhead * 86400000).toISOString().slice(0, 10);
  for (const f of ALL_FIELDS) {
    let v = raw[f.name];
    if (f.type === 'dates') {
      const list = Array.isArray(v) ? [...new Set(v.map(String).filter((d) => /^\d{4}-\d{2}-\d{2}$/.test(d)))].sort() : [];
      if (!list.length) errors.dates = '開催日を1つ以上入れてください。';
      else if (list.length > DATE_LIMIT.max) errors.dates = `開催日は1回の申し込みで${DATE_LIMIT.max}日までです。`;
      else if (list[0] < today) errors.dates = '過ぎた日付が含まれています。';
      else if (list[list.length - 1] > maxDay) errors.dates = '1年以内の日付を入れてください。';
      values.dates = list;
      continue;
    }
    if (!visible(f, raw)) { values[f.name] = ''; continue; }
    v = typeof v === 'string' || typeof v === 'number' ? String(v).trim() : '';
    if (!v) {
      if (f.required) errors[f.name] = '必須項目です。';
      values[f.name] = '';
      continue;
    }
    if (f.maxLength && v.length > f.maxLength) errors[f.name] = `${f.maxLength}文字以内で入力してください。`;
    if ((f.type === 'select' || f.type === 'radio') && !optValues(f).includes(v)) errors[f.name] = '選択肢から選んでください。';
    if (f.type === 'court' && v !== 'other' && !/^[a-z0-9][a-z0-9-]{0,60}$/.test(v)) errors[f.name] = '会場を選んでください。';
    if (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) errors[f.name] = 'メールアドレスの形式が正しくありません。';
    if (f.type === 'url' && !/^https?:\/\/[^\s"<>]+$/.test(v)) errors[f.name] = 'http(s):// から始まるURLを入力してください。';
    if (f.type === 'time' && !/^\d{2}:\d{2}$/.test(v)) errors[f.name] = '時刻の形式が正しくありません。';
    if (f.type === 'date' && !/^\d{4}-\d{2}-\d{2}$/.test(v)) errors[f.name] = '日付の形式が正しくありません。';
    values[f.name] = v.replace(/\r\n/g, '\n');
  }
  if (!errors.emailConfirm && values.email !== values.emailConfirm) errors.emailConfirm = 'メールアドレスが一致しません。';
  if (!errors.timeEnd && values.timeEnd && values.timeStart && values.timeEnd <= values.timeStart) errors.timeEnd = '開始より後の時刻にしてください。';
  if (!errors.deadline && values.deadline && values.dates[values.dates.length - 1] && values.deadline > values.dates[values.dates.length - 1]) errors.deadline = '最後の開催日より前にしてください。';
  return { values, errors };
}

// ---------------- 公開・承認待ち ----------------
async function findOrganizer(key) {
  const names = (await listDir(ORG_DIR)).filter((n) => n.endsWith('.md') && !n.startsWith('_'));
  for (const n of names) {
    const text = await readFile(`${ORG_DIR}/${n}`);
    const { data } = parseFrontmatter(text || '');
    if ((data.emailKeys || []).includes(key)) return { slug: n.replace(/\.md$/, ''), data };
  }
  return null;
}

async function uniquePath(dir, base) {
  for (let i = 0; i < 20; i++) {
    const s = i ? `${base}-${i + 1}` : base;
    if (!(await fileExists(`${dir}/${s}.md`))) return s;
  }
  return `${base}-${Date.now().toString(36).slice(-4)}`;
}

async function publish(r, today) {
  const v = r.values;
  const key = emailKey(v.email);
  const org = await findOrganizer(key);
  const trusted = Boolean(org && org.data.trusted === true && r.isOrganizer);

  const files = [];
  if (org) {
    r.orgSlug = org.slug;
    r.orgName = org.data.name || v.organizerName;
  } else {
    let base = organizerSlugBase(v);
    if (!base || base.length < 3) base = `org-${r.id.slice(-6).toLowerCase()}`;
    r.orgSlug = await uniquePath(ORG_DIR, base);
    r.newOrganizer = true;
    files.push({
      path: `${ORG_DIR}/${r.orgSlug}.md`,
      content: serializeOrganizer({ name: v.organizerName, url: v.organizerUrl, trusted: r.isOrganizer, keys: r.isOrganizer ? [key] : [], today }),
    });
  }

  r.slug = await uniquePath(EVENT_DIR, `${r.orgSlug}-${v.dates[0]}`);
  files.push({
    path: `${EVENT_DIR}/${r.slug}.md`,
    content: serializeEvent(v, { dates: v.dates, organizer: { id: r.orgSlug, name: r.orgName }, today, posted: r.isOrganizer }),
  });

  const message = `イベント掲載：${v.title}（${r.orgName}／${r.id}）`;
  if (trusted) {
    try {
      const branch = `event/${r.id.toLowerCase()}`;
      await createBranch({ branch, message, files });
      const token = seal({ id: r.id, branch, slug: r.slug, title: v.title, message, exp: Date.now() + CONFIRM_DAYS * 86400000 });
      r.confirmUrl = `${SITE_URL}/api/event-confirm?t=${token}`;
      r.link = { url: `https://github.com/${process.env.GITHUB_REPO || 'eisis/tokyo-pickleball-guide'}/tree/${branch}` };
      r.mode = 'confirm';
      return;
    } catch (e) {
      console.error('confirm branch failed, fallback to PR', e.message);
      r.fallback = true;
    }
  }

  const notes = [];
  if (r.newOrganizer && r.isOrganizer) notes.push(`主催者「${v.organizerName}」のファイルも作ります（\`trusted: true\`）。Merge すると、次回から同じメールアドレスの申し込みは、主催者がメールのボタンを押すだけで即時公開になります。そうしたくない場合は、Files changed で \`trusted: false\` に直してから Merge してください。`);
  if (r.newOrganizer && !r.isOrganizer) notes.push('主催者本人ではなく情報提供のため、主催者は「承認済み」にしていません（`trusted: false`）。');
  if (r.newOrganizer) notes.push(`すでに掲載している主催者と同じ団体なら、Files changed で organizers のファイルを消し、イベントの \`organizer.id\` を既存のファイル名に直してください。`);
  if (org && !trusted) notes.push(`主催者「${r.orgName}」は登録済みですが、承認済み（trusted）ではないため確認に回っています。`);
  if (r.fallback) notes.push('承認済みの主催者でしたが、公開待ちのブランチを作れなかったため承認待ちにしています。');

  const prBody = [
    `イベントの掲載申請です。受付番号 **${r.id}**`,
    '',
    `- イベント：${v.title}`,
    `- 主催：${r.orgName}（${r.isOrganizer ? '主催者・スタッフからの申請' : '情報提供'}）`,
    `- 日程：${v.dates.length}日（${v.dates[0]}〜${v.dates[v.dates.length - 1]}）`,
    `- 会場：${v.court === 'other' ? v.venueName : r.courtName || v.court}`,
    `- ページ：\`/events/${r.slug}/\``,
    '',
    '### 確認すること',
    `- [ ] 申込・詳細ページで、日程・会場・参加費が一致している（${v.url || v.entryUrl || 'URLなし：主催者に確認'}）`,
    '- [ ] 誰でも参加を申し込めるイベントで、物販・勧誘が主な目的ではない',
    '- [ ] 下の Vercel のプレビューで、イベントのページの見た目に問題がない',
    ...notes.map((n) => `- [ ] ${n}`),
    '',
    '### 承認のしかた',
    '問題なければ **Merge pull request** を押すと公開され、申請者に公開のお知らせが自動で届きます。',
    '見送る場合は **Close pull request**（メールは送られないので、必要なら info@ から連絡）。',
    '',
    `<!-- pt-meta:${seal({ id: r.id, email: v.email, name: v.contactName, title: v.title, trusted: r.newOrganizer && r.isOrganizer })} -->`,
  ].filter((l) => l !== '').join('\n').replace(/\n(###)/g, '\n\n$1');

  r.link = await createPullRequest({
    branch: `event/${r.id.toLowerCase()}`,
    title: `イベント掲載：${v.title}（${r.id}）`,
    message,
    body: prBody,
    files,
    labels: ['イベント掲載'],
  });
  r.mode = 'review';
}

// ---------------- 台帳・メール ----------------
const label = (f, v) => {
  const o = (f.options || []).find((o) => o.v === v);
  return o ? o.label : v || '';
};
function rows(r, staff) {
  const v = r.values;
  return ALL_FIELDS.filter((f) => !f.confirmOf && (staff || f.public !== false || f.name === 'contactName'))
    .map((f) => {
      if (f.type === 'dates') return [f.label, v.dates.join('、')];
      if (f.type === 'court') return [f.label, v.court === 'other' ? 'その他の会場' : r.courtName || v.court];
      return [f.label, label(f, v[f.name])];
    })
    .filter(([, x]) => x);
}

function saveToSheet(r) {
  const row = {
    受付番号: r.id, 受付日時: r.receivedAt,
    ステータス: r.mode === 'confirm' ? '主催者の確認待ち' : '未対応',
    イベント名: r.values.title, 主催者: r.orgName,
    主催者ページ: r.orgSlug ? `/organizers/${r.orgSlug}/` : '',
    ページ: r.slug ? `/events/${r.slug}/` : '',
    承認画面: r.link ? r.link.url : r.ghError ? `作成失敗：${r.ghError}` : '（未作成）',
    初回開催日: r.values.dates[0], 開催日数: r.values.dates.length,
  };
  for (const [k, v] of rows(r, true)) if (!(k in row)) row[k] = v;
  row['送信元ページ'] = r.source;
  row['担当メモ'] = '';
  return sheetAppend(SHEET, row);
}

function sendNotification(r) {
  const v = r.values;
  const live = r.mode === 'confirm';
  const status = live
    ? `<p>承認済みの主催者からの申し込みです。主催者のメールアドレスに「公開する」ボタンを送りました。<b>押された時点で確認なしで公開</b>されます（${CONFIRM_DAYS}日以内）。公開後に問題があれば、ページのファイルに <code>hidden: true</code> を足すか削除してください。</p><p style="font-size:13px"><a href="${r.link.url}">公開待ちの内容（GitHub）</a>／公開予定のページ：${SITE_URL}/events/${r.slug}/<br>主催者にメールが届かない場合は、<a href="${r.confirmUrl}">こちらから公開</a>できます。</p>`
    : r.link
      ? `<p>承認待ちの変更を作りました。Vercel のプレビューで見た目を確認し、問題なければ Merge してください。申請者に公開のお知らせが自動で届きます。</p>${mailButton(r.link.url, '承認画面を開く（GitHub）')}`
      : `<p style="color:#a23224">承認画面を作れませんでした${r.ghError ? `：${esc(r.ghError)}` : '（GITHUB_SUBMIT_TOKEN が未設定）'}。内容は台帳に残っています。</p>`;
  return sendMail({
    to: process.env.CONTACT_TO,
    reply_to: v.email,
    subject: `【イベント${live ? '確認待ち' : '掲載申請'}】${v.title}（${r.orgName}／${r.id}）`,
    html: mailLayout(`
      <p style="margin:0 0 12px">受付番号：<b>${esc(r.id)}</b>／${esc(r.receivedAt)}</p>
      ${status}
      ${mailTable(rows(r, true))}`),
  });
}

function sendAutoReply(r) {
  const v = r.values;
  const live = r.mode === 'confirm';
  const next = live
    ? `<p>承認済みの主催者からのお申し込みです。下のボタンを押すと、確認なしですぐに公開されます（1〜2分でページに反映）。</p>${mailButton(r.confirmUrl, 'このイベントを公開する')}<p style="font-size:13px;color:#5b6b73">ボタンの期限は${CONFIRM_DAYS}日です。お心当たりのない場合は、このメールは破棄してください（公開されません）。</p>`
    : `<p>このあとの流れ</p>
       <ol style="margin:0 0 12px;padding-left:20px">
         <li>運営チームが内容を確認します（通常1〜2営業日）。確認のためにご連絡する場合があります。</li>
         <li>公開したら、ページのURLをメールでお知らせします。</li>
         ${r.isOrganizer ? '<li>次回からは、このメールアドレスでお申し込みいただくと、届いたメールのボタンを押すだけですぐに公開できます。</li>' : ''}
       </ol>`;
  return sendMail({
    to: v.email,
    reply_to: process.env.CONTACT_TO,
    subject: live ? `【${SITE_NAME}】「${v.title}」の公開ボタンをお送りします（${r.id}）` : `【${SITE_NAME}】イベント掲載のお申し込みを受け付けました（${r.id}）`,
    html: mailLayout(`
      <p>${esc(v.contactName)} 様</p>
      <p>${SITE_NAME} へのイベント掲載のお申し込み、ありがとうございます。</p>
      ${next}
      <p style="margin:16px 0 4px">受付番号：<b>${esc(r.id)}</b></p>
      ${mailTable(rows(r, false))}
      <p>日程の変更・中止は、このメールにそのまま返信してお知らせください。次の開催日は、<a href="${SITE_URL}/events/submit/" style="color:#0e8a8f">掲載フォーム</a>からいつでも追加できます。</p>
      <p style="margin-top:20px;color:#5b6b73;font-size:13px">このメールにそのまま返信すると ${esc(process.env.CONTACT_TO || '')} に届きます。<br>掲載中のイベントは「<a href="${SITE_URL}/this-week/" style="color:#0e8a8f">今週どこで打てる？</a>」のページにも並びます。</p>`),
  });
}
