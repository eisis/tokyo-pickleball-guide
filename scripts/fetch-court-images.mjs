// 画像がまだないコートについて、公式サイトの「シェア用画像（og:image）」を取ってきて保存する。
// - 対象：src/content/courts/*.md のうち image: の行がないもの
// - 取得元：imageUrl（コート写真を直接指定）→ officialUrl（あれば）→ なければ booking.url（予約サイト・ニュースサイトは除外）
// - 保存先：public/images/courts/<ファイル名>.jpg（横1200pxに縮小）
// - コートのファイルに image: と imageSource:（取得元）を書き足す
// ※ 施設の画像なので、掲載時に施設へ一言許可を取る運用にしています。
//   掲載をやめたい画像は、image: と imageSource: の行を消し、hidden 等で対応してください。
import { readdirSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import sharp from 'sharp';

const DIR = 'src/content/courts';
const OUT = 'public/images/courts';

// 施設の公式サイトではないので、ここの画像は使わない
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

async function findOgImage(pageUrl) {
  const res = await fetch(pageUrl, { headers: UA, redirect: 'follow' });
  if (!res.ok) throw new Error(`ページ取得失敗 ${res.status}`);
  const html = await res.text();
  const meta = (prop) =>
    html.match(new RegExp(`<meta[^>]+(?:property|name)=["']${prop}["'][^>]+content=["']([^"']+)["']`, 'i'))?.[1] ??
    html.match(new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["']${prop}["']`, 'i'))?.[1];
  const src = meta('og:image') ?? meta('og:image:url') ?? meta('twitter:image');
  if (!src) throw new Error('シェア用画像が設定されていない');
  return new URL(src.replace(/&amp;/g, '&'), res.url).href;
}

let added = 0;
for (const file of readdirSync(DIR).filter((f) => f.endsWith('.md') && !f.startsWith('_'))) {
  const path = `${DIR}/${file}`;
  const text = readFileSync(path, 'utf8');
  const fm = text.split(/^---$/m)[1] ?? '';
  if (/^image:/m.test(fm)) continue; // すでに画像あり

  const official = fm.match(/^officialUrl:\s*"?([^"\s#]+)/m)?.[1];
  const booking = fm.match(/^booking:\s*\{\s*url:\s*"?([^",\s}]+)/m)?.[1];
  const direct = fm.match(/^imageUrl:\s*"?([^"\s#]+)/m)?.[1]; // コート写真を直接指定したもの
  const page = direct ?? official ?? (booking && !isSkipped(booking) ? booking : null);
  const id = file.replace(/\.md$/, '');
  if (!page) {
    console.log(`- ${id}: 公式サイトのURLがないためスキップ（officialUrl: を書くと取得します）`);
    continue;
  }

  try {
    const imgUrl = direct ?? await findOgImage(page);
    const res = await fetch(imgUrl, { headers: UA });
    if (!res.ok) throw new Error(`画像取得失敗 ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    const meta = await sharp(buf).metadata();
    if ((meta.width ?? 0) < 400) throw new Error(`画像が小さすぎる（幅${meta.width}px）`);

    mkdirSync(OUT, { recursive: true });
    await sharp(buf).resize({ width: 1200, withoutEnlargement: true }).flatten({ background: '#ffffff' })
      .jpeg({ quality: 82, mozjpeg: true }).toFile(`${OUT}/${id}.jpg`);

    const lines = `image: /images/courts/${id}.jpg\nimageSource: ${direct ? (official ?? direct) : page}\n`;
    writeFileSync(path, text.replace(/^booking:/m, `${lines}booking:`));
    console.log(`✓ ${id}: ${imgUrl}`);
    added++;
  } catch (e) {
    console.log(`- ${id}: ${e.message}（${page}）`);
  }
}
console.log(`\n${added}件の画像を追加しました`);
