# Remove public `/projects` page

**Date:** 2026-08-12  
**Status:** approved for implementation  
**Decision:** Approach A — remove from the public site; do not soft-archive.

## Context

v2 shipped `/projects/` as the home for Know-Center-era research software and industry case studies (~20 items), after dropping “deployed systems” rows from the landing-page selected work. The page is linked from the masthead and from a CV summary tile.

That portfolio no longer matches the site’s job: lead of Team AIR, applied AI across several topics, with recommender systems still a research thread but not a consultancy case-study gallery. Papers, keywords, and career already carry RecSys credibility.

## Goals

- Stop presenting a Know-Center client/portfolio page as a primary destination.
- Keep old inbound links from breaking (`/projects.html`, and anyone who bookmarked `/projects`).
- Leave room for a future “shipped systems” story under `/air/` if Infobip work warrants it — not a revival of this portfolio.

## Non-goals

- Rewriting selected work or the AIR page.
- Migrating any case study into updates or publications.
- Soft-archiving an unlisted `/projects/` page.

## Changes

### Public surface

1. Delete `src/pages/projects.astro`.
2. Remove the `projects` item from `Masthead.astro` nav.
3. On `/cv/`, remove the “20 systems & case studies” tile that links to `/projects`.
4. Redirect both `/projects` and `/projects.html` to `/publications` (RecSys evidence lives with the papers).

### Data and schema

5. Delete `src/data/projects.yml`.
6. Remove the `projects` collection from `content.config.ts`.
7. Remove `getProjects` from `src/lib/content.ts` (and any related types/imports).

### Assets

8. Delete `public/images/apps/` (screenshots referenced only by projects). Leave the v1 tree’s copies alone until cutover.

### Docs

9. Update `docs/content-guide.md` and `README.md` to drop projects authoring.
10. Record the decision in `PLAN.md` (site map / selected-work note) and log the change in `ACTIVITY.md` when shipped.

## Redirects

| From | To |
|---|---|
| `/projects` | `/publications` |
| `/projects.html` | `/publications` |

Existing entry `/projects.html` → `/projects` in `astro.config.mjs` becomes `/projects.html` → `/publications`, plus an explicit `/projects` → `/publications` so the removed route does not 404 after deploy.

## Out of scope / later

- Any new production-systems section belongs under `/air/` when there is current work to show.
- RecSys remains in research keywords, publications, and career copy — unchanged by this work.

## Verification

- Build succeeds with no projects collection or page.
- Masthead and CV no longer link to `/projects`.
- `/projects` and `/projects.html` redirect to `/publications`.
- Sitemap / build output contain no `/projects` HTML page.
