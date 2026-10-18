// ============================================================
// イベント掲載フォームの入力 → イベントのファイル（src/content/events/*.md）と主催者のファイル（src/content/organizers/*.md）
// ・書き出す形は手書きのファイルと同じ並びにそろえる（PRの差分が読みやすいように）
// ・メールアドレスはファイルに書かない。照合用に、合言葉（SUBMIT_SECRET）付きのハッシュだけを書く
// ============================================================
import crypto from 'node:crypto';
import { parse as parseYaml } from 'yaml';

const WEEK = ['日', '月', '火', '水', '木', '金', '土'];
const q = (s) => JSON.stringify(String(s)); // JSONの文字列はYAMLとしてもそのまま読める

/** メールアドレス → 照合用のキー（元のアドレスには戻せない） */
export function emailKey(email) {
  const s = process.env.SUBMIT_SECRET;
  if (!s) throw new Error('SUBMIT_SECRET not set');
  return crypto.createHmac('sha256', s).update(String(email).trim().toLowerCase()).digest('hex').slice(0, 32);
}

export function parseFrontmatter(text) {
  const m = String(text).match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { data: {}, body: '' };
  return { data: parseYaml(m[1]) || {}, body: m[2].trim() };
}

export function slugify(s) {
  return String(s || '').toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40).replace(/-+$/, '');
}

/** 主催者のファイル名の候補：InstagramやXのID → サイトのドメイン → 主催者名（英字のとき） */
export function organizerSlugBase(values) {
  const u = values.organizerUrl || values.url || '';
  try {
    const url = new URL(u);
    const host = url.hostname.replace(/^www\./, '');
    const first = url.pathname.split('/').filter(Boolean)[0] || '';
    if (/(instagram\.com|x\.com|twitter\.com|facebook\.com|tiktok\.com)$/.test(host) && first) return slugify(first.replace(/^@/, ''));
    if (!/(google|line\.me|lin\.ee|forms\.gle|peatix|connpass|tennisbear|labola)/.test(host)) return slugify(host.split('.')[0]);
  } catch {}
  return slugify(values.organizerName);
}

/** 毎週同じ曜日に並んでいれば「毎週土曜」のような言い方を返す */
export function weeklyLabel(dates) {
  if (dates.length < 3) return '';
  const ds = dates.map((d) => new Date(d + 'T00:00:00Z'));
  const day = ds[0].getUTCDay();
  const weekly = ds.every((d, i) => d.getUTCDay() === day && (i === 0 || (d - ds[i - 1]) / 86400000 === 7));
  return weekly ? `毎週${WEEK[day]}曜` : '';
}

export const timeLabel = (v) => (v.timeStart ? `${v.timeStart.replace(/^0/, '')}〜${v.timeEnd ? v.timeEnd.replace(/^0/, '') : ''}` : '');

/** フォームの値 → イベントのファイル */
export function serializeEvent(v, { dates, organizer, today, posted }) {
  const time = timeLabel(v);
  const weekly = weeklyLabel(dates);
  const entryRequired = v.entry !== 'walkin';
  const url = v.url || (entryRequired ? v.entryUrl : '');
  const sources = [...new Set([v.url, v.entryUrl].filter(Boolean))];
  const L = [];
  L.push(`title: ${q(v.title)}`);
  L.push(`type: ${v.type}`);
  L.push(`dates: [${dates.join(', ')}]`);
  if (weekly) L.push(`schedule: ${q(`${weekly} ${time}`.trim())}`);
  if (time) L.push(`time: ${q(time)}`);
  if (v.court && v.court !== 'other') {
    L.push(`court: ${v.court}`);
  } else {
    L.push(`venue:`, `  name: ${q(v.venueName)}`);
    if (v.venueAddress) L.push(`  address: ${q(v.venueAddress)}`);
    L.push(`prefecture: ${v.venuePref}`);
  }
  if (v.level) L.push(`level: ${v.level}`);
  if (v.price) L.push(`price: ${q(v.price)}`);
  L.push(`entry:`, `  required: ${entryRequired}`);
  if (entryRequired && v.deadline) L.push(`  deadline: ${v.deadline}`);
  if (entryRequired && v.entryUrl && v.entryUrl !== url) L.push(`  url: ${q(v.entryUrl)}`);
  L.push(`summary: ${q(v.summary)}`);
  if (url) L.push(`url: ${q(url)}`);
  L.push(`organizer:`);
  if (organizer.id) L.push(`  id: ${organizer.id}`);
  L.push(`  name: ${q(organizer.name)}`);
  L.push(`updatedAt: ${today}`);
  if (sources.length) L.push(`sources:`, ...sources.map((s) => `  - ${q(s)}`));
  if (posted) L.push(`organizerPosted: true`);
  const body = (v.detail || '').trim();
  return `---\n${L.join('\n')}\n---\n${body ? `\n${body}\n` : ''}`;
}

/** 新しい主催者のファイル。trusted: true の主催者は、次回から確認なしで即時公開される */
export function serializeOrganizer({ name, url, trusted, keys, today }) {
  const L = [`name: ${q(name)}`];
  if (url) L.push(`url: ${q(url)}`);
  L.push(`trusted: ${trusted}           # true = 次回から同じメールアドレスの申し込みは確認なしで即時公開`);
  if (keys.length) L.push(`emailKeys: [${keys.map(q).join(', ')}]   # 申込メールアドレスの照合用（元のアドレスには戻せない）`);
  L.push(`since: ${today}`);
  return `---\n${L.join('\n')}\n---\n`;
}
