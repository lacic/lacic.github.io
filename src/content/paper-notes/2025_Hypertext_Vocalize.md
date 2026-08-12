---
paper: 2025-hypertext-vocalize-lead
generated: 2026-08-12
---

## What challenge does this work address?

Consumer engagement and effective lead acquisition are notoriously hard problems, especially in saturated digital channels. Typical solutions often lack fun or personalization, which means users either ignore the interaction or drop out quickly. This work explores whether gamified, voice-driven competitions can spark deeper engagement—and, crucially, whether those games are actually useful for brands wanting quality leads.

## What is Vocalize?

Vocalize is a system that lets brands run voice-based competitions via WhatsApp. Users receive a campaign catch phrase (e.g., “I love Berlin”) and an image outline (like a city skyline). To take part, they send audio recordings where they both speak the phrase *and* try to shape their audio waveform (as shown visually in WhatsApp) to match the target image. A processing engine scores entries on (1) how well users recite the phrase, and (2) how well their audio waveform aligns with the visual target. A leaderboard, prizes, and conversational AI keep the experience interactive and competitive.

## How does the system actually work?

- **Multi-stage scoring**: Speech-to-text methods (like Whisper or proprietary STT) check for keyword accuracy using a modified Levenshtein distance. For shape matching, the waveform is split into 40 segments, and similarity with the image contour is scored based on vector alignment.
- **Natural, ongoing interaction**: Generative AI (using LLMs) handles user queries, gives personalized progress updates, and helps maintain engagement with encouragement and practical tips—critical for ensuring users don’t drop out after their first attempt.
- **Easy onboarding for brands**: Launching a competition needs just a phrase and an image, and everything runs over WhatsApp via Infobip’s integration.

## Did this approach work?

Launched at four large live events (Web Summit, GOTO Chicago, KulenDayz, WeAreDevelopers), Vocalize drove notable participation. Conversion rates from initial contact to engaged participant routinely exceeded 60% at smaller events, and ranged from 42-68% even in massive audiences (Web Summit had nearly 800 initial contacts). Engagement was highly skewed: a small group generated most voice recordings—the classic Pareto law in action.  

A useful observation: tweaks in conversational flow can affect the split between textual and voice engagement, especially when additional information is introduced (as at Web Summit).

## What’s next?

Further studies will explore new audio scoring mechanisms and how demographic variables impact engagement. Extending Vocalize beyond WhatsApp and into more flexible scenarios is underway. For now, the main findings are that gamified, voice-based experiences can both amuse users and reliably capture leads—you don’t need high friction or dull forms to get meaningful engagement.
