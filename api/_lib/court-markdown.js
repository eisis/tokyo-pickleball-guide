// ============================================================
// 申請フォームの入力 ⇔ コートのファイル（src/content/courts/*.md）の変換
// ・書き出す形は既存ファイルと同じ並び・書き方にそろえる（PRの差分が読みやすいように）
// ・フォームにない項目（画像の取得元・非表示フラグなど）は、更新のときもそのまま残す
// ============================================================
import { parse as parseYaml } from 'yaml';
import { BOOKING_SYSTEM_OPTIONS } from './court-form.js';

// content.config.ts の並び順
const KEY_ORDER = [
  'name', 'area', 'prefecture', 'environment', 'category', 'courts', 'address', 'access', 'hours', 'price', 'rental',
  'reservation', 'description', 'image', 'imageSource', 'officialUrl', 'imageUrl', 'booking', 'bookingSystem',
  'availabilityUrl', 'location', 'mapQuery', 'openedAt', 'updatedAt', 'sources', 'hidden', 'ownerVerified',
];

// ---------- 読み込み ----------
export function parseCourtFile(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(text);
  if (!m) throw new Error('frontmatter not found');
  return { data: parseYaml(m[1]) || {}, body: m[2].trim() };
}

// ---------- 書き出し ----------
const BARE = /^[a-z][a-z0-9-]*$/; // 英小文字だけの値（tokyo・indoor など）は引用符なしで書く
const DATE = /^\d{4}-\d{2}-\d{2}$/;

// 引用符なしで書いても意味が変わらない文字列か（既存ファイルの書き方に合わせて、差分を小さくする）
// 数字で始まるもの・記号で始まるもの・「, : # [ ] { }」を含むもの・true/null などは引用符を付ける
const RESERVED = /^(true|false|yes|no|on|off|null|~)$/i;
const plainOk = (s) =>
  s.length > 0 && s === s.trim() && !/^[\d\-+.?:,\[\]{}#&*!|>'"%@`<=~]/.test(s) && !/[,\[\]{}#"]|: |:$|\n/.test(s) && !RESERVED.test(s) && !/:\/\//.test(s);
function scalar(v) {
  if (typeof v === 'number' || typeof v === 'boolean') return String(v);
  if (v instanceof Date) return v.toISOString().slice(0, 10);
  const s = String(v);
  if (DATE.test(s) || BARE.test(s) || plainOk(s)) return s;
  return JSON.stringify(s); // JSON の文字列はそのまま YAML として読める
}
function flow(obj) {
  return '{ ' + Object.entries(obj).filter(([, v]) => v !== undefined && v !== '').map(([k, v]) => `${k}: ${scalar(v)}`).join(', ') + ' }';
}

function keyLines(k, v) {
  if (v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length)) return [];
  if (k === 'sources') return ['sources:', ...v.map((s) => `  - ${scalar(s)}`)];
  if (k === 'description' && v && typeof v === 'object') return ['description:', `  ja: ${scalar(v.ja)}`, `  en: ${scalar(v.en)}`];
  if (Array.isArray(v)) return [`${k}: [${v.map(scalar).join(', ')}]`];
  if (v && typeof v === 'object' && !(v instanceof Date)) return [`${k}: ${flow(v)}`];
  return [`${k}: ${scalar(v)}`];
}
const orderOf = (data) => [...KEY_ORDER.filter((k) => k in data), ...Object.keys(data).filter((k) => !KEY_ORDER.includes(k))];

/** 新しく作るファイル */
export function serializeCourt(data, body) {
  const lines = orderOf(data).flatMap((k) => keyLines(k, data[k]));
  return `---\n${lines.join('\n')}\n---\n${body ? `\n${body.trim()}\n` : ''}`;
}

/**
 * 更新：元のファイルの「変わった項目の行だけ」を書き換える（コメントや書き方はそのまま残る）
 * text: 元のファイル / before・after: 変更前後のデータ / body: 変更後の本文
 */
