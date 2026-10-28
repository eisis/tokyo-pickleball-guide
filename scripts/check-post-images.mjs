// ビルド前のチェック：記事の画像が、どこに出しても16:9の枠にきれいに収まるか
//  1. 文字入りの縦長の表紙（coverFit: contain）の記事には、横長の banner が必要
//  2. banner は 16:9（1600×900 を推奨）
//  3. 指定した画像ファイルが存在する
// 問題があればエラーで止める（Vercel の公開も止まる）。使い方：npm run check:images
import { readFileSync, readdirSync, existsSync, openSync, readSync, closeSync } from 'node:fs';
import { join } from 'node:path';
import { parse } from 'yaml';

const ROOT = new URL('..', import.meta.url).pathname;
const POSTS = join(ROOT, 'src/content/posts');
const RATIO = 16 / 9;

function size(file) { // PNG / JPEG の縦横を、ヘッダーだけ読んで調べる
  const fd = openSync(file, 'r'); const b = Buffer.alloc(65536); readSync(fd, b, 0, b.length, 0); closeSync(fd);
  if (b.readUInt32BE(0) === 0x89504e47) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  if (b[0] === 0xff && b[1] === 0xd8) {
    for (let i = 2; i < b.length - 9;) {
      if (b[i] !== 0xff) { i++; continue; }
      const m = b[i + 1], len = b.readUInt16BE(i + 2);
      if (m >= 0xc0 && m <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(m)) return { w: b.readUInt16BE(i + 7), h: b.readUInt16BE(i + 5) };
      i += 2 + len;
    }
  }
  return null;
}

const errors = [];
for (const f of readdirSync(POSTS).filter((f) => f.endsWith('.md') && !f.startsWith('_'))) {
  const m = readFileSync(join(POSTS, f), 'utf8').match(/^---\n([\s\S]*?)\n---/);
  if (!m) continue;
  const d = parse(m[1]) ?? {};
  for (const key of ['cover', 'banner']) {
    if (d[key] && !existsSync(join(ROOT, 'public', d[key]))) errors.push(`${f}: ${key} のファイルがありません（${d[key]}）`);
  }
  if (d.coverFit === 'contain' && !d.banner) {
    errors.push(`${f}: 文字入りの表紙（coverFit: contain）には、記事一覧用の横長の banner が必要です（social/instagram/scripts/banner.py で作れます）`);
  }
  if (d.banner && existsSync(join(ROOT, 'public', d.banner))) {
    const s = size(join(ROOT, 'public', d.banner));
    if (!s) errors.push(`${f}: banner の大きさを読めません（PNGかJPEGにしてください）`);
    else if (Math.abs(s.w / s.h - RATIO) > 0.01) errors.push(`${f}: banner が16:9ではありません（${s.w}×${s.h}）。1600×900 で作ってください`);
  }
}

if (errors.length) {
  console.error('\n記事の画像チェックで問題が見つかりました：\n' + errors.map((e) => '  - ' + e).join('\n') + '\n');
  process.exit(1);
}
console.log('記事の画像チェック：OK');
