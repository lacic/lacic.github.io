# AIR team blog shout-out Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the Team AIR roster vertically and move Ante’s latest post into a soft invite band under the whole team.

**Architecture:** Keep RSS + `latestPost` fallback in page frontmatter; render one invite block after the team `<ul>`, not inside person cards. Top-align person grid cells so avatars/names share a row baseline.

**Tech Stack:** Astro page (`air.astro`), existing `formatMonth`, `fetchLatestFeedItem`, `airTeam` data.

**Spec:** `docs/superpowers/specs/2026-08-12-air-team-blog-shoutout-design.md`

---

### Task 1: Roster markup + invite band

**Files:**
- Modify: `v2/src/pages/air.astro`

- [x] Remove per-person `person-latest` from the team map.
- [x] After `</ul>`, if any latest post exists for Ante (from `latestByMember`), render invite band with copy: “Check out Ante’s blog — some of our ongoing research is updated there.” then date · linked title.
- [x] CSS: `.person { align-items: start; }`; remove `.person-latest*` rules; add `.team-invite` styles matching page stamps (quiet, not a card); extra top margin under `.team`.
- [x] Verify: `curl`/browser `/air` — four aligned people; invite below grid; no post inside Ante’s card.
- [ ] Commit only if the user asks.