export function patchCourtFile(text, before, after, body) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(text);
  const lines = m[1].split(/\r?\n/);
  // 上の階層の項目ごとに、行のまとまりに分ける（字下げされた行・リストの行は直前の項目に属する）
  const blocks = [];
  for (const line of lines) {
    const km = /^([A-Za-z_][\w]*):/.exec(line);
    if (km || !blocks.length) blocks.push({ key: km ? km[1] : null, lines: [line] });
    else blocks[blocks.length - 1].lines.push(line);
  }
  const same = (a, b) => JSON.stringify(a ?? null) === JSON.stringify(b ?? null);
  const out = [];
  const done = new Set();
  for (const b of blocks) {
    if (!b.key) { out.push(...b.lines); continue; }
    done.add(b.key);
    if (same(before[b.key], after[b.key])) out.push(...b.lines);
    else out.push(...keyLines(b.key, after[b.key]));
  }
  // 元のファイルになかった項目は、決まった並び順の位置に差し込む
  for (const k of orderOf(after).filter((k) => !done.has(k))) {
    const add = keyLines(k, after[k]);
    if (!add.length) continue;
    const prevKeys = KEY_ORDER.slice(0, Math.max(0, KEY_ORDER.indexOf(k)));
    let at = -1;
    out.forEach((l, i) => { const km = /^([A-Za-z_][\w]*):/.exec(l); if (km && prevKeys.includes(km[1])) at = i; });
    if (at === -1) { out.unshift(...add); continue; }
    let end = at + 1;
    while (end < out.length && !/^[A-Za-z_][\w]*:/.test(out[end])) end++;
    out.splice(end, 0, ...add);
  }
  const oldBody = m[2];
  const newBody = body.trim() === oldBody.trim() ? oldBody.replace(/^\n?/, '') : body ? `${body.trim()}\n` : '';
  return `---\n${out.join('\n')}\n---\n${newBody ? `\n${newBody}` : ''}`;
}

// ---------- フォーム → コートのデータ ----------
const clean = (s) => String(s || '').replace(/<[^>]*>/g, '').replace(/\r\n/g, '\n').trim();
const oneLine = (s) => clean(s).replace(/\s*\n\s*/g, ' ');

/**
 * values: 検証済みの入力 / existing: 更新のときの今のデータ（新規は null）
 * 戻り値の notes は、審査で確認してほしいこと（PRのチェックリストに出す）
 */
export function toCourtData(values, existing, { today, location, images }) {
  const prev = existing ? { ...existing.data } : {};
  const notes = [];
  const d = { ...prev };

  d.name = oneLine(values.name);
  const areaEn = oneLine(values.areaEn);
  d.area = { ja: oneLine(values.areaJa), en: areaEn || prev.area?.en || oneLine(values.areaJa) };
  if (!areaEn && !prev.area?.en) notes.push('エリア表示の英語が未入力のため、日本語を仮に入れています。');
  d.prefecture = values.prefecture;
  d.environment = values.environment;
  // 既存ファイルで category を省略している（＝専用コート）なら、省略のままにする
  d.category = existing && !prev.category && values.category === 'dedicated' ? undefined : values.category;
  d.courts = values.courts ? Number(values.courts) : undefined;
  d.address = oneLine(values.address);
  const accessJa = oneLine(values.accessJa);
  const accessEn = oneLine(values.accessEn);
  d.access = accessJa ? { ja: accessJa, en: accessEn || prev.access?.en || accessJa } : undefined;
  if (accessJa && !accessEn && !prev.access?.en) notes.push('アクセスの英語が未入力のため、日本語を仮に入れています。');
  d.hours = oneLine(values.hours) || undefined;
  d.price = oneLine(values.price) || undefined;
  d.rental = values.rentalStatus ? { status: values.rentalStatus, note: oneLine(values.rentalNote) || undefined } : undefined;
  d.reservation = values.reservation.length ? values.reservation : undefined;
  const descJa = oneLine(values.descriptionJa);
  const descEn = oneLine(values.descriptionEn);
  d.description = { ja: descJa, en: descEn || (prev.description?.ja === descJa ? prev.description?.en : '') || descJa };
  if (d.description.en === descJa) notes.push('ひとこと紹介の英語が未入力のため、日本語を仮に入れています。');

  if (images?.length) {
    d.image = images[0];
    delete d.imageSource; // 運営者の写真を使うので、自動取得の情報は外す
    delete d.imageUrl;
  }
  d.officialUrl = values.officialUrl || undefined;
  // 予約ボタンの文言：ネット・LINEで予約できるなら「予約する」、それ以外は「詳細を見る」。更新でURLが同じなら今の設定を残す
  const canBook = values.reservation.includes('online') || values.reservation.includes('line');
  const keepLabel = existing && prev.booking?.url === values.bookingUrl ? prev.booking.label : null;
  d.booking = { url: values.bookingUrl, label: keepLabel || (canBook ? 'book' : 'info') };
  const sys = values.bookingSystem === 'その他' ? oneLine(values.bookingSystemOther) || undefined : values.bookingSystem || prev.bookingSystem;
  d.bookingSystem = sys;
  d.availabilityUrl = values.availabilityUrl || undefined;

  if (location) d.location = location;
  else if (!values.mapUrl) delete d.location; // 地図リンクを消した
  if (!d.location) notes.push('地図の位置が未設定のため、このコートは地図にピンが出ません（Googleマップのリンクがあれば location を追加）。');
  d.mapQuery = prev.mapQuery && existing && prev.name === d.name ? prev.mapQuery : `${d.name} ${d.address}`.trim();

  d.openedAt = values.openedAt || undefined;
  d.updatedAt = today;
  const sources = new Set(prev.sources || []);
  if (values.officialUrl && (!existing || values.officialUrl !== prev.officialUrl)) sources.add(values.officialUrl);
  d.sources = sources.size ? [...sources] : undefined;

  const prevBody = existing ? existing.body : '';
  let body = existing ? keepBodyImages(prevBody, clean(values.body)) : clean(values.body);
  const extra = (images || []).slice(1).map((src, i) => `![${d.name}の写真${i + 2}](${src})`);
  if (extra.length) body = [body, extra.join('\n\n')].filter(Boolean).join('\n\n');

  return { data: d, body, notes };
}

