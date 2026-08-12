# Neighborhood Troubles: On the Value of User Pre-Filtering to Speed Up and Enhance Recommendations

1. **User pre-filtering for recommender systems**: This work demonstrates that pre-selecting a subset of candidate users (i.e., neighbors) before the core recommendation step can significantly speed up collaborative filtering algorithms. Rather than comparing every user, the system only considers the most promising neighbors, reducing computational cost.

2. **Evaluation and results**: Experiments showed that user pre-filtering can halve recommendation computation time without sacrificing accuracy. In some cases, accuracy actually increased, as noisy or irrelevant neighbors were excluded by design.

3. **Practical insights**: For large-scale recommendation environments (think: e-commerce, social media), these optimizations make real-time recommendations more feasible without massive infrastructure upgrades.

This approach is most beneficial in production settings with millions of users, where performance bottlenecks are common. The method's simplicity and strong empirical results add to its appeal, especially as recommender systems continue to scale.

[Download PDF](elacic_cv_old.pdf)
