# Socrecm: A scalable social recommender engine for online marketplaces

Socrecm was built to address a frequent pain point for online marketplaces: how to deliver timely, relevant recommendations when the data, and system requirements, are constantly shifting. Unlike typical recommender engines tethered to a single platform or interaction type, Socrecm is designed for scale and adaptability. The core insight is making the architecture modular, so injecting new social signals or user features doesn't cripple performance.

I focused on supporting a mix of collaborative filtering and social network-based algorithms, making them accessible through Apache Solr for ease of deployment. That means you get social-aware recommendations at near real-time, which is surprisingly hard to pull off at the scale of modern marketplaces. And it works: in our evaluations, Socrecm maintained high throughput and accuracy even as we threw more users and data at it.

Honestly, the most striking part is how cleanly the engine plugs into existing infrastructures. You don't have to retool your data pipeline from scratch—if you're using Solr, it just fits. This lowers the typical barrier for researchers and practitioners wanting to experiment with or deploy more advanced recommendation logic, especially in social and item-rich environments. The catch? Generality comes with the expected trade-offs: you won't eke out every drop of possible accuracy for niche deployments without careful tuning. But as a pragmatic, scalable solution, Socrecm moves the needle for marketplace recommendations.

[Download PDF](lacic_cv_old.pdf)
