---
name: elacic.me
description: Precise, calm lab-notebook visual system for a research-led personal site.
colors:
  accent: "#fc6423"
  accentInk: "#b83f0c"
  paper: "#fbfcfd"
  grid: "#edf1f4"
  ink: "#1b1a19"
  pencil: "#6d6c6c"
  rule: "rgba(27, 26, 25, 0.16)"
  ruleSoft: "rgba(27, 26, 25, 0.09)"
  ink70: "rgba(27, 26, 25, 0.74)"
typography:
  display:
    fontFamily: "IBM Plex Sans, system-ui, -apple-system, sans-serif"
    fontSize: "clamp(1.85rem, 5.1vw, 3.15rem)"
    fontWeight: 500
    lineHeight: 1.14
    letterSpacing: "-0.024em"
  headline:
    fontFamily: "IBM Plex Sans, system-ui, -apple-system, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 600
    lineHeight: 1.16
    letterSpacing: "-0.018em"
  title:
    fontFamily: "IBM Plex Sans, system-ui, -apple-system, sans-serif"
    fontSize: "1.13rem"
    fontWeight: 600
    lineHeight: 1.16
    letterSpacing: "-0.018em"
  body:
    fontFamily: "IBM Plex Serif, Georgia, serif"
    fontSize: "1.06rem"
    fontWeight: 400
    lineHeight: 1.68
    letterSpacing: "normal"
  label:
    fontFamily: "IBM Plex Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "11.5px"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.09em"
rounded:
  none: "0px"
  sm: "2px"
  pill: "9999px"
  circle: "50%"
spacing:
  xs: "0.45rem"
  sm: "0.9rem"
  md: "1.4rem"
  lg: "1.75rem"
  xl: "2.25rem"
  "2xl": "3.5rem"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.68em 1.05em"
  button-primary-hover:
    backgroundColor: "{colors.accentInk}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.68em 1.05em"
  action-link:
    backgroundColor: "transparent"
    textColor: "{colors.pencil}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.34em 0.58em"
  nav-link:
    backgroundColor: "transparent"
    textColor: "{colors.pencil}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0"
  tag:
    backgroundColor: "transparent"
    textColor: "{colors.ink70}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.25em 0.5em"
  pill:
    backgroundColor: "transparent"
    textColor: "{colors.pencil}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.1em 0.4em"
  avatar:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.circle}"
    size: "112px"
---

# Design System: elacic.me

## Overview

**Creative North Star: "Lab Notebook"**

This system reads like a working notebook laid on a paper grid: careful, legible, and built from evidence rather than flourish. The page is a white sheet over a faint graph field, so the structure feels precise before the content even begins. The single accent orange is kept rare and deliberate, used to mark action, state, and emphasis instead of becoming the page’s mood.

Typography does the heavy lifting. IBM Plex Sans carries the hierarchy and the section structure, IBM Plex Serif gives the longer reading passages a calm editorial cadence, and IBM Plex Mono handles labels, metadata, and navigation with quiet authority. The overall effect is technical but not cold, academic but not formalist, and calm without going soft.

**Key Characteristics:**
- White paper sheet on a subtle grid.
- One rare accent color, never a flood.
- Sans / serif / mono roles with clear separation.
- Thin rules, dotted underlines, and generous whitespace.

## Colors

The palette is restrained and evidence-first: neutral paper and ink carry the interface, while the orange accent only wakes up important states.

