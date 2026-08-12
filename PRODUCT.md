# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary audience: researchers, IT companies, and research groups who want to understand Emanuel Lacić’s current work, publications, and collaboration fit.

Secondary audience: recruiters who want a concise view of experience, credentials, and contact details.

## Product Purpose

A personal research and professional site for Dr. Emanuel Lacić that presents current work, publications, talks, career history, education, funding, and contact details.

Success means a visitor can quickly understand who he is, what he works on now, what evidence supports that work, and how to get in touch or read more.

## Positioning

The site is a living research profile: it combines current AI research activity with a verified record of publications, talks, and career history, rather than presenting a static CV alone.

## Operating Context

Visitors use the site to:

- read the current landing page summary and research focus;
- browse AIR, publications, paper notes, talks, career, education, and funding;
- download linked PDFs and slides;
- follow legacy URLs that still need to work;
- contact Emanuel for collaboration or professional inquiry.

The repository treats content as data and validates it before build time.

## Capabilities and Constraints

- The site is a static Astro project.
- Draft content is visible in development but excluded from production builds.
- The site preserves legacy document URLs and redirects older page URLs where needed.
- Public PDFs, images, and generated figures are part of the product evidence and should remain consistent with the content data.
- The repository is the source of truth for profile, publications, talks, service, and AIR research areas.
- No additional product facts are assumed beyond what the repository confirms.

## Brand Commitments

- Name: elacic.me.
- Persona: Dr. Emanuel Lacić, Principal Engineer at Infobip, leading Team AI Research (AIR).
- Voice: factual, research-forward, and professional.
- Use real assets and verified information only; do not fabricate customers, benchmarks, or claims.

## Evidence on Hand

- `README.md` describes the site, stack, build commands, deployment, and content structure.
- `src/data/profile.ts` defines the identity, bio, links, career, education, funding, awards, languages, and AIR research areas.
- `src/pages/index.astro` shows the landing page structure and the current content order.
- `src/styles/global.css` defines the shared visual system for the current implementation.
- `public/documents/` contains the PDFs and slides linked from the site.
- `public/images/` contains the profile and team imagery used by the site.

## Product Principles

- Lead with current work and make the visitor’s next question easy to answer.
- Keep every public claim grounded in repository-backed evidence.
- Preserve useful URLs and downloadable artifacts so outside links keep working.
- Serve both specialist and professional audiences without diluting technical credibility.
- Prefer concise, structured presentation over narrative drift.
