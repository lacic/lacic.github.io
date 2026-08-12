---
title: A notebook instead of a homepage
standfirst: The old site was a CV that happened to be on the web. This one is a place to write things down — starting with why the publication list is now data rather than markup.
date: 2026-08-10
type: field-note
tags:
  - meta
  - evaluation
draft: true
# canonical: https://research.infobip.com/...   # set this if cross-posted
---

The previous version of this site answered one question: what has this person
done. It answered it with a sidebar, a photo, and a list of 33 papers as
hand-written HTML. That is a fine answer to a question almost nobody was
asking. The people who actually arrive here — a peer after a talk, a candidate
considering the team, a partner deciding whether a conversation is worth an
hour — want to know what I am working on *now*, and whether it is any good.

So this version leads with a log, and the record moved behind it.

## The publication list is now data

The 33 papers used to live in `main_pubs.html` as markup: a `<div>` per paper,
a hand-typed venue string, a link to a PDF. Four separate things had to be
edited in agreement to add a paper, which is why the list had drifted — a
missing year here, an inconsistent author initial there, a poster that existed
on disk but was linked nowhere.

They are now rows in a YAML file with a schema attached. The build fails if a
venue kind is not one of the nine allowed values, or if a paper note points at
a publication that does not exist. That is a small thing, but it changes the
economics of maintenance: the failure mode moved from *silently wrong in
public* to *loudly wrong before deploy*.

The citations follow from the same rows. There is no stored BibTeX string to
fall out of sync with the venue field, because the BibTeX is generated from the
venue field.

## The part I keep relearning

Every paper now has a plain-language note answering what it says, before you
decide whether to open the PDF. Writing those made something obvious that I
already knew and had not acted on: several papers whose contribution I could
state in one sentence took three paragraphs in the abstract. Some of that is
the genre. Not all of it.

That is the kind of thing this log is for. Not announcements — notes, when
something turns out differently than expected.
