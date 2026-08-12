# Real-Time Recommendations in a Multi-Domain Environment

Modern recommender systems face a bigger challenge than just improving accuracy—they have to operate across multiple domains, handle diverse, streaming data, and offer real-time results that react to rapidly changing user preferences. Most established methods look at one domain with a static, periodic update cycle. That’s not enough anymore, especially as application scales and user expectations grow.

This dissertation investigates how recommender systems can efficiently combine different types of data—items, social signals, location information—to generate more robust, context-aware recommendations instantly, not hours or days later. Experiments show that blending these data sources isn’t just theoretically appealing, it genuinely improves performance, especially when dealing with recommendations across varying category levels or domain specializations.

To make this practical, the work introduces a flexible framework built on two key ideas: using search engines like Apache Solr to ingest and process updates in real-time, and deploying the system via a microservices architecture. This allows each domain (marketplaces, news sites, hotels) to run its own isolated, scalable recommendation service that customizes data features and algorithms per domain, with a dedicated microservice to keep things in sync.

The approach bridges the gap between large-scale data requirements, speed, and flexibility—showing that real-time, multi-domain recommenders aren’t just possible, but practical with the right mix of technologies and design choices.

[Download PDF](SigWeb_2017.pdf)
