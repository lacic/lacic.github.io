# Updating the site

Everything on this site comes from files in `src/`. There is no CMS and no admin login: you edit a
file, check it locally, and push.

Start the dev server once and leave it running while you work — it reloads on save, and it shows
drafts:

```bash
npm run dev      # http://localhost:4321
```

**Contents**

- [The one rule](#the-one-rule)
- [Writing a blog post](#writing-a-blog-post)
- [Adding a paper](#adding-a-paper)
- [Adding a talk](#adding-a-talk)
- [Adding a project or case study](#adding-a-project-or-case-study)
- [Adding academic service](#adding-academic-service)
- [Career, education, funding, awards, keywords](#career-education-funding-awards-keywords)
- [The AIR research areas](#the-air-research-areas)
- [Publishing](#publishing)
- [When the build fails](#when-the-build-fails)

---

## The one rule

**If the build passes, the content is valid.** Every content file is checked against a schema in
`src/content.config.ts` when the site builds. A misspelled venue kind, a missing date, a paper note
pointing at a paper that does not exist — all of these stop the build with a message naming the file
and the field.

So you never have to remember the allowed values. Guess, run `npm run dev`, and the error will tell
you. That is what it is for.

---

## Writing a blog post

### Create it

```bash
uv run scripts/new_post.py "Why our A/B test disagreed with the offline evaluation"
```

That writes `src/content/updates/2026-08-14-why-our-ab-test-disagreed/index.md` with the frontmatter
filled in and `draft: true`. Open the printed URL and write. The scaffold exists so you never
hand-write frontmatter or stare at an empty file.

Options:

```bash
--type deep-dive              # field-note (default) | deep-dive | paper-note
--date 2026-09-01             # defaults to today
--tags evaluation,real-time
--series "Semantic Scholar MCP" --part 3
```

### The frontmatter

```yaml
---
title: Why our A/B test disagreed with the offline evaluation
standfirst: The offline metric said the new ranker was 8% better. Online it lost. The gap was in how we sampled negatives.
date: 2026-08-14
type: field-note
tags: [evaluation, recommender-systems]
draft: true
---
```

| Field | Notes |
| --- | --- |
| `title` | Plain. It appears in the index, the tab title and the link preview. |
| `standfirst` | **The field worth rewriting until it is good.** One sentence. It is the index entry, the social preview and the reader's decision to keep reading. |
| `date` | `YYYY-MM-DD`. Controls ordering. |
| `type` | `field-note`, `deep-dive` or `paper-note`. See below. |
| `tags` | Free-form. This is where the actual subject lives. Tag `air` to have a post appear on the AIR page. |
| `draft` | `true` while writing. Flip to `false` to publish. |
| `series` | Optional: `{ name, part }`. Adds part-to-part navigation. |
| `canonical` | Optional. Set to the `research.infobip.com` URL when cross-posting. |

### Which type?

The three types are a closed set because each one changes the page: a deep dive gets a table of
contents and series navigation, a paper note gets the paper's links and citation box. Tags are open,
so the subject is never constrained by the type.

**If a post fits none of them, it is a field note.** That is the default, not a decision.

To attach a paper to a post, add `paper: <publication-id>` — the post then shows that paper's PDF,
poster and citation at the end.

### Images

Put them in the post's own folder and reference them relatively:

```
src/content/updates/2026-08-14-why-our-ab-test-disagreed/
  index.md
  offline-vs-online.png
```

```markdown
![Offline gain against online outcome, by negative-sampling strategy](./offline-vs-online.png)
```

A post is a folder rather than a file precisely so this works. The post stays self-contained, moves
as a unit, and no shared uploads directory fills up with orphaned images.

Always write real alt text. `![](...)` on a chart makes the post useless to a screen reader and to
Google.

### Publishing it

Set `draft: false`, then commit and push. Drafts are visible in `npm run dev` and excluded from the
production build, the index, the sitemap and the RSS feed — so an unfinished post is genuinely
invisible and you can write it across several sittings.

---

## Adding a paper

```bash
uv run scripts/add_paper.py documents/2026_RecSys_llm_ranking.pdf
```

The script reads the PDF, extracts the metadata with an LLM, cross-checks it against Crossref,
proposes an entry for `src/data/publications.yml`, and — after you confirm — writes it along with a
plain-language note in `src/content/paper-notes/`.

Add `--dry-run` to see the proposed entry without writing anything, or `--no-summary` to skip
generating the note.

### Then check it, because the entry is machine-extracted

The script sets `needsReview: true`, which renders a visible `needs review` marker next to the paper.
That marker is there to annoy you into checking. Three things are commonly wrong:

1. **Your surname.** It must be `Lacić`. Extraction sometimes returns `Lacic`, and the diacritic ends
   up in everyone's bibliography once someone copies the citation.
2. **`venue.kind`.** A workshop paper extracted as `conference` misfiles the paper for good. If it is
   a workshop, also set `colocatedWith`.
3. **Author order and initials.** Compare against the PDF's title page.

Clear `needsReview` (delete the line or set it to `false`) once you have checked. Never ship `true`.

### The fields

```yaml
- id: 2026-recsys-llm-ranking            # permanent — this is the paper's URL
  title: "Ranking with Language Models: What Survives Production"
  authors: ["Lacić, E.", "Someone, A."]
  year: 2026
  venue:
    name: RecSys                          # short, as a peer would say it
    full: 20th ACM Conference on Recommender Systems   # for the citation
    kind: conference                      # see the list below
    publisher: ACM
    pages: "123-134"                      # optional
    colocatedWith: RecSys 2026            # workshops only
  pdf: /documents/2026_RecSys_llm_ranking.pdf
  poster: /documents/posters/2026_RecSys_llm_ranking_poster.pdf
  doi: 10.1145/1234567.1234568
  areas: [recommender-systems, generative-ai]
  selected: false
  needsReview: false
```

`kind` is one of: `conference`, `journal`, `workshop`, `book-chapter`, `demo`, `thesis`,
`newsletter`, `industry`, `preprint`.

`areas` are the filter tags on `/publications`: `recommender-systems`, `information-retrieval`,
`fairness-bias`, `real-time`, `social-networks`, `learning-analytics`, `evaluation`, `health`,
`generative-ai`. Only tag what the paper is actually about — a tag that matches everything filters
nothing.

**`id` is permanent.** It is the paper's URL (`/publications/<id>`) and what paper notes and projects
reference. Renaming it breaks both, so pick it once.

You never write BibTeX or APA. Both are generated from these fields, which is why a corrected venue
cannot leave a stale citation behind.

### The plain-language note

`src/content/paper-notes/<name>.md`:

```markdown
---
paper: 2026-recsys-llm-ranking
---

# Ranking with Language Models

## What we did
...
```

The note gives the paper a page that is not a PDF, so a reader can find out what it says before
committing to reading it. `paper:` must match an existing publication `id` or the build fails.

The H1 is hidden on the page (the page already has the title as its heading) — keep it, since it
makes the file readable on its own.

Notes are generated by `scripts/summarize_papers.py`, so they read like an LLM by default. They are
worth editing: the useful sentence is usually the one about what did *not* work.

### Putting a paper in "Selected work"

The landing page shows five papers, controlled by two fields:

```yaml
selected: true
selectedRank: 3      # 1 comes first
```

Keep it to five, and remove a paper when you add one. The section is a claim about what matters most,
and it stops being a claim at ten items.

---

## Adding a talk

`src/data/talks.yml`:

```yaml
- id: shift-2026-zadar
  title: "What survives production"
  event: Infobip Shift 2026
  location: Zadar, Croatia
  date: 2026-09-16
  kind: talk                 # keynote | talk | panel | tutorial | invited | chair
  slides: /documents/talks/Infobip_Shift_2026.pdf
  video: https://youtube.com/watch?v=...
  url: https://shift.infobip.com/
  description: >-
    Two or three sentences on what the talk argued.
```

Put slide PDFs in `documents/talks/` at the repository root; they are served from
`/documents/talks/...`. Only `id`, `title`, `event` and `date` are required.

---

## Adding a project or case study

`src/data/projects.yml`:

```yaml
- id: some-system
  title: Some System
  kind: case-study           # software | case-study
  summary: >-
    ONE concrete sentence: what the system did, in plain terms.
  detail: >-
    Optional. One to three sentences of extra detail.
  years: "2024-2025"
  partner: Client name
  image: /images/apps/some_system.png
  papers: [2026-recsys-llm-ranking]     # optional, links to publications
  featured: true                         # case studies only: shown first
```

Use `kind: software` for a named tool or framework, `case-study` for applied work with a partner.

Write `summary` as what the system did, not what it enabled or transformed. The v1 page read as a
consultancy portfolio; the interesting claim is narrower and stronger — these systems ran in
production and are why several of the papers exist.

Three case studies migrated from v1 are marked `PLACEHOLDER - needs a real description` in `detail`,
because v1 had no text for them at all. Either write a real summary or delete the entry.

Images go in `images/apps/` at the repository root.

---

## Adding academic service

`src/data/service.yml`:

```yaml
- id: umap-pc
  category: programme-committee
  role: Programme Committee member
  venue: UMAP
  years: "2021-2022"
  detail: Best reviewer award, 2021.
  url: https://www.um.org/umap2022/
```

`category` is one of `programme-committee`, `reviewing`, `organising`, `editorial`, `chairing`,
`supervision`. Repeated service at the same venue belongs in one entry with a year range, not one
entry per year.

Co-supervised theses go here as `category: supervision`; they also appear on `/cv`.

---

## Career, education, funding, awards, keywords

These are singletons, so they live in TypeScript rather than YAML: `src/data/profile.ts`. Each block
has a comment explaining why it is shaped the way it is — worth reading before restructuring.

| What | Where in `profile.ts` |
| --- | --- |
| Name, role, email, links | `profile` |
| The three hero lines and the working note | `profile.statement`, `profile.workingNote` |
| The research keyword line | `profile.keywords` (six at most) |
| Bio used on `/cv` and in meta descriptions | `profile.bio` |
| Career | `career` |
| Education | `education` |
| Funding and fellowships | `funding` |
| Awards | `awards` |
| Languages | `languages` |

### Adding a job

`career` is grouped by organisation, not by role, so several roles at one employer stay together:

```ts
{
  org: 'Know-Center',
  place: 'Graz',
  span: '2016—2023',
  url: 'https://www.know-center.at/',
  roles: [
    { years: '2021—23', title: 'Operations Area Manager, Fair-AI', detail: '...' },
    { years: '2016—20', title: 'Senior Researcher', detail: '...' },
    { years: '2018', title: 'Visiting researcher, UCLA', concurrent: true, tag: 'visiting', detail: '...' },
  ],
}
```

- **A promotion** is a new entry in `roles`, newest first — not a new organisation.
- **A parallel engagement** (a visiting stay during a job) gets `concurrent: true`, which indents it
  and marks it as running alongside rather than after.
- `early: true` renders an organisation quietly. It is set on the pre-2013 roles so the recent work
  leads; the full history is still there.
- `current: true` adds the orange dot.

### Funding vs awards

They are separate blocks on purpose. An award says other people rated the work; funding says a
consortium and a budget were trusted to you. For someone leading an industrial research team the
second is the rarer signal, so funding appears on the landing page and awards only on `/cv`. Put
`amount` in `funding` only where the figure is public.

---

## The AIR research areas

Two things have to agree: the text list on `/air` and the generated image used on both the landing
page and `/air`.

1. Edit `researchAreas` in `src/data/profile.ts` (name, slug, summary).
2. Edit the matching tile in `tools/air/compose.html` — the label and, if it is a new area, the icon
   and its Infobip colour pair.
3. Regenerate the image:

```bash
npm run image     # requires Google Chrome; writes public/air-areas.png
```

4. Check the result. The labels must be in IBM Plex Sans, the same font as the page around them. If
   they render in a fallback, the webfont did not load and the render should be repeated.

The image is committed to the repository, so nobody needs Chrome to build the site. It exists as a
rendered PNG rather than inline SVG because the tiles need Infobip's real squircle shape
(CSS `corner-shape`), the icons come from `research.infobip.com` as masked SVGs, and the labels need
the site's webfont. Chrome already does all three correctly.

Keep the order in `profile.ts` matching the order in the image, since the numbered list on `/air`
reads as a key to it.

---

## Publishing

```bash
npm run check     # 0 errors expected
npm run build     # fails on invalid content
npm run preview   # look at it as it will be deployed
git add -A && git commit -m "Add post on offline vs online evaluation" && git push
```

Pushing to `main` builds and deploys via GitHub Actions, which takes a minute or two. If the build
fails, nothing is deployed and the current site stays up.

Before pushing, worth a look:

- The post reads well at mobile width (narrow the browser).
- No `needs review` marker is visible on `/publications`.
- New PDF links actually open.
- `standfirst` says something.

### Do not break URLs

Renaming a post folder or a publication `id` changes its URL and breaks every link to it. If you must
rename one, add a redirect in `astro.config.mjs`:

```js
redirects: {
  '/updates/old-slug': '/updates/new-slug',
}
```

Deleting a post is fine; leaving one at a URL that 404s is not.

---

## When the build fails

The error names the file and the field. The common ones:

**`Invalid enum value. Expected 'conference' | 'journal' | ...`**
A `kind` or `category` is misspelled. The message lists the allowed values.

**`Entry ... does not exist in collection "publications"`**
A paper note's `paper:` or a project's `papers:` points at an `id` that is not in
`publications.yml`. Usually a typo or a renamed id.

**`Required field: standfirst`**
Frontmatter is incomplete. Every post needs `title`, `standfirst` and `date`.

**`Expected type "date", received "string"`**
A date is not `YYYY-MM-DD`, or is quoted in a way YAML reads as text.

**A YAML parse error with a line number**
Almost always a value containing `:` that is not quoted, or inconsistent indentation. Wrap the value
in quotes, or use a `>-` block for anything long.

**The site builds but a post is missing**
It still has `draft: true`. That is the mechanism working.
