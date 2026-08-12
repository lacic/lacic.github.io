/**
 * Minimal RSS helpers for build-time shout-outs (e.g. a teammate's latest blog post).
 * Kept dependency-free: one regex pass over the feed XML is enough for title/link/date.
 */

export type FeedItem = {
  title: string;
  link: string;
  date: Date;
};

function decodeXmlEntities(value: string): string {
  return value
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'");
}

function tagValue(block: string, tag: string): string | null {
  const match = block.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, 'i'));
  if (!match) return null;
  return decodeXmlEntities(match[1].trim());
}

/**
 * Latest item from an RSS 2.0 feed. Optionally keep only links under a path prefix
 * (e.g. `/blog/` so project pages in a mixed Hugo feed are skipped).
 * Returns null on network/parse failure so the page still builds.
 */
export async function fetchLatestFeedItem(
  feedUrl: string,
  options: { pathIncludes?: string } = {},
): Promise<FeedItem | null> {
  try {
    const response = await fetch(feedUrl, {
      headers: {
        Accept: 'application/rss+xml, application/xml, text/xml, */*',
        // Some hosts reject Node's default UA; a browser-like one is safer.
        'User-Agent': 'elacic.me-site-builder/1.0 (+https://elacic.me)',
      },
    });
    if (!response.ok) return null;

    const xml = await response.text();
    const items = xml.match(/<item\b[\s\S]*?<\/item>/gi) ?? [];
    for (const block of items) {
      const title = tagValue(block, 'title');
      const link = tagValue(block, 'link');
      const pubDate = tagValue(block, 'pubDate');
      if (!title || !link) continue;
      if (options.pathIncludes && !link.includes(options.pathIncludes)) continue;

      const date = pubDate ? new Date(pubDate) : new Date(NaN);
      return {
        title,
        link,
        date: Number.isNaN(date.valueOf()) ? new Date() : date,
      };
    }
    return null;
  } catch {
    return null;
  }
}
