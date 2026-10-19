import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import rehypeArticle from './src/lib/rehype-article.mjs';

export default defineConfig({
  site: 'https://www.pickleball-tokyo.com',
  // 準備中で非公開のページはサイトマップに載せない（公開するときはここから外す）
  integrations: [sitemap({ filter: (page) => !/\/(my-paddle|tokushoho)\/$/.test(page) })],
  markdown: {
    rehypePlugins: [rehypeArticle], // 記事のボックス・写真の説明・表（src/lib/rehype-article.mjs）
  },
});
