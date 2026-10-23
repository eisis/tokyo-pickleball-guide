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
const hideFromSitemap = (page) => {
  const path = new URL(page).pathname;
  if (/^\/(my-paddle|tokushoho|contact)\/$/.test(path)) return true; // 準備中・問い合わせページ
  const m = path.match(/^\/events\/([^/]+)\/$/);
  if (m && m[1] !== 'submit' && !selfEvents.has(m[1])) return true;
  return false;
};

export default defineConfig({
  site: 'https://www.pickleball-tokyo.com',
  // 準備中で非公開のページはサイトマップに載せない（公開するときはここから外す）
  integrations: [sitemap({ filter: (page) => !hideFromSitemap(page) })],
  markdown: {
    rehypePlugins: [rehypeArticle], // 記事のボックス・写真の説明・表（src/lib/rehype-article.mjs）
  },
});
