import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://tokyo-pickleball-guide.vercel.app',
  integrations: [sitemap()],
});
