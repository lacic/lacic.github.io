# AFEL-REC: A Recommender System for Providing Learning Resource Recommendations in Social Learning Environments

## How AFEL-REC Works

AFEL-REC is built for social learning environments, not just generic recommendation tasks. The architecture stands on top of the scalable ScaR framework, with Apache Solr powering high-performance search and storage, and Apache ZooKeeper handling distributed communication and scaling. The system is designed as a set of distinct modules: a Service Provider for client interaction, a Data Modification Layer for CRUD operations, a modular Recommender Engine, and tooling for customization and offline/online evaluations.

This structure allows for flexibility: AFEL-REC can process traditional user-resource interactions, but also richer social learning data such as tags. Seven core recommendation use cases are defined, ranging from simple popularity-based suggestions for new (cold-start) users, through collaborative filtering via interactions or shared tags, to context-sensitive recommendations and recommendations tailored to specific learning goals.

## What We Tested

In preliminary evaluations, we focused on three use cases using data from Didactalia—a large Spanish social learning platform:
- **MostPopular (MP)**: recommends the most interacted-with resources.
- **Collaborative Filtering by Interactions (CFi)**: recommends based on shared resource interactions.
- **Collaborative Filtering by Tags (CFt)**: recommends based on shared tags between users.

The dataset featured 1.87 million user-resource interactions, over a million users, and nearly half a million tags. For evaluation, standard train-test splits were used, and we measured accuracy via Recall, Precision, F1, MRR, MAP, and nDCG, plus user coverage.

## What We Learned

- MP guarantees full user coverage (100%), but at the cost of extremely low accuracy.
- CFi offers far better accuracy than MP, but only reaches 40% of users (many lack sufficient interaction data for personalized recs).
- CFt outperforms both on almost all accuracy metrics and increases coverage to 53%. The takeaway: **leveraging tags as social signals enables both more accurate and more widely applicable recommendations than relying on user interactions alone.**

Tag-based collaborative filtering is especially useful in social learning platforms, where tags are abundant even when interaction data is sparse. For practitioners, this means that even with limited click data, incorporating tagging activity can significantly improve the value and scope of recommendations.

[Download PDF](2018_CIKM_AFEL.pdf)
