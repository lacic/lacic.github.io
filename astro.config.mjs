// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { satteri } from '@astrojs/markdown-satteri';

/**
 * External links in Markdown open in a new tab, so a reader following a paper
 * citation does not lose their place in the post. Done here rather than in the
 * Markdown so posts stay plain `[text](url)`. Internal links are left alone.
 *
 * Written against Sätteri, Astro 7's default Markdown processor; rehype plugins
 * would need the separate unified pipeline installed.
 */
const externalLinksInNewTab = {
  name: 'external-links-new-tab',
  element: {
    filter: ['a'],
    /** @param {any} node @param {any} ctx */
    visit(node, ctx) {
      const href = node.properties?.href;
      if (typeof href !== 'string' || !/^https?:\/\//.test(href)) return;
      ctx.setProperty(node, 'target', '_blank');
      ctx.setProperty(node, 'rel', 'noopener noreferrer');
    },
  },
};

/**
 * Inline code that is a semantic ID, such as `<12><201><7>`, gets one span per
 * level so each depth keeps the same colour wherever it appears. Level n is
 * styled by `.sid-ln` in global.css; anything that is not purely `<digits>`
 * tokens is left as ordinary code.
 */
const semanticIdLevels = {
  name: 'semantic-id-levels',
  element: {
    filter: ['code'],
    /** @param {any} node @param {any} ctx */
    visit(node, ctx) {
      const text = ctx.textContent(node);
      if (!/^(<\d+>)+$/.test(text)) return;
      const tokens = text.match(/<\d+>/g) ?? [];
      ctx.setProperty(node, 'className', ['sid']);
      ctx.setProperty(
        node,
        'children',
        tokens.map((token, i) => ({
          type: 'element',
          tagName: 'span',
          properties: { className: [`sid-l${Math.min(i + 1, 4)}`] },
          children: [{ type: 'text', value: token }],
        })),
      );
    },
  },
};

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
    processor: satteri({ hastPlugins: [externalLinksInNewTab, semanticIdLevels] }),
  },
  devToolbar: { enabled: false },
});
