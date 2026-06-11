import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import preact from '@astrojs/preact';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  integrations: [mdx(), preact({ compat: true })],
  vite: {
    plugins: [tailwindcss()],
  },
  site: 'https://wenpengcheng0413.github.io',
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
  prefetch: {
    prefetchAll: true,
  },
});
