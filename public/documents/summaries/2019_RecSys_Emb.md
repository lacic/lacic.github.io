# Should we Embed? A Study on the Online Performance of Utilizing Embeddings for Real-Time Job Recommendations

Everyone in job recommendation assumes the recent fashion of using neural embeddings—particularly Doc2Vec or Word2Vec—should beat traditional content-based or collaborative filtering, especially offline. But does that hold up when recommendations need to be made in real time and actually tested with live users? That is the question we tackled with this study, using large-scale online A/B testing on the Studo Jobs platform.

For recommending "similar jobs" (the classic item-to-item scenario), the standard baseline is TF-IDF content-based filtering. Industry wisdom suggests that replacing this with neural embeddings would boost click-through rates (CTR) and maybe runtime—but there hasn't been much evidence from true online experiments. Our A/B tests show:

- Using embeddings derived from the _most recent_ job interaction (the "LAST" approach) increased CTR by 18% compared to TF-IDF, _and_ delivered a 24% reduction in runtime latency. The wins in both accuracy and speed were clear in the live environment.
- Trying to mix in both frequency and recency, via the ACT-R-inspired Base-Level Learning (BLL) equation, did _not_ help for this scenario. Simpler is better when users expect jobs similar to their last click—prioritizing just recency beats frequency-weighted combinations as well as more complicated blends.

When it comes to personalizing the homepage experience, the story is different. Here, collaborative filtering (CF) is still the default for most platforms. But by modeling user job browsing history via both frequency and recency (using BLL over embeddings), we saw:

- BLL embeddings outperformed CF by a significant margin: 15% higher CTR and lower latency.
- Combining CF and BLL (in hybrid recommendations) yielded the best effect—33% improvement in CTR over CF alone, at the expense of higher runtimes.

So the short answer: _It depends on the context_. For immediate item-to-item suggestions, fresh recency-based embeddings work best, making the approach not only more effective but also faster than TF-IDF. For broader, homepage-level personalization, there is real value in capturing both frequency and recency—ideally blending multiple signals if you can afford the runtime hit.

Honestly, the most surprising part was just how much simpler recency-based embeddings outperformed fancier blends in the item-to-item case. This challenges the recent trend to always add more complexity; online reality isn't always impressed by more maths. If you deploy recommenders at scale, these results might save you lots of engineering time—and make your users happier in the process.

[Download PDF](2019_RecSys_Emb.pdf)
