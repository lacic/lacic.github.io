# Neighborhood Troubles: On the Value of User Pre-Filtering to Speed Up and Enhance Recommendations

Traditional user-based collaborative filtering (UB-CF) hits a notorious bottleneck: as user-item data grows, calculating similarities across potentially huge candidate sets slows down recommender systems—sometimes to a crawl. Add to this the push for real-time recommendations, and suddenly UB-CF feels like an old engine struggling on a race track.

This work takes a direct shot at this pain point. We propose a simple—almost greedy—user pre-filtering step before similarity calculations. Instead of comparing a target user to every possible neighbor, we use Apache Solr's faceting to efficiently pull only the top-N users with the highest overlap in consumed items. This shrinks the candidate set to a fraction of its original size, focusing computational effort only where there's a fighting chance of relevance.

The most striking result: **runtime drops by more than 23x**—from roughly two seconds per recommendation down to below 90 milliseconds—without any exotic hardware or heavy system optimizations. But the pleasant surprise is that accuracy also improves, as measured by nDCG, with optimum results found around N=60 neighbors. Pre-filtering doesn’t just make the system faster; it actively boosts recommendation quality.

We validated this approach on a large, sparse Foursquare dataset. While only one dataset, the findings suggest that heavy, brute-force neighbor calculations are not just slow—they’re suboptimal. In our setup, the pre-filtered solution performed on par with naïve popularity-based baselines for speed, but substantially better for recommendation relevance.

There are caveats. We need broader validation, as all tests were on a single dataset type. Still, these initial results are compelling: when every millisecond and CPU cycle counts, narrowing the pool with a smart filter isn’t just a hack—it may be the best way forward for next-generation scalable recommenders.

[Download PDF](2018_CIKM_CF.pdf)
