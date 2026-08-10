# elacic.me v2 — Structure & Visual Identity Plan

**Scope of this document.** Information architecture, reading order, new sections, and visual
direction. Technology stack, build tooling, and migration mechanics are covered in
[Stack and deployment](#14-stack-and-deployment).

---

## Status: built

This plan has been implemented. The site is an Astro 7 project in this directory — see
[`README.md`](README.md) for how it is put together and [`docs/content-guide.md`](docs/content-guide.md)
for how to add content.

**Built as planned:** Direction B visual identity with the Infobip accent; the reading order in
§3; all pages in the §4 site map; the AIR section as a generated figure rather than a table;
publications as validated data with generated BibTeX and APA and no citation counts; career grouped
by organisation with concurrent roles marked; education and funding as separate blocks; the three
post types with draft support, series navigation and canonical URLs; RSS; redirects from v1's URLs.

**Content migrated:** 33 publications, 33 paper notes, 20 projects, 21 service entries, 2 talks,
career/education/funding/awards. Every PDF keeps its v1 URL.

**Decided during implementation, differing from this plan:**

- Five selected papers rather than four, all peer-reviewed; the "deployed systems" rows were dropped
  from the landing page in favour of `/projects`.
- Section numbers on the landing page are counted at render time, so a section with nothing to show
  (no posts yet) does not leave a gap in the sequence.
- The research-areas figure is a committed PNG rendered by `npm run image`, not inline SVG, because
  the tiles need CSS `corner-shape` and the site's webfont.
- `needsReview` is camelCase in the schema, matching the other fields.

**Still open** (was §14.4, unchanged): analytics — the dead `UA-134621087-1` tag was not carried
over, and nothing replaced it yet. Three case studies migrated from v1 carry a `PLACEHOLDER` note
because v1 had no text for them; talk dates are inferred from PDF timestamps and want confirming.

---

## 1. The problem with v1

v1 is a 2015 academic CV template, and it still tells the story of someone applying for a
postdoc. Four things work against the goals of "easier to read" and "engaging":

1. **The order serves a hiring committee, not a visitor.** The second thing a reader meets is a
   33-item publication list. Nobody reads it. It buries everything after it.
2. **There is no "now".** The most recent dated content on the landing page is a 2024 talk. A
   reader cannot tell what you are working on this month, and has no reason to return.
3. **Nothing is linkable.** Every section is injected by jQuery at runtime, so there is no URL
   for a single paper, no link previews, and nothing for search engines.
4. **Content is markup.** Publications and projects are hand-written HTML, so adding an item
   means copying boilerplate. This is why the site stopped being updated.

The content itself is strong. The problem is sequencing and framing, which is what this plan fixes.

---

## 2. Audience and the landing page's job

Five readers arrive, roughly in order of how much you care about them now:

| Reader | Arrives from | Wants to know |
|---|---|---|
| Potential research collaborator | A paper, a conference, research.infobip.com | Is there a real R&D group here, and what do they work on |
| Candidate for Team AIR | A talk, a post, word of mouth | What would I work on, who would I work with |
| Industry peer / practitioner | LinkedIn, a shared post | Has he solved the problem I have, is he worth following |
| Conference or program chair | A talk, a PC list | Is he credible, what does he speak about |
| Academic peer | Google Scholar | The full publication record |

Only the last of those five is served well by v1's ordering, and they are the one reader who
will find what they need regardless.

**The landing page has one job:** convince a research-minded reader within 30 seconds that this
is a practitioner running real applied AI research at global scale, and hand them exactly one
next step — read a recent update, look at Team AIR, or get in touch.

Three checkpoints to test any draft against:

- **5 seconds:** who he is, what he does now, that there is a team behind it.
- **30 seconds:** the four research areas, one concrete result, that the site is current.
- **5 minutes:** one update read end to end, plus a path into publications or AIR.

---

## 3. Reading order

This is the central decision of v2. Ordered by what the reader needs, with the academic record
demoted from second position to a destination of its own.

| # | Section | Why here | On landing page? |
|---|---|---|---|
| 1 | **Identity statement** | Answers "who and what now" before anything else | Hero |
| 2 | **Now / latest updates** | The single biggest change. Proves the site is alive, gives a reason to return | 3 most recent |
| 3 | **Team AIR** | The new headline story; what makes this more than a personal CV | Summary + 4 areas |
| 4 | **Selected work** | Mixes papers with shipped systems. Credibility through results, not volume | 5 items |
| 5 | **Talks** | Cheap credibility, high engagement (slides are downloadable) | 3 most recent |
| 6 | **Career in brief** | Full history, grouped by employer, early roles set quietly | 7 organisations |
| 7 | **Education** | Beside the timeline, deliberately not merged into it | 3 degrees |
| 8 | **Funding & fellowships** | Evidence of leading, not just publishing | 4 entries |
| 9 | **Contact / collaborate** | The call to action, once they have a reason to act | Closing band |

Everything else becomes a destination page, reachable but not in the way: full publications,
project portfolio, community and service, CV.

**The key inversion:** v1 leads with the archive and hides the person. v2 leads with the person
and the current work, and keeps the archive one click away for the people who actually want it.

---

## 4. Site map

```
/                       Landing — the seven blocks above, each a gateway
/air/                   Team AI Research — the new centrepiece
/updates/               Reverse-chronological index, filter by tag and series
/updates/<slug>/        One post
/publications/          All ~33 papers, grouped by year, filterable
/publications/<slug>/   Optional: one paper, plain-language summary + PDF
/talks/                 All talks with slides
/projects/              Portfolio, ~15 industry cases
/service/               PC membership, reviewing, workshops, editorial
/cv/                    Readable HTML CV + PDF download
/feed.xml               RSS — required, given the posting goal
```

Nine URLs where v1 had one. Each is independently shareable, previewable, and indexable.

---

## 5. New and reshaped sections

### 5.1 Identity statement (replaces the sidebar profile)

Kill the left-hand CV sidebar. The photo, language list, and programming-language list are CV
furniture that cost the reader attention and tell them nothing.

Replace with a short, declarative statement in large type: name, that you lead Team AI Research
at Infobip, and what the team is for — in your own words, not a job title. One primary action:
read the latest update.

**Underneath: research keywords, not credentials.** An earlier draft put a proof line there — PhD
with distinction, 33 papers, Frontiers editor. Keywords are the better use of that space, because
they answer the question the reader actually has ("is this person working on my problem?") rather
than one they have not asked yet ("is he qualified?"). Set them like the keyword line of a paper:
small mono, thin-bordered, six at most.

```
Keywords  Recommender systems · Generative AI & LLMs · Fairness & bias
          Real-time personalization · Information retrieval · Evaluation & reproducibility
```

The credentials are not lost, just relocated to where they answer a question: the PhD appears in
the career timeline and on `/cv/`, the paper count is already implied by "five of 33" and the link
beside it, and the Frontiers editorship belongs in `/service/`.

### 5.2 Team AIR — the new centrepiece

The section you asked for, and it should carry the most weight on the page. Structure:

- **What AIR is.** Two or three sentences: an R&D team inside Infobip doing applied research on
  AI for communication at global scale, where research insight has to survive contact with
  production. The tension between "research" and "production" is the interesting part — lead
  with it.
- **The eight research areas as one image.** There are eight, not four — the full list is on
  [research.infobip.com/research](https://research.infobip.com/research): Human-AI Collaboration,
  Trustworthy AI, Conversational AI, AI-powered Communication, Fraud Detection, Spam Filtering,
  Voice AI, and Generative Models (shortened from Infobip's "Special Generative Models" —
  worth keeping consistent if the AIR page ever quotes their wording verbatim). The landing page
  **names them and nothing more**: no
  per-area links, no paper counts, no evidence badges. One link sends the reader to the AIR page
  for the detail.

  The image is built from Infobip's own eight area icons, recoloured into their four dark/bright
  pairs and set in squircles. It is generated rather than hand-drawn — see section 8.1 for the
  build path — so re-rendering after a copy or colour change is one command.
- **How research reaches production.** A short honest account of the path from question to
  deployed system. This is your genuine differentiator over an academic group and over a
  product team, and no one else's site can claim it.
- **Programme work.** EDIH Adria, IPCEI-CIS, Conversational Order Management, Global
  Communication Platform — framed as what they enable, not as grant titles.
- **Two exits.** Collaborate with the team, and join the team.

### 5.3 Updates — the engine

The section that makes the site worth revisiting, and the one most likely to decay if the
authoring path has friction. Design the model before the layout.

Three post types, so that "posting an update" is never a blank page:

| Type | Length | Cadence | Example from research.infobip.com |
|---|---|---|---|
| **Field note** | 150–400 words | Whenever | "We've created a game to raise fan engagement through WhatsApp" |
| **Deep dive** | 1,000+ words, may be a series | Monthly-ish | The three-part Semantic Scholar MCP series |
| **Paper note** | Auto-drafted, then edited | Per paper | Plain-language version of a publication |

Notes on each:

- **Series support is not optional.** The MCP posts are explicitly Part 1/2/3. A reader landing
  on Part 3 needs to see the whole arc and where they are in it.
- **Paper notes are nearly free.** `documents/summaries/` already holds 39 generated markdown
  summaries with frontmatter, produced by `scripts/summarize_papers.py`. That is 39 posts and
  39 plain-language paper descriptions of drafted content sitting unused. Wiring it up is the
  highest-leverage content move available in v2.
- **Every post needs**: date, type, tags, reading time, and a one-sentence standfirst that
  works as both a preview and a social share. Titles like "The phone codec behind most calls
  favors male voices by a full standard deviation" already do this job well — that is the
  register to write in.

### 5.4 Publications — from wall to instrument

Same 33 papers, restructured so a human can use them:

- Grouped by year, newest first, collapsed to one line per paper: title, venue, year.
- Filter by research area, venue type (conference / journal / workshop), and year.
- Expanding a paper reveals the plain-language summary from `documents/summaries/`, then the
  PDF, poster, and slides. **The summary is what makes this section readable** — a title and a
  venue tell a non-specialist nothing.
- Mark the highlighted papers so the "selected" list on the landing page and this page agree.

**No citation counts.** They would need a refresh path, they age badly, and they make deployed
systems look like failures. Every paper row instead carries the same three actions:

| Action | Behaviour |
|---|---|
| `pdf` | Direct link to the existing file in `documents/` |
| `poster` | Same, where a poster exists; visibly disabled where it does not |
| `cite` | Opens a small menu with **BibTeX** and **APA**, each copying to the clipboard |

Notes on `cite`: generate both strings at build time from the publication data, so there is one
source of truth and no chance of the page and the BibTeX disagreeing. Confirm the copy with a
brief `aria-live` message rather than a silent state change, close on Escape and on outside
click, and keep the trigger a real `<button>` with `aria-expanded`. Deployed systems have no
paper and no citation, so their row shows a single `case study` action — the asymmetry is honest
and makes the point that not all work ends in a publication.

### 5.5 Selected work — papers only, with the real venue

An earlier draft of this plan mixed papers and deployed systems into one list, labelling the
systems `deployed` in the venue column. That was wrong: a "venue" column has one meaning to this
audience, and putting a non-venue in it makes the reader stop and work out what happened.

**Selected work is five papers, each showing where it was actually published**, with the venue
name, year, and kind:

| # | Paper | Published in |
|---|---|---|
| 01 | Uptrendz: API-Centric Real-Time Recommendations in Multi-Domain Settings | ECIR 2023 · conference · Springer |
| 02 | What Drives Readership? | ECIR 2022 · conference · Springer |
| 03 | Using Autoencoders for Session-based Job Recommendations | UMUAI 2020 · journal · Springer |
| 04 | Should we Embed? | RecSys 2019 · conference · ACM |
| 05 | Utilizing Online Social Network and Location-Based Data… | MMSM 2015 · book chapter · Springer |

Marking the kind matters, because a journal article, a full conference paper and a book chapter
carry different weight to an academic reader and are indistinguishable from the title alone.

Deployed systems keep their credibility role, but as a **one-line link out** beneath the list
rather than as rows inside it — the portfolio is where they belong. Newest-first ordering, stated
plainly in the caption; no claim of ranking, since the list is chronological.

### 5.6 Career in brief

Show the **whole** history, not an abridged version. An earlier draft cut it to four or five
entries and lost 1&1 Internet AG, FZI, Ericsson, and the first Infobip role — which reads as a
gap rather than as brevity. Eight roles across seven organisations is not too many when they are
grouped and the early ones are set quietly.

**Group by organisation, not by role.** This is the answer to the multiple-roles-per-employer
problem. A reader is orienting themselves by *place* — "he was at Know-Center for seven years" is
the fact they retain; the internal promotion is detail underneath it. A flat chronological list
makes one continuous tenure look like two short ones, which understates you.

So the outer row is the organisation with its full span, and the roles nest inside it:

```
2023 —      Infobip                              Zagreb
              Principal Engineer — founded and lead Team AI Research

2016—2023   Know-Center             Graz · 7 years, 2 roles
              2021—23  Operations Area Manager, Fair-AI division
              2016—20  Senior Researcher & RecSys Architect
            ╌ 2018     [visiting] Visiting researcher, UCLA

2013—2016   TU Graz                              Graz
              University & Project Assistant — EU project Learning Layers
            ─────────────────────────────────────────────── quieter below
2013        1&1 Internet AG                      Karlsruhe
              Junior Software Developer — Ruby, data-centre tooling
2012        FZI Forschungszentrum Informatik     Karlsruhe
              Java Developer — EU FP7 project Mirror
2011—2012   Infobip                              Zagreb
              Software Engineer — mobile cloud services (SMS, HLR, USSD)
2010        Ericsson                             Zagreb
              Java Developer — primary healthcare information system
```

**Set the pre-2013 roles quietly rather than cutting them.** Smaller type and tighter rows, same
structure. They establish that you were an engineer before you were a researcher — which is
exactly the claim the AIR section makes — while keeping the recent work visually dominant. This is
also what makes showing all eight affordable.

**Two separate Infobip rows, and no annotation.** Grouping by organisation would suggest merging
them, but a single "Infobip · 2011, 2023—" row would imply continuous employment that did not
happen. Two rows twelve years apart, each with its real dates, and no "started here" or "returned"
label — the dates say it, and a reader who cares will notice. An earlier draft drew a bracket
between them; it was the kind of device that flatters the designer more than it helps the reader.

Same grouping rule generalises: group when a tenure is continuous, split when there is a genuine
gap, and never let the layout assert something the dates contradict.

**Concurrent positions, e.g. UCLA.** The visiting research stay at UCLA in 2018 happened *during*
the Know-Center years on a Marshall Plan Fellowship. It is not a job, and listing it as one would
either imply you left Know-Center or create a phantom overlap the reader has to reconcile.

Nest it inside the Know-Center block as a third row, but style it as parallel rather than
sequential: indented behind a dashed rule and tagged `visiting`. The dashed rule is doing real
work — solid means "this role followed the one above it", dashed means "this ran alongside".

```
2016—2023   Know-Center     Graz · 7 years, 2 roles
              2021—23  Operations Area Manager, Fair-AI division
              2016—20  Senior Researcher & RecSys Architect
            ╌ 2018     [visiting] Visiting researcher, UCLA Computer
                       Science — Marshall Plan Fellowship
```

This generalises to anything concurrent: guest lectures, editorial roles, advisory positions. The
host organisation stays the outer row; the parallel engagement is nested and marked.

### 5.8 Education — a separate block, not part of the timeline

Three degrees, all from `sidebar.html`:

| Degree | Institution | Year |
|---|---|---|
| PhD, Computer Science, with distinction | Graz University of Technology | 2022 |
| M.Sc., Software Engineering & Information Systems | University of Zagreb (FER), final year at Karlsruhe Institute of Technology | 2012 |
| B.Sc., Software Engineering & Information Systems | University of Zagreb (FER) | 2010 |

**Do not interleave these into the career timeline.** It is tempting, but the PhD completed in
2022 while you were an Operations Area Manager, so a single merged timeline would place a degree
between two jobs and imply you stopped working to get it. Education and employment answer
different questions and should be read separately.

Two details worth keeping. The **"with distinction"** qualifier earns a highlight — it is the one
piece of the education block that is not merely expected. And the PhD row carries its own actions,
`thesis` and `defence slides`, since both PDFs already exist in `documents/` and a curious reader
will want them right there rather than after a detour to `/cv/`.

The M.Sc. spans two institutions. State it as one degree with the final year at KIT rather than as
two entries, which is what actually happened and takes one line instead of two.

### 5.9 Funding — separate it from awards

v1 puts a €286k project grant, a travel grant, an Erasmus scholarship, and two best-paper awards
in a single sidebar list called "Awards and Grants". That mixes two different claims. **An award
says other people rated your work. Funding says you can be trusted with a budget and a
consortium.** For someone leading an industrial research team, the second is the stronger and
rarer signal, and it should not sit next to a 2012 student scholarship.

Split them:

- **Funding & fellowships** gets its own block on the landing page, next to the career timeline.
  Each entry: what it was, the amount where public, the programme, the year, and **your role** —
  whether you secured it, led it, or contributed. Role is the part that matters and the part v1
  omits entirely.
- **Awards and honours** move to `/cv/`: best paper and poster awards, the Mind-the-gap diversity
  award, travel grants, scholarships.

Four entries are enough on the landing page, ordered by weight rather than date: IPCEI-CIS and
EDIH Adria as the current EU programme work, Data Market Austria at €286,000 as the concrete
number, and the Marshall Plan Fellowship as the personal grant.

Two cautions. **Check what you can disclose** — the Infobip-side programme values are likely
confidential, so those entries show the programme and your role but no figure, and the block says
so rather than leaving the reader to wonder. And **decide whether a total belongs in the hero**;
an aggregate figure is normal in academic CVs but reads as boasting on a personal site, so this
plan leaves it out of the hero and keeps the detail in the block.

### 5.7 Service and community

Keep it, move it to `/service/`, and group into PC and reviewing, workshops organised,
editorial roles, and supervision. It matters to the academic reader and to no one else, so it
should be reachable and out of the way. Fold in the three co-supervised theses, currently
stranded inline in `index.html`.

---

## 6. Relationship to research.infobip.com

The two sites will overlap, so set the rule now to avoid both duplicate content penalties and a
confused reader.

- **research.infobip.com is the company voice** — official team page, programme announcements,
  recruiting, partnerships. Authoritative for anything that speaks for Infobip.
- **elacic.me is your voice** — personal perspective, method, what did not work, the reasoning
  behind a result, your own publication record and career.
- **`/air/` should introduce and link out, never mirror.** Describe the team as its lead, then
  send readers to research.infobip.com for the official page and open roles.
- **For cross-posted articles, set `rel="canonical"` to the research.infobip.com URL.** You get
  the reader; they get the search ranking; nobody is penalised.
- A short "also published at" line on cross-posted items keeps this honest and visible.

---

## 7. What to cut

Cutting is most of the readability gain. Remove outright:

- The left CV sidebar as a layout device.
- Animated skill bars (`assets/js/main.js`), the programming-language list, the spoken-language
  list, and the 2012 Agile certification.
- The 33-item publication list on the landing page.
- `index_old_849bck_up32.html` and `resume.html` — both dead, one unlinked.
- Duplicate vendor CSS: Bootstrap in both `assets/css/` and `css/`, Font Awesome 4 *and* 5.
- The `UA-134621087-1` Universal Analytics tag. The property has been dead since 2023 and is
  collecting nothing. Replace deliberately or drop it.
- `public/tags/` and `public/categories/` — empty leftovers from an abandoned Hugo attempt.

Keep and reuse: all 51 PDFs, the 15 project screenshots, the 39 generated summaries.

---

## 8. Visual identity — three directions

Constraint worth stating: the current teal-on-Bootstrap look must go, but so must the obvious
replacements. A cream background with a big serif and a terracotta accent, or near-black with
one acid accent, are the two most common looks on the internet right now. They are defaults, not
choices. Each direction below is derived from your actual subject matter instead.

### Direction A — "Relevance" (recommended)

**Concept.** Your entire career is about ordering things by relevance — top-k lists, ranking,
embeddings, evaluation. So the page is built as a ranked result list. The reader is not scrolling
a CV; they are reading a ranking, best first. This gives an honest reason for structure that
would otherwise be decoration, and it makes the demotion of the publication archive feel like
a design principle rather than an omission.

**Palette** — cool and instrument-like, deliberately not warm paper.

| Token | Hex | Use |
|---|---|---|
| `ink` | `#14192B` | Text, headings. Near-black with a blue cast, never pure black |
| `paper` | `#F6F7FB` | Background. Off-white pulled cool, explicitly not cream |
| `muted` | `#7C859B` | Metadata, venues, dates, rules |
| `accent` | `#4739FF` | Electric indigo. Links, rank markers, one element per screen |
| `signal` | `#FFA62B` | Amber. *Only* for "new" and current-work flags. Never decorative |

**Type** — the deliberate risk is inverting the usual pairing. Almost every site in this genre
uses a serif display with a sans body; this does the opposite.

- **Display:** Bricolage Grotesque — a variable grotesque with genuine quirk in its widths.
  Opinionated, and not Inter or Playfair.
- **Body:** Source Serif 4 — because updates are long-form, and serif at 18–19px is simply
  easier to read than sans. This directly serves "easier to read".
- **Utility:** IBM Plex Mono — years, rank markers, venue tags, metrics. Data should look like data.

**Signature element:** the rank marker. Selected work is numbered in mono, and each item carries
a thin horizontal bar. Numbering is justified here because the list genuinely *is* a ranking —
if the bar cannot encode something true (citation count, recency), drop the bar and keep the
number. A decorative bar would undercut the whole premise.

### Direction B — "Lab notebook"

**Concept.** Applied research as it actually happens: annotated, provisional, corrected. Faint
grid underlay, marginal annotations in mono, small inline plots, visible revision dates. Fits
the honesty of "here is what we tried and what failed".

**Palette:** cool grey grid `#EDF1F4`, graphite ink `#1B2024`, plot red `#D83A2C`, pencil
`#5C6670`. **Type:** mono-forward for structure, humanist sans for body.

**Risk, stated plainly:** hairline rules plus dense columns plus zero border-radius drifts
toward the broadsheet look that is itself becoming a default. It needs real restraint to avoid.

### Direction C — "Global scale"

**Concept.** Messaging across networks — nodes, routes, latency, volume. Darker interface with
ambient network motion, numbers-forward, emphasising the scale that distinguishes industry
research from academic research.

**Palette:** deep navy `#0B1220`, cyan-white `#E8F1FF`, route violet `#7A5CFF`, live green `#2BD98A`.

**Risk:** near-black with one bright accent is the second AI default. Would need the motion to be
genuinely derived from real traffic-shaped data to earn it, and dark backgrounds make long-form
reading harder — which fights the primary goal.

### Chosen: Direction B, adapted

Direction B is the direction, with three adaptations recorded below. The relevance-ranking idea
from Direction A survives as an ordering principle in "Selected work" — the list is ordered by
relevance rather than date, and says so — but without the citation bars.

**Palette.** Notebook neutrals stay as the site's own voice; the arbitrary plot-red is replaced
with Infobip's real brand orange so the site accent and the AIR section agree. These are the
actual tokens from Infobip's 2024 theme, not approximations:

| Token | Hex | Infobip name | Use |
|---|---|---|---|
| `ink` | `#1B1A19` | `--color-black` | Text |
| `pencil` | `#6D6C6C` | `--color-grey-600` | Metadata, annotations |
| `accent` | `#FC6423` | `--color-brand` | Links, section numbers, the single accent |
| `grid` | `#EDF1F4` | near `--color-light-blue-200` | Grid underlay |
| `paper` | `#FBFCFD` | near `--color-light-blue-100` | The sheet |

Infobip pairs a dark background with one bright "accent-on-background" colour. There are exactly
four such pairs, and exactly four research areas, so each area gets one:

| Area | Dark | Bright |
|---|---|---|
| Conversational AI | `#17283A` dark-blue-900 | `#9EB2FF` bright-blue-600 |
| Trustworthy AI | `#053133` dark-green-900 | `#CBEA99` bright-green-300 |
| Human-AI Collaboration | `#32232F` dark-pink-800 | `#FFA8EB` bright-pink-300 |
| AI-powered Communication | `#2D2C2B` grey-800 | `#FC6423` brand |

These four pairs appear **only inside the AIR cluster**. That keeps a visible boundary between
the personal site and the company section. Worth knowing: making brand orange the site-wide
accent ties your personal identity to Infobip's, so if you ever want to decouple, it is a
one-token change.

**Shape language: squircles, not hexagons.** You asked about a hexagonal structure. Infobip's
graphic system is explicitly built on the *squircle* — a rounded-square taken from their brand
symbol, elongated up to 4× for the wider system. Hexagons would read as off-brand. Their
expressive tier is called the **"Biposphere"**: a network of connected squircles standing for the
global communication network.

### 8.1 The research-areas image

Generated, not drawn by hand, and reproducible:

1. Eight source icons come straight from research.infobip.com
   (`research-<area>.svg` on their CDN). Each is a single path filled `#FC6423`.
2. `v2/mockups/air/compose.html` lays them out as eight squircles, recolouring each icon with
   `mask-image` so the source SVGs are never edited, and rotating the four Infobip dark/bright
   pairs diagonally across the grid.
3. Headless Chrome screenshots that page at `--force-device-scale-factor=2` to a transparent PNG.
   Chrome is needed for two reasons: it loads IBM Plex Sans as a webfont, and it supports
   `corner-shape: squircle` for a true superellipse rather than a rounded rectangle.

Three consequences worth writing down:

- **Ship the SVG, not just the PNG.** The composer output is vector; rendering to PNG loses
  crispness and makes the text unselectable. In the real build, inline or embed the SVG and keep
  the PNG only as a fallback and as the Open Graph image.
- **The alt text must name all eight areas**, since the area names exist only as pixels in the
  PNG. This is the one real cost of using an image here.
- **Icons are Infobip assets.** Fine for a page about the team, but the file should be regenerated
  from their CDN rather than forked, in case the set changes.

**Typography.** Infobip's own faces are KMR Apparat for headlines and Inter for everything else.
KMR Apparat is licensed and not available to us, and using Inter would make the site look like a
corporate microsite. Keep IBM Plex Sans / Serif / Mono: it holds the notebook character, reads
well at length, and keeps the personal site distinguishable from the company one.

---

## 9. Layout

One measured reading column, roughly 66 characters, with a metadata rail on wide screens that
collapses above the content on mobile. No two-column CV.

**Landing page:**

```
┌──────────────────────────────────────────────────────────────┐
│  ELACIC                    updates  air  papers  talks  cv   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   I lead Team AI Research at Infobip,                        │
│   where we build AI for communication                        │
│   at global scale — and find out what                        │
│   survives contact with production.                          │
│                                                              │
│   PhD · 33 papers · Frontiers editor    [Latest update →]    │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  NOW                                          all updates →  │
│  ▸ Aug 2026  The phone codec that favors male voices   6 min │
│  ▸ Jul 2026  Semantic Scholar MCP, part 3          series·3  │
│  ▸ Jul 2026  Semantic Scholar MCP, part 2          series·3  │
├──────────────────────────────────────────────────────────────┤
│  TEAM AI RESEARCH (AIR)                            about →   │
│  ┌────────────────┐ ┌────────────────┐                       │
│  │ Human-AI       │ │ Trustworthy    │   R&D inside Infobip. │
│  │ Collaboration  │ │ AI             │   Four questions we   │
│  └────────────────┘ └────────────────┘   work on, and what   │
│  ┌────────────────┐ ┌────────────────┐   shipped because of  │
│  │ Conversational │ │ AI-powered     │   them.               │
│  │ AI             │ │ Communication  │                       │
│  └────────────────┘ └────────────────┘                       │
├──────────────────────────────────────────────────────────────┤
│  SELECTED WORK                                all papers →   │
│  01  What Drives Readership?          ECIR'22  ███████░  pdf │
│  02  Autoencoders for Session-based…  UMUAI'20 ██████░░  pdf │
│  03  Should we Embed?                 RecSys'19 █████░░░ pdf │
│  04  Job Marketplace                  deployed system    →   │
│  05  Steerable Guest Activities       deployed system    →   │
├──────────────────────────────────────────────────────────────┤
│  TALKS  ·  CAREER IN BRIEF  ·  COLLABORATE                   │
└──────────────────────────────────────────────────────────────┘
```

**Update post:**

```
┌──────────────────────────────────────────────────────────────┐
│  ← updates                                                   │
│                                                              │
│  FIELD NOTE · 10 Aug 2026 · 6 min                            │
│                                                              │
│  The phone codec behind most calls                           │
│  favors male voices by a full                                │
│  standard deviation                                          │
│                                                              │
│  One-sentence standfirst that also works as the              │
│  social preview and the index entry.                         │
│  ──────────────────────────────────────────                  │
│                                                    ┌───────┐ │
│  Body in Source Serif, 19px, 66ch.                 │ tags  │ │
│                                                    │ series│ │
│                                                    │ also  │ │
│                                                    │ at →  │ │
│                                                    └───────┘ │
│  ──────────────────────────────────────────                  │
│  Next in series: part 3 →                                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 10. Motion

One orchestrated moment, not scattered effects. On load, the identity statement sets line by
line and the "now" list settles into place — the page assembling its own ranking. After that,
motion is limited to hover and focus states. Respect `prefers-reduced-motion` throughout.

Explicitly not doing: scroll-jacking, count-up numbers, parallax, or per-section fade-ins.

---

## 11. Quality floor

Not features, just the baseline any draft must meet:

- Content in the HTML, readable with JavaScript disabled. This is the fix for v1's core defect.
- Every section and item has its own URL.
- Visible keyboard focus, AA contrast on all five palette tokens, real landmarks and heading order.
- `prefers-reduced-motion` honoured.
- Open Graph and Twitter card images per page — you will be sharing posts, and link previews are
  the first impression.
- RSS at `/feed.xml`.
- Mobile first; the metadata rail collapses, the reading column never exceeds ~66ch.

---

## 12. What this plan does not yet answer

Open questions to resolve before building:

1. **The photo.** Removing the sidebar removes the portrait. Does a photo appear at all, and if
   so where — hero, footer, or only on `/cv/`?
2. **Honest metrics.** The relevance bar in Direction A needs a true underlying number. Citation
   counts from Scholar are the obvious candidate but need a refresh path.
3. **Voice.** How personal is the writing? "What did not work" is the most engaging register and
   the most exposed one.

**Resolved — posting cadence.** Monthly to every two months, with occasional cross-posts from
research.infobip.com. Three consequences for the design of the "now" block:

- **Use absolute dates, never relative ones.** "Aug 2026" ages gracefully; "3 days ago" makes a
  seven-week gap look like neglect.
- **Show the three most recent posts regardless of age**, and never label the block "Recent" or
  "Latest news". A neutral heading — "Now", or nothing at all — cannot go stale.
- **A bi-monthly rhythm makes deep dives the backbone**, not field notes. Plan the block around
  one substantial piece with two shorter items beside it, and lean on paper notes from
  `documents/summaries/` to fill the gaps without inventing work.

Because cross-posting is occasional rather than default, individual posts decide their own home:
the `rel="canonical"` and "also published at" treatment in section 6 becomes per-post metadata,
not a site-wide rule.

---

## 12a. Publishing workflow — adding a paper

The question this section answers: *I have a new paper PDF. What do I do?*

### Why placement stops being a problem

In v1 a script would have to splice HTML into `main_pubs.html` at the right line, in the right
year group, in the right format — fragile, and the reason nobody automated it.

In v2 publications are **data, not markup**: one `publications.yml`, and the page sorts and groups
at build time. A script only has to append an entry. "The appropriate place" is then a consequence
of the data, not something the script has to get right.

### The command

```bash
uv run scripts/add_paper.py documents/2026_RecSys_llm_ranking.pdf
```

Which does six things:

| Step | Detail |
|---|---|
| 1. Extract text | `pypdf`, exactly as `summarize_papers.py` already does |
| 2. Extract metadata | A new Pydantic model (`PaperEntry`) alongside the existing `PaperSummary` — title, authors, venue, year, kind, abstract |
| 3. Verify against a real source | Look the paper up on Semantic Scholar or Crossref for canonical venue, DOI, and BibTeX |
| 4. Find the poster | By filename convention: `documents/posters/<stem>_poster.pdf` |
| 5. Append to `publications.yml` | With `needsReview: true` |
| 6. Write the summary | Reuse the existing summariser into `documents/summaries/<stem>.md` |

Then the loop is just: review the entry, `git commit`, `git push`. CI builds, the site updates,
the paper appears in the right year group with its PDF, poster, plain-language summary, and
BibTeX and APA citations generated from the same single entry.

### Three things that matter more than the automation

**Never let extracted metadata reach the site unreviewed.** Bibliographic data is precisely where
LLM extraction fails: author lists get truncated, workshop papers get labelled as main-conference
papers, and diacritics get mangled — your own surname, `Lacić`, is the most likely casualty on
your own site. Hence step 3 against a real bibliographic source, and hence `needsReview: true`,
which the build surfaces as a warning until you clear it. The script's job is to remove typing,
not judgement.

**Filename conventions only half exist today.** `2023_ECIR_uptrendz.pdf` pairs with
`posters/2023_ECIR_uptrendz_poster.pdf`, but `2019_RecSys_Emb.pdf` pairs with
`posters/Studo_RecSys19_Poster.pdf`. So auto-detection should guess by convention and *ask* when
it cannot, rather than silently attaching nothing. Going forward, one convention makes step 4
reliable; the existing ~51 files get their links written once during migration.

**The schema is the real safety net.** Astro validates `publications.yml` against a Zod schema at
build time, so a missing year or an unknown venue kind fails the build rather than rendering a
broken row. That is what makes it safe to have a script writing to your content.

### Writing a post about anything else

Papers are the special case, because they have structured metadata. Ordinary writing is simpler:
a markdown file is a post.

**Scaffold it**, so you never hand-write frontmatter or start from a blank file:

```bash
uv run scripts/new_post.py "Why our A/B test disagreed with the offline evaluation"
# → src/content/updates/2026-08-14-why-our-ab-test-disagreed/index.md  (draft)
```

**A post is a folder, not a file.** You will want screenshots and plots, and co-locating them
beside the text means a post is self-contained, moves as a unit, and never accumulates orphaned
images in a shared uploads folder:

```
src/content/updates/2026-08-14-why-our-ab-test-disagreed/
  index.md
  offline-vs-online.png
```

**The frontmatter** is the whole contract, and the Zod schema enforces it:

```yaml
---
title: "Why our A/B test disagreed with the offline evaluation"
standfirst: "We shipped a ranker that looked worse offline and better online.
             Here is what the offline metric was missing."
date: 2026-08-14
type: field-note          # field-note | deep-dive | paper-note
tags: [evaluation, recommender-systems, production]
draft: true
series: null              # or { name: "Semantic Scholar MCP", part: 3 }
canonical: null           # set when cross-posted to research.infobip.com
---
```

**Then write, with live preview.** `npm run dev` serves the post at its real URL with reload on
save, so you are editing the actual page rather than imagining it.

**Publish by flipping `draft: false`, then commit and push.** Drafts are excluded from the build,
the index, and the feed, so you can leave a half-written post in the repo for weeks without it
leaking. This matters at a bi-monthly cadence, where posts get written across several sittings.

Four notes on the model:

- **`type` controls layout; `tags` describe subject.** Keep `type` a small closed set, because
  each value implies a template decision — a deep dive gets series navigation, a paper note gets a
  PDF link and a citation. Tags stay open, and are where the actual topic lives.
- **If a post fits no type, it is a field note.** That is the default rather than a decision to
  make, so "I want to write about something else" never becomes a modelling question.
- **`standfirst` does triple duty**: the index entry, the social preview, and the first thing a
  reader sees. It is the one field worth rewriting until it is good.
- **A post can become a series retroactively.** Adding `series` to an existing post is enough;
  nothing needs restructuring, which is how the Semantic Scholar MCP posts presumably grew.

### Adding other content

| Content | How |
|---|---|
| **A talk** | One entry in `talks.yml`, slides PDF into `documents/talks/` |
| **A new AIR research area** | Edit `compose.html`, re-render `air-areas.png`, update the alt text |
| **A CV update** | Replace `documents/elacic_cv.pdf`; the HTML CV reads the same data as the rest of the site |

## 13. Suggested order of work

Structure first, then identity, then content migration.

1. Lock the reading order and site map (sections 3 and 4).
2. Pick a visual direction and build the token set (section 8).
3. Build the landing page and one update post as vertical slices, to test both.
4. Wire `documents/summaries/` into paper notes and the publications page.
5. Write `/air/` — the section with no existing content to migrate, and the most important.
6. Migrate publications, projects, talks, service, CV into data files.
7. Build `scripts/add_paper.py` (section 12a) — last, because it writes into a schema that has to
   exist first, and because migrating 33 papers by hand is what proves the schema is right.

---

## 14. Stack and deployment

### 14.1 Stack: Astro 7

The content model in section 5.3 means markdown with frontmatter, which means a build step this
repo has never had. **Astro 7.2** (current as of August 2026) is the choice.

Reasons specific to this project, rather than general enthusiasm:

- **Content collections with schema validation.** Publications and projects become typed data
  validated at build time. Given that v1 rotted because every new paper meant copying HTML, a
  schema that fails the build on a malformed entry is the single most useful property available.
- **Markdown with frontmatter is the native input**, which is exactly what
  `scripts/summarize_papers.py` already emits into `documents/summaries/`.
- **Zero JavaScript by default.** This directly fixes v1's core defect. Content ships in the HTML;
  interactivity (the publications filter) is added as an island only where it earns its place.
- **A real component model with scoped styles**, which matters because v2 is a design-led
  rebuild. Section 8's token system becomes CSS custom properties in one place.
- **Open Graph image generation, RSS, and sitemaps** are solved problems in this ecosystem, and
  sections 5.3 and 11 require all three.

Rejected, with reasons:

| Option | Why not |
|---|---|
| **Jekyll** | Its one real advantage is building natively on GitHub Pages with no CI at all. But Ruby tooling and a dated templating story make it the wrong instrument for a design-forward rebuild. |
| **Hugo** | Fast, with strong taxonomy support for tags and series. Go templates actively fight fine-grained design work — and this repo already contains the remains of an abandoned Hugo attempt in `public/`. |
| **Eleventy** | A reasonable second choice. Loses on schema validation and on OG image tooling. |
| **Hand-authored HTML** | Cannot support the content model. This is how v1 got here. |
| **Python SSG** | Matches your existing tooling, but the ecosystem for a design-forward content site is much weaker. Keep Python for the summarizer, which stays as-is. |

### 14.2 Deployment: switch Pages to GitHub Actions

Today the repository root *is* the published site, served from `master`. A build step makes that
untenable, and committing build output is not an acceptable answer.

**Change the GitHub Pages source from "deploy from a branch" to "GitHub Actions".** Source lives
in the repo, the workflow builds it, and the result is deployed as an artifact. Nothing built is
ever committed. The workflow is small — `withastro/action@v6` followed by
`actions/deploy-pages@v5`, on push to `master`.

Two details worth setting up correctly the first time:

- **Preserve every existing URL.** Inbound links to PDFs are the most valuable thing v1 has, and
  they must not break. Put `documents/` and `images/` under Astro's `public/` so
  `/documents/2022_ECIR_news.pdf` resolves exactly as it does now. Keep `CNAME` in `public/` too,
  belt and braces alongside the domain setting. Add one redirect: `/resume.html` → `/cv/`.
- **Persist the build cache.** Roughly 66 MB of PDFs are copied on every build. That is fine, but
  cache `node_modules/.astro/` in CI and enable Astro 7.2's `experimental.incrementalBuild` with
  `entry.digest` as the `cacheKey` once the publication and update routes exist.

### 14.3 This resolves the `v2/` preview question

GitHub Pages hosts one deployment, so `v2/` cannot be both a preview and a clean cutover. It
should never be served from Pages at all.

- **While building:** develop in `v2/` and preview with the local dev server. For a shareable
  preview URL, point Cloudflare Pages or Netlify at the repo with `v2/` as the project root —
  free, no effect on the live site, and a real URL per branch.
- **At cutover:** move the Astro project from `v2/` to the repository root, delete the v1 HTML
  files listed in section 7, switch the Pages source, and keep `CNAME` unchanged. The custom
  domain never moves and `elacic.me/v2/` is never a public URL.

### 14.4 Still open

- **Analytics.** The `UA-134621087-1` property has been dead since 2023. Either adopt something
  privacy-respecting and lightweight, or decide the site does not need analytics at all. Do not
  port the broken tag forward.
- **Infobip brand alignment.** Direction A is deliberately not Infobip-branded, since this is a
  personal site. Given how prominently Team AIR features, worth one sanity check against brand
  guidelines so the two properties do not clash.