// ---------- コートのデータ → フォーム（更新時の初期値） ----------
export function fromCourtData(data, body) {
  const sys = data.bookingSystem;
  const known = BOOKING_SYSTEM_OPTIONS.some((o) => o.v === sys);
  return {
    name: data.name || '',
    category: data.category || 'dedicated',
    environment: data.environment || [],
    courts: data.courts ?? '',
    prefecture: data.prefecture || '',
    areaJa: data.area?.ja || '',
    areaEn: data.area?.en || '',
    address: data.address || '',
    accessJa: data.access?.ja || '',
    accessEn: data.access?.en || '',
    mapUrl: data.location ? `https://www.google.com/maps?q=${data.location.lat},${data.location.lng}` : '',
    officialUrl: data.officialUrl || '',
    openedAt: data.openedAt ? String(data.openedAt instanceof Date ? data.openedAt.toISOString() : data.openedAt).slice(0, 10) : '',
    hours: data.hours || '',
    price: data.price || '',
    rentalStatus: data.rental?.status || '',
    rentalNote: data.rental?.note || '',
    descriptionJa: data.description?.ja || '',
    descriptionEn: data.description?.en && data.description.en !== data.description?.ja ? data.description.en : '',
    body: (body || '').replace(/!\[[^\]]*\]\([^)]*\)\s*/g, '').trim(), // 本文の画像はフォームに出さない（更新しても消えない）
    reservation: data.reservation || [],
    bookingUrl: data.booking?.url || '',
    availabilityUrl: data.availabilityUrl || '',
    bookingSystem: sys ? (known ? sys : 'その他') : '',
    bookingSystemOther: sys && !known ? sys : '',
  };
}

// 更新時に本文の画像を残す
export function keepBodyImages(oldBody, newBody) {
  const imgs = (oldBody || '').match(/!\[[^\]]*\]\([^)]*\)/g) || [];
  const missing = imgs.filter((m) => !newBody.includes(m));
  return [newBody, ...missing].filter(Boolean).join('\n\n');
}

