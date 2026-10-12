import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.pickleball-tokyo.com',
  integrations: [sitemap()],
});
