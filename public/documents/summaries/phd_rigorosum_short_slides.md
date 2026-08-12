# Real-time Recommender Systems in Multi-Domain Settings

## What is the challenge?

Building recommender systems that work in real time across multiple domains isn’t just a scaling problem – it’s a tangle of data heterogeneity, domain-specific needs, and constant updates. Each domain (think music, jobs, news, e-learning) comes with distinct interaction signals and metadata. On top of that, there’s demand for immediate, personalized results. Existing systems either sacrifice speed for quality or lose flexibility in the quest for scalability.

## What did we set out to learn?

My dissertation tackled the following:
- Does blending heterogeneous data sources and algorithm types make recommendations more robust?
- How can we enable customization, scalability, and true real-time performance in multi-domain settings?
- What’s the actual trade-off—quantified—between accuracy and runtime?
- How should we think about going beyond accuracy (novelty, diversity, coverage), especially for anonymous or short-lived user sessions?

## Technical insights

1. **Mixing it up helps**: Integrating extra signals (e.g., social links, location) consistently mitigates the cold start problem, boosting robustness on accuracy, diversity, and user coverage. This is especially notable at recommendation system launch or during onboarding spikes.

2. **Architecture matters**: The ScaR framework, designed with microservices thinking, allowed us to run isolated recommendation engines per domain with shared infrastructure, tailoring algorithms and data pipelines flexibly.

3. **Runtime vs. accuracy**: Sometimes, practical pre-filtering or greedy neighbor search schemes for Collaborative Filtering cut latency by 3x or more with modest accuracy loss. Embedding models (when engineered right) can also deliver both real-time speed and improved novelty/coverage.

4. **Measuring more than accuracy**: I showed that context (like which page the user is on) and session recency can matter as much as the model itself. For example, with job recommendations, users actually preferred simpler last-item strategies on detail pages, despite fancier models.

5. **Session-based learning**: Using neural autoencoders to generate session embeddings unlocked better novelty and coverage for anonymous session recommendations, with accuracy competitive to SOTA baselines.

## What’s the bottom line?

If you’re designing real-world multi-domain recommenders, you need to plan for heterogeneity, immediate feedback loops, and the fact that users don’t just want the top hit—they want surprising and suitable options. Architecture, data richness, and practical evaluation matter more than gimmicks. The work outlined new ways to measure utility beyond accuracy and sketched concrete technical patterns (and trade-offs) for scalable, real-time recommendations in multi-domain environments.

[Download PDF](phd_rigorosum_short_slides.pdf)
