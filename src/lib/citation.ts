/**
 * BibTeX and APA strings, generated from the publication record.
 *
 * These are derived rather than stored so a corrected venue or author cannot
 * end up disagreeing with the citation someone pastes into their paper. If a
 * citation looks wrong, fix src/data/publications.yml and both change together.
 */

import type { CollectionEntry } from 'astro:content';
import { profile } from '../data/profile';

type Publication = CollectionEntry<'publications'>['data'];

const STOPWORDS = new Set(['a', 'an', 'the', 'and', 'or', 'of', 'for', 'in', 'on', 'with', 'to']);

/** Is this author string one of your own name forms? */
export function isSelf(author: string): boolean {
  return profile.surnameForms.some((form) => author.startsWith(form));
}

/** "Lacić, E." -> "Lacić" */
function surname(author: string): string {
  return (author.split(',')[0] ?? author).trim();
}

/** Latin-1 down-conversion, so diacritics do not break a plain LaTeX build. */
function toLatex(text: string): string {
  const map: Record<string, string> = {
    ć: "\\'{c}", Ć: "\\'{C}",
    č: '\\v{c}', Č: '\\v{C}',
    š: '\\v{s}', Š: '\\v{S}',
    ž: '\\v{z}', Ž: '\\v{Z}',
    đ: '\\dj{}', Đ: '\\DJ{}',
    ä: '\\"{a}', ö: '\\"{o}', ü: '\\"{u}',
    Ä: '\\"{A}', Ö: '\\"{O}', Ü: '\\"{U}',
    ß: '\\ss{}',
    é: "\\'{e}", è: '\\`{e}', ë: '\\"{e}',
    á: "\\'{a}", à: '\\`{a}',
    í: "\\'{i}", ó: "\\'{o}", ú: "\\'{u}",
    ñ: '\\~{n}', ç: '\\c{c}',
  };
  return text.replace(/[^\u0000-\u007F]/g, (ch) => map[ch] ?? ch);
}

/** e.g. lacic2023uptrendz */
export function citeKey(pub: Publication): string {
  const first = surname(pub.authors[0] ?? 'anon')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z]/g, '');
  const word =
    pub.title
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .split(/[\s-]+/)
      .find((w) => w.length > 3 && !STOPWORDS.has(w)) ?? 'paper';
  return `${first}${pub.year}${word}`;
}

const BIBTEX_TYPE: Record<Publication['venue']['kind'], string> = {
  conference: 'inproceedings',
  workshop: 'inproceedings',
  demo: 'inproceedings',
  industry: 'inproceedings',
  journal: 'article',
  newsletter: 'article',
  'book-chapter': 'incollection',
  thesis: 'phdthesis',
  preprint: 'misc',
};

/**
 * The container title as a citation wants it.
 *
 * publications.yml stores venue names the way a peer says them ("45th European
 * Conference on Information Retrieval"), but a proceedings citation needs
 * "Proceedings of the ...". Deriving it here keeps the data readable and the
 * citation correct, instead of forcing one of the two to be wrong.
 */
function containerTitle(pub: Publication): string {
  const name = pub.venue.full ?? pub.venue.name;
  const isProceedings = ['conference', 'workshop', 'demo', 'industry'].includes(pub.venue.kind);
  if (!isProceedings || /^(proceedings|extended|companion|adjunct)/i.test(name)) return name;
  return `Proceedings of the ${name.replace(/^the\s+/i, '')}`;
}

export function toBibtex(pub: Publication): string {
  const kind = pub.venue.kind;
  const entryType = BIBTEX_TYPE[kind];
  const container = containerTitle(pub);

  const fields: [string, string | undefined][] = [
    ['title', pub.title],
    ['author', pub.authors.join(' and ')],
    ['year', String(pub.year)],
  ];

  if (entryType === 'inproceedings') {
    fields.push(['booktitle', container]);
  } else if (entryType === 'incollection') {
    fields.push(['booktitle', container]);
  } else if (entryType === 'phdthesis') {
    fields.push(['school', pub.venue.publisher ?? container]);
  } else if (entryType === 'article') {
    fields.push(['journal', container]);
    fields.push(['volume', pub.venue.volume]);
  } else {
    fields.push(['howpublished', container]);
  }

  fields.push(['pages', pub.venue.pages]);
  fields.push(['publisher', pub.venue.publisher]);
  fields.push(['doi', pub.doi]);
  fields.push(['url', pub.url ?? (pub.doi ? `https://doi.org/${pub.doi}` : undefined)]);

  const body = fields
    .filter((entry): entry is [string, string] => Boolean(entry[1]))
    .map(([key, value]) => `  ${key} = {${toLatex(value)}},`)
    .join('\n');

  return `@${entryType}{${citeKey(pub)},\n${body}\n}`;
}

/** APA 7th: up to 20 authors, ampersand before the last. */
function apaAuthors(authors: string[]): string {
  const list = authors.map((a) => a.replace(/\s+/g, ' ').trim());
  if (list.length === 1) return list[0]!;
  if (list.length === 2) return `${list[0]}, & ${list[1]}`;
  if (list.length <= 20) {
    return `${list.slice(0, -1).join(', ')}, & ${list.at(-1)}`;
  }
  return `${list.slice(0, 19).join(', ')}, ... ${list.at(-1)}`;
}

export function toApa(pub: Publication): string {
  const container = containerTitle(pub);
  const parts = [`${apaAuthors(pub.authors)} (${pub.year}). ${pub.title}.`];

  if (pub.venue.kind === 'journal' || pub.venue.kind === 'newsletter') {
    const volume = pub.venue.volume ? `, ${pub.venue.volume}` : '';
    const pages = pub.venue.pages ? `, ${pub.venue.pages}` : '';
    parts.push(`${container}${volume}${pages}.`);
  } else if (pub.venue.kind === 'thesis') {
    parts.push(`[Doctoral dissertation, ${pub.venue.publisher ?? container}].`);
  } else {
    const pages = pub.venue.pages ? ` (pp. ${pub.venue.pages})` : '';
    parts.push(`In ${container}${pages}.`);
    if (pub.venue.publisher) parts.push(`${pub.venue.publisher}.`);
  }

  if (pub.doi) parts.push(`https://doi.org/${pub.doi}`);
  else if (pub.url) parts.push(pub.url);

  return parts.join(' ');
}

/** "ECIR 2023 · workshop paper" style line for list rows. */
export function venueLine(pub: Publication): string {
  const bits = [`${pub.venue.name} ${pub.year}`];
  if (pub.venue.kind === 'workshop' && pub.venue.colocatedWith) {
    bits.push(`workshop @ ${pub.venue.colocatedWith}`);
  } else if (pub.venue.kind !== 'conference') {
    bits.push(pub.venue.kind.replace('-', ' '));
  }
  return bits.join(' · ');
}
