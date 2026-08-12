# Team AIR publication flag

**Status:** approved  
**Date:** 2026-08-12

## Problem

Topic `areas` describe what a paper is about. Infobip / Team AIR is where it came from. Those must not share one vocabulary if publications filtering and the AIR page both need a reliable query.

## Decision

Add a dedicated boolean on each publication:

```yaml
air: true
```

Missing or `false` means not an AIR / Infobip research outcome.

## Detection

When adding a paper, propose `air: true` if the PDF front matter contains:

- an author email matching `@infobip.com`, or
- a clear Infobip affiliation line (`Infobip`)

Always reviewable by hand (clear or set the flag).

## Surfaces

1. **`/publications`** — a separate **Team AIR** filter chip (not a topic tag), visually distinct; papers with `air: true` show a small Team AIR pill. Deep link: `/publications#air`.
2. **`/air` intro rail** — latest three `air: true` papers on the right, with “all Team AIR →” linking to `/publications#air`.
3. **`/air` (later)** — fuller research-outcomes section if needed; data query is already `papers.filter(p => p.data.air)`.

## Out of scope here

Building the AIR outcomes section UI (data + publications filter only).
