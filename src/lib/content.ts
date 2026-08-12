/**
 * Content queries live here so that every page, the index, the RSS feed and the
 * sitemap apply the same rules — in particular the draft rule.
 *
 * `draft: true` must mean genuinely invisible. A draft that leaks into the feed
 * is worse than no draft support at all, because you find out from a reader.
 */

import { getCollection, type CollectionEntry } from 'astro:content';

/** Drafts are visible while running `astro dev`, never in a production build. */
export const showDrafts = import.meta.env.DEV;

export async function getPosts(): Promise<CollectionEntry<'updates'>[]> {
  const posts = await getCollection('updates', ({ data }) => showDrafts || !data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** Published only, whatever the environment. Used by the RSS feed. */
export async function getPublishedPosts(): Promise<CollectionEntry<'updates'>[]> {
  const posts = await getCollection('updates', ({ data }) => !data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export async function getPublications(): Promise<CollectionEntry<'publications'>[]> {
  const pubs = await getCollection('publications');
  return pubs.sort((a, b) => {
    if (b.data.year !== a.data.year) return b.data.year - a.data.year;
    return a.data.title.localeCompare(b.data.title);
  });
}

/** The landing page shortlist, in the order set by `selectedRank`. */
export async function getSelectedPublications(): Promise<CollectionEntry<'publications'>[]> {
  const pubs = await getCollection('publications', ({ data }) => data.selected);
  return pubs.sort((a, b) => (a.data.selectedRank ?? 99) - (b.data.selectedRank ?? 99));
}

/** publication id -> paper-note id, for "what it says" links. */
export async function getNoteMap(): Promise<Map<string, string>> {
  const notes = await getCollection('paperNotes');
  return new Map(notes.map((note) => [note.data.paper.id, note.id]));
}

export async function getTalks(): Promise<CollectionEntry<'talks'>[]> {
  const talks = await getCollection('talks');
  return talks.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export async function getService(): Promise<CollectionEntry<'service'>[]> {
  return getCollection('service');
}
