/**
 * RSS feed at /feed.xml.
 *
 * Uses getPublishedPosts rather than getPosts, so a draft can never reach a
 * subscriber even if someone builds the site from a dirty working tree.
 */
import rss from '@astrojs/rss';
import type { APIRoute } from 'astro';
import { profile } from '../data/profile';
import { getPublishedPosts } from '../lib/content';

export const GET: APIRoute = async (context) => {
  const posts = await getPublishedPosts();

  return rss({
    title: `${profile.name} — updates`,
    description:
      'Field notes, deep dives and paper notes on applied AI research: recommender systems, generative models, evaluation, and what survives production.',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.standfirst,
      pubDate: post.data.date,
      link: `/updates/${post.id}/`,
      categories: [post.data.type, ...post.data.tags],
    })),
    customData: '<language>en-gb</language>',
  });
};
