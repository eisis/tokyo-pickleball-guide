// 公式サイトの「リンクカード」情報（ページのタイトル・シェア用画像のURL）を取ってきて、コートのファイルに書き込む。
// SNSにURLを貼ったときに出るプレビューと同じ仕組み。画像はダウンロード・保存せず、相手のURLのまま表示する。
// - 対象：src/content/courts/*.md のうち linkCard: の行がないもの（作り直したいときは linkCard: の行を消す）
// - 取得元：officialUrl → なければ booking.url（予約システム・ニュース・SNSは施設の公式ページではないので除外）
// - 運営者から画像を外してほしいと言われたら、linkCard の "image" だけ消す（画像なしのカードになり、再取得もされない）
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';

const DIR = 'src/content/courts';

const SKIP_HOSTS = [
  'resv.jp', 'reserva.be', 'labola.jp', 'tablecheck.com', 'instabase.jp', 'lin.ee', 'line.me',
  'coubic.com', 'airrsv.net', 'peatix.com', 'news.', 'prtimes.jp', 'nikkei.com', 'yahoo.co.jp',
  'instagram.com', 'facebook.com', 'x.com', 'twitter.com', 'google.com',
];
const isSkipped = (url) => {
  const host = new URL(url).hostname;
  return SKIP_HOSTS.some((h) => (h.endsWith('.') ? host.startsWith(h) || host.includes(`.${h}`) : host === h || host.endsWith(`.${h}`)));
};

const UA = { 'user-agent': 'Mozilla/5.0 (compatible; PickleballTokyoBot/1.0; +https://www.pickleball-tokyo.com/)' };

const decode = (s) => s
  .replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'")
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
  .replace(/\s+/g, ' ').trim();

async function readCard(pageUrl) {
  const res = await fetch(pageUrl, { headers: UA, redirect: 'follow', signal: AbortSignal.timeout(15000) });
  if (!res.ok) throw new Error(`ページ取得失敗 ${res.status}`);
  const html = await res.text();
  const meta = (prop) =>
    html.match(new RegExp(`<meta[^>]+(?:property|name)=["']${prop}["'][^>]*content=["']([^"']+)["']`, 'i'))?.[1] ??
    html.match(new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]*(?:property|name)=["']${prop}["']`, 'i'))?.[1];
  const title = decode(meta('og:title') ?? html.match(/<title[^>]*>([^<]+)<\/title>/i)?.[1] ?? '');
  if (!title) throw new Error('ページのタイトルがない');
  const site = meta('og:site_name') ? decode(meta('og:site_name')) : undefined;
  const card = { url: res.url, title: title.slice(0, 80), ...(site ? { site } : {}) };

  const src = meta('og:image') ?? meta('og:image:url') ?? meta('twitter:image');
  if (src) {
    const image = new URL(decode(src), res.url).href;
    // 実際に画像が表示できるか確かめる（https・画像として返ってくるもの）
    const img = await fetch(image, { headers: UA, signal: AbortSignal.timeout(15000) }).catch(() => null);
    const type = img?.headers.get('content-type') ?? '';
    if (image.startsWith('https://') && img?.ok && type.startsWith('image/')) card.image = image;
    else console.log(`  （画像は使えないため、画像なしのカードにします：${image}）`);
  }
  return card;
}

let added = 0;
for (const file of readdirSync(DIR).filter((f) => f.endsWith('.md') && !f.startsWith('_'))) {
  const path = `${DIR}/${file}`;
  const text = readFileSync(path, 'utf8');
  const fm = text.split(/^---$/m)[1] ?? '';
  if (/^linkCard:/m.test(fm)) continue;

  const official = fm.match(/^officialUrl:\s*"?([^"\s#]+)/m)?.[1];
  const booking = fm.match(/^booking:\s*\{\s*url:\s*"?([^",\s}]+)/m)?.[1];
  const page = official ?? (booking && !isSkipped(booking) ? booking : null);
  const id = file.replace(/\.md$/, '');
  if (!page) {
    console.log(`- ${id}: 公式サイトのURLがないためスキップ（officialUrl: を書くと取得します）`);
    continue;
  }
  try {
    const card = await readCard(page);
    writeFileSync(path, text.replace(/^booking:/m, `linkCard: ${JSON.stringify(card)}\nbooking:`));
    console.log(`✓ ${id}: ${card.title}${card.image ? '（画像あり）' : ''}`);
    added++;
  } catch (e) {
    console.log(`- ${id}: ${e.message}（${page}）`);
  }
}
console.log(`\n${added}件のリンクカードを追加しました`);
