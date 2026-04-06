# Beyond Accuracy Optimization: On the Value of Item Embeddings for Student Job Recommendations

Conventional job recommendation systems for students often fixate on accuracy, ranking jobs by how closely they match previous user activity. In practice—especially on mobile platforms with limited display—it’s quickly obvious this approach stumbles. When job postings share repetitive content (which many do), recommendations end up bland and redundant, limiting both diversity and actual usefulness for users seeking new opportunities.

In this work, we focused on the real trade-offs between accuracy, diversity, and novelty in student job recommendation on the Studo platform. We experimented with neural item embeddings (Doc2Vec) to represent job postings, capturing semantic connections beyond just raw text similarity. Three methods were used to craft reference vectors for recommendations: relying on the most recent job interaction (LAST), averaging over a user’s job history (AVG), and, crucially, a novel application of the Base-Level Learning (BLL) equation from human memory theory. The BLL method weights past interactions by both recency and frequency, aiming to more realistically model what jobs actually stay meaningful to a student over time.

The results highlight some useful surprises. Standard collaborative filtering and popularity-based approaches yielded reasonable accuracy and diversity, but seriously lagged in novelty—the recommendations gravitated toward overexposed positions, risking user disengagement. Traditional content-based filtering, meanwhile, tipped the scale too far in the other direction: high novelty (recommending obscure jobs), but at the expense of both relevance and diversity.

What made a difference was integrating item embeddings with frequency-recency modeling through the BLL equation. This approach delivered a notably better balance—good accuracy, strong diversity, and novelty scores that actually aligned with the jobs students chose to apply to. In fact, by combining the BLL-based content model with user-based collaborative filtering, we came close to matching the ideal novelty value derived from true applications.

If there’s a core takeaway, it’s that optimizing accuracy in isolation is shortsighted. Incorporating cognitively-inspired, frequency-recency-aware embeddings enables genuinely useful recommendations, better mirroring what students want and might actually pursue. For real-world systems, especially in crowded markets like student job portals, this balance can make all the difference.

[Download PDF](WSDM2018_IFUP.pdf)
