# TagRec: Towards a Toolkit for Reproducible Evaluation and Development of Tag-Based Recommender Algorithms

Tag-based recommender systems are everywhere in social platforms, but the lack of standard evaluation pipelines and diverse, sometimes incompatible implementations has made progress slower—and less reproducible—than it should be. TagRec is our answer: an open-source, Java-based framework tailored to the realities (and headaches) of research in folksonomy-based recommendations.

**Why TagRec is different:**

1. **Full-stack reproducibility:** Data pre-processing, model building, algorithm comparison, and evaluation are all integrated, with consistent protocols and tooling.
2. **Breadth of algorithms:** With over 30 algorithms (including classics like FolkRank, tensor factorization such as PITF, and new entrants based on cognitive psychology like ACT-R and MINERVA2-derived models), TagRec should cover nearly any angle of tag or item prediction research.
3. **Plug-and-play extensibility:** All algorithms share a common interface, and external libraries (e.g., LibFM) can be connected. New methods slot in cleanly.
4. **Benchmarking at scale:** We evaluated algorithms on several large real-world datasets (BibSonomy, CiteULike, Delicious, Flickr, MovieLens), measuring standard IR metrics like Recall, nDCG, MAP, and run-time.

**Empirical takeaways:**
- Cognitive-inspired models (3LTtag+MPr, BLL+C) are not only fast but also outperform more complex, factorization-based methods for tag recommendation. This runs contrary to much of the hype about deep models in recent years.
- For item recommendation, re-ranking with tag and time (CIRTT) comes out on top for both accuracy and diversity. Simpler collaborative filtering models still hold their ground for speed.
- The evaluation experiments surface subtle but critical findings: for instance, tag co-occurrence is not always more informative than time/frequency dynamics; the supposed complexity of tensor methods doesn't always pay off.

There's a philosophy behind TagRec: if recommender research is to be cumulative, transparent, and future-proof, we need shared infrastructure. TagRec is our stake in the ground for the tag-based recommender community. Contributions, criticisms, and new algorithms welcome. The project remains open source and under active development.

[Download PDF](TagRec_SigWeb.pdf)
