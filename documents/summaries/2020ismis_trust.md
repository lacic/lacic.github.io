# Empirical Comparison of Graph Embeddings for Trust-Based Collaborative Filtering

Key takeaways from this paper:

1. **Random walk graph embeddings lead the pack for trust-based collaborative filtering in cold-start scenarios.** Node2vec and DeepWalk consistently outperformed classic trust baselines and other embedding families on three real-world datasets (Epinions, Ciao, FilmTrust). The result is not just better accuracy, but higher novelty and diversity in recommendations—a somewhat rare combination.

2. **User coverage improves noticeably with embeddings.** Traditional trust-based recommenders always struggle with sparsity: if a user's trust links are few, recommendations barely reach them. By learning latent representations from the graph (instead of relying on explicit trust alone), embedding methods provided recommendations for substantially more users—practical for real platforms with lots of cold-start users.

3. **Accuracy and novelty correlate positively—users actually prefer novel content when accuracy is held constant.** That observation isn't new, but the correlation is unusually strong here (Kendall rank: up to 0.43). This means optimizing solely for accuracy may also give you novelty, at least on datasets structured like these.

A few notes on setup: All trust graphs were treated as undirected (to maximize comparability and reduce sparsity), which is a pragmatic but imperfect choice because it discards directionality of trust—a potentially valuable signal. Some methods (like SDNE) underperformed, likely due to insufficient hyperparameter search. More broadly, trust networks are messy, and this study clarifies that no single metric should dominate evaluation: novelty, diversity, and coverage matter concretely.

These insights suggest that for real-world recommender systems facing cold starts, graph embeddings—especially random walk variants—are a safe bet. But the devil is in the details: network structure, method family, and how we handle edge direction all matter. Next steps include exploring trust directionality and coupling embeddings with user features from ratings, aiming for interpretable, high-coverage, well-balanced recommendations.

[Download PDF](2020ismis_trust.pdf)
