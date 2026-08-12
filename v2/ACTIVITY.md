# elacic.me v2 — Activity log

Short bullet summaries of what has shipped. Newest first.

---

## 2026-08-12 — Publications refresh + Team AIR outcomes

- Added seven recent papers (PDFs, YAML entries, paper notes), including Infobip AIR work
- Open-vocabulary topic tags with reuse bias; `retag_areas.py` and `add_paper.py --update`
- Publications list shows topics per paper; filter chips require ≥2 papers; tighter year spacing
- `air: true` flag for Infobip/Team AIR papers, with a distinct filter chip and pill
- AIR page intro rail lists the latest three AIR papers and links to `/publications#air`
- Stopped root `.gitignore` from ignoring `v2/src/lib/` so citation/content helpers are tracked

## 2026-08-12 — Remove public projects page

- Dropped `/projects` from nav, CV, and the site map; Know-Center portfolio is no longer public
- `/projects` and `/projects.html` redirect to `/publications`
- Removed `projects.yml` and the projects content collection; `images/apps/` screenshots remain (shared with v1 via symlink) until cutover

## 2026-08-11 — AIR rotating banner + UCLA education fix

- Replaced the duplicated AIR area list (grid image + eight paragraphs) with a full-width rotating banner
- Each panel shows the Infobip colour pair, icon, summary, and an emphasised key phrase
- Auto-advances every five seconds; pauses on hover, focus, off-screen section, hidden tab, and reduced-motion
- Pause control is first in the tab order
- Tightened area summaries to a 15–21 word band so a panel reads within its five seconds
- Moved the eight area icons into `public/icons/air/` so the browser can fetch them
- Emphasis phrases live next to their copy and fail the build if the copy is reworded out from under them
- Moved the UCLA visiting stay from career into education (doctoral research abroad, not a job change)

## 2026-08-11 — Astro rebuild in `v2/`

- Rebuilt the site as an Astro project; landing page leads with a log and Team AIR, CV/record behind it
- Content is schema-validated data instead of hand-written HTML (33 papers, notes, projects, service, talks, profile)
- BibTeX and APA are generated from the same publication fields; broken paper-note links fail the build
- Every PDF keeps its v1 URL; v1 page URLs redirect
- Added `docs/content-guide.md`, content helper scripts, and a GitHub Actions deploy workflow for Pages