### Primary
- **Accent orange** (#fc6423): the site’s active signal for CTAs, focus emphasis, separators, and AIR identity markers.

### Neutral
- **Paper white** (#fbfcfd): the main sheet background and reading surface.
- **Grid mist** (#edf1f4): the notebook-style canvas behind the sheet.
- **Ink black** (#1b1a19): primary text, the wordmark, and strong contrast surfaces.
- **Pencil grey** (#6d6c6c): secondary text, metadata, and quiet navigation.
- **Rule grey** (rgba(27, 26, 25, 0.16)): the default border and divider tone.
- **Soft rule grey** (rgba(27, 26, 25, 0.09)): lighter separators and subtle structural lines.
- **Ink 70** (rgba(27, 26, 25, 0.74)): body-adjacent secondary text when a softer tone is needed.

### Named Rules
**The Accent Is Rare Rule.** The orange accent is reserved for actions, active states, and small structural cues. It should feel like a highlight in a notebook, not a background color.

**The Grid Is Structural Rule.** The grid is a working-surface cue, not decoration. It should stay faint enough that content always wins.

## Typography

**Display Font:** IBM Plex Sans (with system-ui, -apple-system, sans-serif fallback)
**Body Font:** IBM Plex Serif (with Georgia, serif fallback)
**Label/Mono Font:** IBM Plex Mono (with ui-monospace, SFMono-Regular, Menlo fallback)

**Character:** The sans face gives the page its backbone, the serif face slows the reader down for sustained reading, and the mono face keeps the metadata and navigation crisp. The pairing feels practical, research-led, and composed.

### Hierarchy
- **Display** (500, clamp(1.85rem, 5.1vw, 3.15rem), 1.14): hero headlines and the first read on the page.
- **Headline** (600, 1.4rem, 1.16): section headings and other structural titles.
- **Title** (600, 1.13rem, 1.16): local titles inside lists and grouped records.
- **Body** (400, 1.06rem, 1.68): reading copy and explanatory text; keep the measure generous and relaxed.
- **Label** (500, 11.5px, 0.09em, uppercase): nav, metadata, button text, and notation.

### Named Rules
**The Measure Rule.** Body text should stay readable and unhurried; the prose measure lives in the comfortable editorial range rather than a dense dashboard width.

## Layout

The page is a centered paper sheet with a maximum width of 1140px, sitting on a faint 26px grid. Sections are separated by thin rules, and content blocks use generous internal padding rather than nested card stacks. The landing page is intentionally two-column in places — hero, AIR, and CV sections — then collapses to a single column below the mid-size breakpoint where clarity matters more than side-by-side density.

Spacing is roomy but not airy: blocks use roughly 2.25rem to 3.5rem of padding, section headers keep the reading order explicit, and small metadata groups are tightly packed. The layout feels like a dossier assembled on a workbench: orderly, low-drama, and easy to scan.

## Elevation & Depth

The system is flat by design. It does not use drop shadows, glass, or blur for depth. Separation comes from the paper sheet, the surrounding grid, 1px borders, dotted rules, and whitespace. Hover and focus states shift opacity and border color rather than lifting surfaces.

### Named Rules
**The Flat Sheet Rule.** Surfaces stay flat at rest. If a layer needs emphasis, give it contrast or structure before reaching for visual lift.

## Shapes

The shape language is disciplined and mostly rectangular. The outer sheet is square-cornered, section blocks are straight-edged, and most controls sit inside thin bordered boxes. The only deliberate circle is the portrait/avatar, which softens the otherwise technical composition and keeps the identity block human.

### Named Rules
**The Square-First Rule.** The default shape is a rectangle with no decorative rounding. Rounded geometry is reserved for the portrait and small, token-like accents.

## Components

Each component is understated, legible, and built to disappear into the reading experience until it needs to speak.

### Buttons
Primary actions use a dark solid fill with light text and a small orange arrow cue. Smaller action links use a bordered, mono-label treatment so they feel like utility controls rather than marketing buttons.
- **Primary button:** solid ink background, paper text, mono label, compact padding, no rounding.
- **Hover / Focus:** the fill shifts to accent ink, border cues strengthen, and the arrow remains a small orange signal.

### Navigation
Top and bottom navigation are quiet and textual. The masthead wordmark is mono and uppercase; nav links are dotted by default and solid only when active or hovered. Mobile navigation stacks cleanly rather than compressing into a dense toolbar.
- **Style:** mono labels, thin dotted underlines, restrained contrast.
- **Active state:** orange underline for the current page.

### Metadata Tokens
Tags and pills are low-noise, single-line labels for secondary structure and status.
- **Tag:** thin outline, neutral text, no fill.
- **Pill:** uppercase mono token with an outlined chip feel.
- **Use:** section metadata, labels, and compact supporting cues.

### Containers
The sheet, section blocks, and figure frames form the main container language. They are bounded by rules rather than shadows, and their job is to keep the page readable under a broad range of content lengths.
- **Sheet:** white background, thin border, centered within the page grid.
- **Blocks:** generous padding, full-width in the sheet, no nested card stacks.

### Hero Identity Block
The hero pairs a bold statement with a smaller right-hand margin that holds the portrait, working note, and destination links. It should feel like a confident first page in a notebook: concise, direct, and grounded in real identity.
- **Structure:** strong headline on the left; portrait, note, and links on the right.
- **Mood:** calm, professional, and immediately legible.

### AIR Figure
The AIR research areas are represented as a single generated image rather than a table. That keeps the section feeling like a designed artifact instead of a list, while preserving the ability to read the eight areas at a glance.
- **Structure:** one linked figure with a centered caption.
- **Behavior:** subtle hover fade only; no theatrical motion.

## Do's and Don'ts

### Do:
- **Do** keep the paper sheet, grid canvas, and thin rules as the main structural vocabulary.
- **Do** reserve the orange accent for key actions, active states, and AIR markers.
- **Do** use IBM Plex Sans, IBM Plex Serif, and IBM Plex Mono in their assigned roles.
- **Do** keep the layout generous and readable, with clear section order and sensible collapse at smaller widths.

### Don't:
- **Don't** introduce shadows, glass, gradients, or other depth effects that compete with the flat notebook world.
- **Don't** turn content blocks into same-size marketing cards.
- **Don't** let the accent color become a background mood; it should stay a highlight.
- **Don't** blur the distinction between metadata, navigation, body reading, and display type.
