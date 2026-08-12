# Uptrendz: API-Centric Real-time Recommendations in Multi-Domain Settings

Uptrendz tackles a perennial problem in recommender systems: most platforms are tied to a single domain, rigid data model, and the sort of piecemeal custom logic that makes scaling across applications a headache. This work introduces a pragmatic solution—a genuinely API-centric platform that can support multiple domains in real-time, with each domain enjoying isolated data storage, customizable upload APIs, and targeted recommendation models.

The core insight is simple but powerful: you shouldn't be forced to rewrite the backend every time a new data schema or business case comes along. Uptrendz abstracts this away; for every domain—be it MovieLens-style movie recommendations or entrepreneurial start-up support—you can define item/user attributes, upload data through bespoke APIs, and generate timely recommendations with off-the-shelf or hybrid algorithms. It takes the pain out of data heterogeneity and service isolation; each domain is provisioned as a microservice, so load peaks or failures in one don't spill into the others.

There are real-world demos to back it up: classic collaborative, content-based, and popularity models running on MovieLens, and a more eclectic start-up matching scenario, each with domain-specific customization and hybridization. The platform is built on the ScaR framework but exposes a much friendlier API layer.

Honestly, the real win here is practical: if you're building or maintaining recommenders for multiple products or business units, Uptrendz saves you from tangled codebases and the endless refactor treadmill. It’s not magic AI. It's thoughtful engineering, for messy real-world data and evolving requirements.

[Download PDF](2023_ECIR_uptrendz.pdf)
