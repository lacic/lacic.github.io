/** Shared formatting helpers, so dates and labels read the same everywhere. */

const DAY = new Intl.DateTimeFormat('en-GB', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  timeZone: 'UTC',
});

const MONTH = new Intl.DateTimeFormat('en-GB', {
  month: 'short',
  year: 'numeric',
  timeZone: 'UTC',
});

/** "14 Aug 2026" */
export function formatDay(date: Date): string {
  return DAY.format(date);
}

/** "Aug 2026" */
export function formatMonth(date: Date): string {
  return MONTH.format(date);
}

/** For <time datetime=""> */
export function isoDay(date: Date): string {
  return date.toISOString().slice(0, 10);
}

export function typeLabel(type: 'field-note' | 'deep-dive' | 'paper-note'): string {
  return { 'field-note': 'Field note', 'deep-dive': 'Deep dive', 'paper-note': 'Paper note' }[type];
}

/** Rough reading time. Deliberately coarse: it is a hint, not a measurement. */
export function readingTime(body: string): string {
  const words = body.trim().split(/\s+/).length;
  return `${Math.max(1, Math.round(words / 220))} min read`;
}

/** Human labels for publication area slugs used on /publications.
 *
 * Areas are an open vocabulary discovered from publications.yml. Most labels
 * are derived by replacing hyphens; this map is only for awkward cases.
 */
const AREA_LABEL_OVERRIDES: Record<string, string> = {
  'fairness-bias': 'fairness & bias',
  'generative-ai': 'generative AI',
  'voice-ai': 'voice AI',
  'conversational-ai': 'conversational AI',
};

export function areaLabel(area: string): string {
  if (AREA_LABEL_OVERRIDES[area]) return AREA_LABEL_OVERRIDES[area];
  return area.replace(/-/g, ' ');
}