// ---------- 差分（PRの説明用） ----------
const show = (v) => (v === undefined || v === null || v === '' ? '—' : typeof v === 'object' ? JSON.stringify(v) : String(v));
const KEY_LABELS = {
  name: '施設名', area: 'エリア表示', prefecture: '都道府県', environment: '屋内/屋外', category: '施設の種類', courts: '面数', address: '住所',
  access: 'アクセス', hours: '営業時間', price: '料金', rental: 'レンタル', reservation: '予約方法', description: 'ひとこと紹介', image: 'メイン写真',
  imageSource: '画像の取得元', imageUrl: '画像URL', officialUrl: '公式サイト', booking: '予約ページ', bookingSystem: '予約システム',
  availabilityUrl: '空き状況ページ', location: '地図の位置', mapQuery: '地図の検索語', openedAt: 'オープン日', sources: '情報源', ownerVerified: '運営者掲載',
};
const DEFAULTS = { category: 'dedicated', hidden: false, ownerVerified: false }; // 書いていないときの値（content.config.ts と同じ）
export function diffCourt(before, after) {
  const withDefaults = (o) => { const x = { ...o }; for (const k in DEFAULTS) if (x[k] === undefined) x[k] = DEFAULTS[k]; return x; };
  before = withDefaults(before);
  after = withDefaults(after);
  const keys = [...new Set([...Object.keys(before), ...Object.keys(after)])].filter((k) => k !== 'updatedAt');
  return keys
    .filter((k) => show(before[k]) !== show(after[k]))
    .map((k) => ({ key: KEY_LABELS[k] || k, before: show(before[k]), after: show(after[k]) }));
}

// ---------- ファイル名（ページのURLになる） ----------
export function slugify(s) {
  return String(s || '')
    .normalize('NFKD').replace(/[̀-ͯ]/g, '')
    .toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48).replace(/-+$/, '');
}

// ---------- Googleマップのリンク → 緯度経度 ----------
export function coordsFromMapUrl(url) {
  const s = decodeURIComponent(String(url || ''));
  const pats = [/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/, /@(-?\d+\.\d+),(-?\d+\.\d+)/, /[?&](?:q|query|ll|center|destination)=(-?\d+\.\d+),\s*(-?\d+\.\d+)/];
  for (const p of pats) {
    const m = p.exec(s);
    if (m) {
      const lat = Number(m[1]), lng = Number(m[2]);
      if (lat > 20 && lat < 50 && lng > 120 && lng < 155) return { lat: Number(lat.toFixed(6)), lng: Number(lng.toFixed(6)) };
    }
  }
  return null;
}

/** 短縮リンク（maps.app.goo.gl など）は転送先をたどってから読む */
export async function resolveMapUrl(url) {
  if (!url) return null;
  let cur = url;
  for (let i = 0; i < 4; i++) {
    const found = coordsFromMapUrl(cur);
    if (found) return found;
    let host;
    try { host = new URL(cur).hostname; } catch { return null; }
    if (!/(^|\.)(goo\.gl|google\.[a-z.]+|maps\.app\.goo\.gl|g\.co)$/.test(host)) return null;
    try {
      const r = await fetch(cur, { redirect: 'manual', signal: AbortSignal.timeout(5000) });
      const next = r.headers.get('location');
      if (!next) {
        if (r.status === 200) { const html = await r.text(); return coordsFromMapUrl(html.slice(0, 200000)); }
        return null;
      }
      cur = new URL(next, cur).toString();
    } catch { return null; }
  }
  return coordsFromMapUrl(cur);
}

// ---------- 運営者確認（メールのドメインが公式サイトと同じか） ----------
const FREE_MAIL = /(^|\.)(gmail\.com|googlemail\.com|yahoo\.co\.jp|yahoo\.com|icloud\.com|me\.com|outlook\.(com|jp)|hotmail\.(com|co\.jp)|live\.(jp|com)|docomo\.ne\.jp|ezweb\.ne\.jp|au\.com|softbank\.ne\.jp|i\.softbank\.jp|ymobile\.ne\.jp)$/;
function baseDomain(host) {
  const parts = host.toLowerCase().replace(/^www\./, '').split('.');
  const n = /\.(co|or|ne|ac|go|lg|gr|ed|ad)\.jp$/.test(host.toLowerCase()) ? 3 : 2;
  return parts.slice(-n).join('.');
}
export function emailMatchesSite(email, siteUrl) {
  if (!email || !siteUrl) return false;
  const domain = String(email).split('@')[1]?.toLowerCase() || '';
  if (!domain || FREE_MAIL.test(domain)) return false;
  try { return baseDomain(domain) === baseDomain(new URL(siteUrl).hostname); } catch { return false; }
}
