# Evaluating Tag Recommendations for E-Book Annotation Using a Semantic Similarity Metric

Tagging e-books sounds easy, but the vocabulary mismatch between editors and readers remains a persistent headache. Editors gravitate toward formal, often content-descriptive tags, while readers search and review using their own (sometimes unpredictable) language. The result? A gap between how books are described and how they're actually found.

This paper tackles that gap using tag recommendation systems. We introduced a hybrid approach that combines traditional editor tags with Amazon user search terms, arguing that blending these sources might bridge the vocabulary divide. Our evaluation covered 19 distinct algorithms, grouped into popularity-based, content similarity-based, and hybrid variants. Importantly, we didn't just chase raw accuracy; we also evaluated semantic similarity—how closely recommended tags match the *meaning* (using Doc2Vec embeddings) rather than just the exact words—and diversity within the tag suggestions.

The results are telling:

- **Accuracy? Editor tags still rule.** Populating recommendations from editor tags, perhaps filtered by author, leads the pack on nDCG measures. Amazon search terms alone are less precise—hardly surprising, given their noisiness.

- **Semantic similarity and diversity? User signals matter.** The standout insight is that even when search-term-based methods fare poorly on accuracy, they often suggest tags that are semantically close to users' actual review vocabulary. These tags may not *match* the gold standard, but they match what readers mean—an advantage if you care about real-world retrieval. Diversity also improves with user-derived tags: their noisier nature widens the conceptual scope.

- **Hybrid models win when you want both.** By combining the strengths of both sources, the best hybrid approaches outperform single-source methods, particularly when the performance is measured over multiple metrics (accuracy, semantic similarity, *and* diversity). The optimal hybrids blend popularity-based filtering (for precision) with similarity-based expansions (for breadth and relevance).

The catch—editor tags and Amazon search vocabularies overlap with only a sliver of the catalog. That limits the pure coverage of data-driven approaches. Still, the hybrid models nudge the metadata ecosystem closer to what users look for, not just what experts assign. If e-book discovery is the goal, it's an important adjustment.

[Download PDF](2019_RecSys_HGV.pdf)
