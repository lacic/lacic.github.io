// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://elacic.me',
  // No `base`: this is a user site served from the domain root. PDF and image
  // URLs under /documents/ and /images/ must keep resolving exactly as they do
  // on v1, so those directories live in public/ unchanged.
  output: 'static',
  trailingSlash: 'ignore',

  /**
   * v1 loaded its sections as HTML fragments, but each fragment was also a real,
   * crawlable URL. Anything Google indexed or anyone bookmarked keeps working,
   * because a rebuild is not a reason to break someone else's link.
   *
   * PDF and image URLs are unchanged — those files sit in public/ untouched —
   * so no redirect is needed for them.
   */
  redirects: {
    // No entry for /index.html: the host already serves that as the root page,
    // and adding a redirect makes Astro emit a dist/index.html *directory*,
    // which then collides with the real homepage.
    '/main_pubs.html': '/publications',
    '/selected_pubs.html': '/publications',
    '/projects': '/publications',
    '/projects.html': '/publications',
    '/services.html': '/service',
    '/speaking.html': '/talks',
    '/experience.html': '/cv',
    '/resume.html': '/cv',
    '/sidebar.html': '/cv',
  },

  integrations: [sitemap()],
  markdown: {
    shikiConfig: { theme: 'github-light', wrap: true },
  },
  devToolbar: { enabled: false },
});
