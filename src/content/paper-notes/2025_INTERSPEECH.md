---
paper: 2025-arxiv-language-gender
generated: 2026-08-12
---

Most people assume that audio codecs are technical plumbing—transparent, equal-opportunity, strictly functional. This research punches a hole in that assumption.

**PSTN codecs are *not* neutral.** When running over two million real call recordings through PSTN, VoIP, and neural codecs, the gender gap with traditional PSTN codecs jumped off the page. ViSQOL scores for male voices routinely outperformed female ones, sometimes by more than a full standard deviation. That’s a massive effect—much more than the fuzz you get from user preference or random noise. In practical terms, if you sound like a man, these codecs make you sound clearer. If you’re not, you get the short end of the stick.

**Neural codecs, on the other hand, introduce language bias that’s subtle but significant.** Using multilingual speech data, neural codecs (especially EnCodec) showed systematically higher audio quality for Romance languages (like Spanish or French) than for Germanic ones (like Dutch or German). The effect size here is non-trivial—not a curiosity, but a consistent boost, approaching 10% improvements in some pairwise comparisons. PSTN and VoIP codecs barely moved the needle by comparison. Why does this happen? Likely training set bias: these neural nets generalize less well to unfamiliar phonological structures than their designers hope.

**What if you want to minimize bias?** Pick your codec carefully, and consider that PSTN codecs are entrenched in global telecom—billions of calls are still routed through them. Yet, they systematically favor certain users. And if you’re deploying neural codecs, don’t assume language-independence unless you’ve proved it with real, diverse data.

**The bottom line:** Codec engineering isn’t just about compression and bitrates—it’s a real vector for bias. If these effects hold in deployment, speech tech is amplifying disparities we’re only starting to see. This work puts the burden on developers and service providers: do the measurement, and mind the biases lurking under the hood.
