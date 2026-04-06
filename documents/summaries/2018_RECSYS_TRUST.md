# Trust-Based Collaborative Filtering: Tackling the Cold Start Problem Using Regular Equivalence

Cold-start users remain a headache for collaborative filtering, with the classic rating vector similarity simply breaking down when new users lack interaction history. We wanted to see if trust networks could do better by tapping into social signals instead of waiting for cold-start users to generate their own data.

Our approach borrows Katz similarity from network science, letting us propagate trust through user connections beyond direct links—using both regular equivalence and actual path-based structure of the network. The trick is limiting path length (l_max = 2 in our best setup), applying careful normalization to avoid popularity bias, and boosting the propagated similarities so indirect trust relationships don't get drowned out. For neighbor selection, this means we can recommend items based on users two hops away in the trust graph, not just those one step removed.

Tested on Epinions cold-start cases (users with ≤10 ratings), this outperformed naïve trust baselines and the usual most-popular fallback, with nDCG gains up to .0303 versus .0224 or less for prior methods. Most interestingly, effective trust propagation substantially boosted both recall and precision, provided normalization (especially max norm) was handled properly.

There are caveats. This only tackles accuracy for now; coverage and novelty remain open. Direct user similarity will always struggle when data is sparse, but smart trust propagation offers a clear edge—if you can handle normalization, matrix sparsity, and boosting safely. In retrospect, the biggest gains came from letting the trust signal travel just that bit further, not merely from adding more math. Future work should test whether node embeddings or deeper paths help—or just introduce noise.

[Download PDF](2018_RECSYS_TRUST.pdf)
