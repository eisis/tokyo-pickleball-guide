import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import rehypeArticle from './src/lib/rehype-article.mjs';
import { readdirSync, readFileSync } from 'node:fs';

// Pickleball Tokyo 主催のイベント（organizer の self: true）だけ検索・サイトマップに載せる。
// 他の主催者のイベント詳細ページは、主催者の公式ページと内容が重なるため検索には出さない（ページの robots と合わせる）
const selfEvents = new Set(
  readdirSync('./src/content/events')
    .filter((f) => f.endsWith('.md') && !f.startsWith('_'))
    .filter((f) => /\n\s*self:\s*true/.test(readFileSync(`./src/content/events/${f}`, 'utf8')))
    .map((f) => f.replace(/\.md$/, '')),
);
// 期間限定で営業が終わったコート（closesAt が過ぎたもの）は、ページは残すが検索には出さない（ページ側も noindex）
const today = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
const closedCourts = new Set(
  readdirSync('./src/content/courts')
    .filter((f) => f.endsWith('.md') && !f.startsWith('_'))
    .filter((f) => {
      const m = readFileSync(`./src/content/courts/${f}`, 'utf8').match(/^closesAt:\s*(\d{4}-\d{2}-\d{2})/m);
      return m && m[1] < today;
    })
    .map((f) => f.replace(/\.md$/, '')),
);
const hideFromSitemap = (page) => {
  const path = new URL(page).pathname;
  if (/^\/(my-paddle|tokushoho|contact)\/$/.test(path)) return true; // 準備中・問い合わせページ
  const c = path.match(/^\/courts\/([^/]+)\/$/);
  if (c && closedCourts.has(c[1])) return true;
  const m = path.match(/^\/events\/([^/]+)\/$/);
  if (m && m[1] !== 'submit' && !selfEvents.has(m[1])) return true;
  return false;
};

// サイトマップの更新日（lastmod）：コート・イベント・記事は、ファイルに書いた確認日・更新日を使う
const lastmodOf = (dir, key) => {
  const map = new Map();
  for (const f of readdirSync(dir).filter((f) => f.endsWith('.md') && !f.startsWith('_'))) {
    const t = readFileSync(`${dir}/${f}`, 'utf8');
    const v = key.map((k) => t.match(new RegExp(`^${k}:\\s*(\\d{4}-\\d{2}-\\d{2})`, 'm'))?.[1]).find(Boolean);
    if (v) map.set(f.replace(/\.md$/, ''), v);
  }
  return map;
};
const LASTMOD = {
  courts: lastmodOf('./src/content/courts', ['updatedAt']),
  events: lastmodOf('./src/content/events', ['updatedAt']),
  blog: lastmodOf('./src/content/posts', ['updatedAt', 'publishedAt']),
};

export default defineConfig({
  site: 'https://www.pickleball-tokyo.com',
  // 準備中で非公開のページはサイトマップに載せない（公開するときはここから外す）
  integrations: [
    sitemap({
      filter: (page) => !hideFromSitemap(page),
      serialize(item) {
        const m = new URL(item.url).pathname.match(/^\/(courts|events|blog)\/([^/]+)\/$/);
        const d = m && LASTMOD[m[1]].get(decodeURIComponent(m[2]));
        if (d) item.lastmod = new Date(d + 'T00:00:00+09:00').toISOString();
        return item;
      },
    }),
  ],
  markdown: {
    rehypePlugins: [rehypeArticle], // 記事のボックス・写真の説明・表（src/lib/rehype-article.mjs）
  },
});
