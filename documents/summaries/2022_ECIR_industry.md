# Recommendations in a Multi-Domain Setting: Adapting for Customization, Scalability and Real-Time Performance

Modern recommender systems rarely have the luxury of a single, homogeneous domain. In this work, we address what it takes to build systems that support recommendation tasks across vastly different application contexts—without sacrificing speed or customizability.

The core of our approach is a microservice-based recommender engine flexible enough to support job marketplaces one day and entrepreneurial platforms the next. The system employs standard algorithms—collaborative filtering, content-based filtering, plus neural embeddings like Doc2Vec and Autoencoders—but the real value lies in how these components are modular and tuned per domain. Algorithmic choices, data structures, and optimization criteria can all be customized according to use case: recommending job postings to students in one scenario, matching start-up co-founders or innovation experts in another.

Achieving real-time performance is a sticking point, especially when simultaneous requests come from vastly different domains. We leverage distributed architectures and search engine technology (e.g., Apache Solr) to keep latency down, even when computing recommendations on-the-fly with fresh input. In practice, the online performance is highly dependent on the context in which recommendations are shown—location context, for instance, affects job listing relevance. In the startup use case, the data is much more intricate and dynamic, requiring the system to handle heterogeneous profiles, innovation topics, and even education materials.

What's obvious in retrospect: there is no universal recommendation model for all domains. Instead, adaptability at the architectural level—using service isolation and algorithmic swapping—proves more sustainable and robust than hunting for a single superior algorithm. This system has held up in both research pilots and live industry deployments, which is rare for frameworks aimed at multi-domain scalability and real-time use cases.

[Download PDF](2022_ECIR_industry.pdf)
