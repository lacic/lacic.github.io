# AIR team roster + Ante blog invite

**Date:** 2026-08-12  
**Status:** approved; implementing

## Problem

The Team AIR roster misaligns when Ante’s latest post sits inside his card: avatars and name/role blocks no longer share a common vertical rhythm. The inline shout-out also feels like clutter rather than an invite.

## Goals

- Photos, names, and roles align across the first row (and any wrapped rows).
- Surface Ante’s latest blog post as a soft invite under the whole team.
- Copy should invite readers because some ongoing research is updated there.

## Non-goals

- Redesigning other `/air` sections.
- Multiple blog shout-outs or a full post list under the team.
- Changing RSS/fallback data plumbing beyond what the new placement needs.

## Design

### Roster

- Keep the existing responsive grid of four members.
- Each person card contains only: avatar, name, role, link row (`website · blog · Scholar` as available).
- Align person rows to the **top** (`align-items: start`) so avatars share a baseline across the row.
- Remove the per-person `person-latest` block from cards.

### Blog invite (below the grid)

- Place a single band under the team list, with slightly more top margin than the grid’s row gap.
- Soft invite framing (tone B):

  > **Check out Ante’s blog** — some of our ongoing research is updated there.  
  > *[month year]* · *[latest post title]* (title links to the post)

- Visual language: quiet stamp/label consistent with existing AIR stamps (`In practice`, rail heads); not a card, border box, or badge cluster.
- Data: prefer live RSS (`feed` + `/blog/` filter); fall back to committed `latestPost`; hide the whole band if neither is available.

## Success criteria

- On a typical desktop width, the four avatars and the four name/role stacks line up.
- Ante’s latest post is visible once, below the roster, with invite copy as above.
- Hard refresh of `/air` in local preview shows the band without needing the feed to succeed (fallback).
