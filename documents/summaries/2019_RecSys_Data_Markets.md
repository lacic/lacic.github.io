# Using the Open Meta Kaggle Dataset to Evaluate Tripartite Recommendations in Data Markets

Recommendation in data markets is a more nuanced problem than traditional user-item settings, adding a layer of complexity by introducing services alongside users and datasets. In this work, we formalized four distinct recommendation use cases corresponding to different interactions within a tripartite graph: recommending datasets to users, services to users, datasets to services, and services to datasets.

We implemented and evaluated two standard algorithms—most popular (MP) and collaborative filtering (CF)—across these scenarios, using the open Meta Kaggle dataset as a real-world proxy. The results make it clear that algorithm choice must depend on the structural properties of the recommendation problem. For cases with a limited set of candidate items, such as recommending datasets to users or to services, simple popularity-based recommendations often outperform more sophisticated approaches. For example, in the dataset-to-user task, the MP baseline achieved higher accuracy (P@1: 0.823) than CF (P@1: 0.705), contrary to typical collaborative filtering superiority in standard recommender system benchmarks.

As the recommendation task becomes more complex, particularly when linking entities with less direct interaction data (e.g., services to users or services to datasets), CF begins to surpass popularity-based methods—not dramatically, but sufficiently to be a better fit. Still, the performance even with CF in the most complex case (services for datasets) is underwhelming (nDCG@10: 0.009), hinting that both approaches struggle with high sparsity and the indirect linkage inherent in these cases.

This evaluation exposes the pitfalls of assuming a single method can fit all scenarios in data markets. The structure of the candidate pool, the available interaction data, and the mapping between entities fundamentally shift what works. The next step is obvious: incorporating content-based or hybrid approaches is necessary for the hardest tasks, as MP and CF alone clearly hit a ceiling in utility as tripartite complexity grows.

[Download PDF](2019_RecSys_Data_Markets.pdf)
