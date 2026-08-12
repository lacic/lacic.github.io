---
paper: 2023-frontiers-in-big-data-beyond-accuracy
generated: 2026-08-12
---

Graph neural networks (GNNs) have reshaped collaborative filtering, driving accuracy gains that are now standard in recommender systems. But as the community obsesses over precision metrics, important dimensions—diversity, serendipity, and fairness—often remain afterthoughts. This review addresses that gap by surveying recent advances and highlighting how GNN-based recommenders can (and should) move beyond the singular focus on accuracy.

The paper examines concrete strategies to optimize these beyond-accuracy objectives through the full lifecycle of GNN-based model development: from preprocessing and graph construction to embedding design, propagation, fusion, and the selection of specialized loss functions. For diversity, methods span everything from submodular neighbor selection to contrastive co-training, yielding richer item discovery and preventing over-concentration on popular content. Serendipity and novelty receive attention through normalization tactics and architecture innovations, while fairness is increasingly tackled using multimodal graphs and contrastive learning to combat popularity bias and ensure balanced exposure for users and providers.

Perhaps the most practical contribution is the mapping of which stages of the modeling process matter for which objectives. The review doesn't pretend the solutions are easy—trade-offs between accuracy and beyond-accuracy metrics are real, and implementation challenges persist, particularly when scaling to large catalogues with sparse user feedback. We included a comprehensive summary table to guide readers through the varied approaches, metrics, and techniques in recent literature—something still missing from much of the field's work.

If the field takes these findings seriously, GNN recommenders can become more robust, ethically sound, and genuinely user-centric, instead of just accurate. The challenge now is to push beyond benchmarks and engage with the conflicting demands of real users and real-world equity.
