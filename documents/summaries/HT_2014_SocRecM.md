# SocRecM: A Scalable Social Recommender Engine for Online Marketplaces

SocRecM addresses a set of headaches that persist for anyone deploying recommender systems in online marketplaces: integration friction, scalability barriers, lack of robust hybridization, and the challenge of meaningfully using social data. This framework is open-source, built in Java, and leverages Apache Solr for speed and flexibility.

## Architecture and Integration

SocRecM’s service-based architecture is RESTful by design – making it straightforward to drop into existing systems. Data enters the engine via dedicated connectors for both marketplace and social data sources (e.g., purchases, Facebook, Twitter). After pre-processing, everything is indexed in Solr, which powers both the algorithm layer and search functionalities.

Developers get access to four core recommendation approaches: MostPopular (MP), Collaborative Filtering (CF), Content-based (C), and Hybrid Recommendations (CCF). Each algorithm can be powered by either traditional marketplace features (purchases, titles, descriptions) or a suite of social features (likes, comments, group memberships, interest tags, even full social stream content). These data streams can also be combined in hybrid models tailored for either marketplace or social data emphasis.

## Evaluation and Performance

The system includes built-in evaluation tools, measuring standard IR metrics (Recall, Precision, nDCG, User Coverage, and more) and supports practical benchmarking right out of the box. We stress-tested SocRecM on a large SecondLife dataset (over 120k users and items, millions of interactions). Results show that social-feature-based recommenders, and especially hybrids (CCFs, CFin), outperform those using only marketplace data – but their effectiveness does depend on sufficient social data availability. Algorithms using social stream content and interests underperformed, revealing useful limits.

SocRecM's speed is a strong point, with near real-time recommendations: even the most complex hybrid approaches averaged under 60 milliseconds per query in tests.

## Why Use SocRecM?

If you're integrating recommendations into an online marketplace and want flexible, scalable, and social-aware algorithms, SocRecM provides a pragmatic and extensible engine. Everything is open-source, so it's also a baseline for further research or customization.

[Download PDF](HT_2014_SocRecM.pdf)
