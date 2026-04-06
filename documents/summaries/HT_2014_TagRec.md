# TagRec: Towards A Standardized Tag Recommender Benchmarking Framework

## What problem does TagRec solve?

Reproducibility and comparability are persistent challenges in tag recommendation research. Before TagRec, results for new algorithms could rarely be compared directly due to differing preprocessing, evaluation protocols, and baseline choices. TagRec aims to address this by offering a standardized, extensible Java framework that covers the full experimental pipeline.

## What does the framework actually provide?

- **Data Preprocessing:** Built-in tools to process and split real social tagging datasets like CiteULike, BibSonomy, LastFm, and Flickr. Includes p-core pruning, train/test splitting, and topic modeling.
- **Model Abstraction:** Fully object-oriented data model, making it easier to develop and compare algorithms.
- **Algorithm Collection:** Implements a range of well-known tag recommender algorithms and two families of novel approaches based on human cognition and memory theories (notably, 3L/3LT and BLL/BLL+C).
- **Evaluation:** Out-of-the-box evaluation using standard IR metrics (Recall, Precision, F1, MRR, MAP). Results can be filtered or grouped by user activity.

## What did we learn from benchmarking on Flickr?

Testing on a large-scale Flickr dataset (9,590 users, >3.5M tags), the framework showed:

- Most state-of-the-art algorithms outperform the basic popularity baseline, but with runtime differences that matter in practice.
- Cognition-inspired methods (BLL+C, 3LT) achieved the best combination of predictive quality and runtime, outperforming more complex approaches like LDA or tensor factorization in this setting.

## Why does this matter?

TagRec helps clean up replication and evaluation in the tag recommendation domain. Anyone with new ideas can benchmark quickly against a rich baseline set. Especially relevant: models inspired by human memory and forgetting, rather than just pure graph or matrix models, set a new bar for both quality and usability. For anyone planning serious work on tag recommenders, this framework should be a default starting point.

[Download PDF](HT_2014_TagRec.pdf)
