# Popularity Bias in Collaborative Filtering-Based Multimedia Recommender Systems

In collaborative filtering (CF)-based multimedia recommender systems, popularity bias is the elephant in the room. The standard algorithms resourcefully personalize lists, but everyone in the field suspects they systematically over-recommend popular items and ignore the long tail. What’s been missing is a clear mapping of *how bad* this is for different types of users across several media domains. That’s the gap we targeted here.

Across four representative datasets—music (Last.fm), movies (MovieLens), digital books (BookCrossing), and anime (MyAnimeList)—we grouped users by their explicit inclination toward popular items (LowPop, MedPop, HighPop). This enabled a granular analysis not just of how frequently popular items are recommended (item-level bias), but also of who is most affected (user-level bias).

**Key findings:**
- **Popular items dominate rec lists** for all algorithms and datasets. The probability of an item being recommended is tightly coupled to its underlying popularity, regardless of user profile.
- **LowPop users get the short end of the stick:** Despite having the largest and richest user profiles—making them theoretically valuable for system learning—users uninterested in popular items consistently receive *significantly* worse recommendations (as measured by MAE). This holds across all datasets and algorithms tested (UserKNN, UserKNNAvg, NMF, CoClustering).
- **The problem is consistent across domains:** Music, movies, books, anime—the effect persists. We even see statistically robust differences (p < 0.001) in accuracy depending on user group.

This is unsettling. If your system’s best data sources (the LowPop cohort) are the ones getting the least satisfying recommendations, something is fundamentally broken. Current CF approaches don’t just reinforce the popularity bias at the item level; they embed a kind of user-level unfairness that disadvantages the very profiles that—given their engagement and diversity—should be prized.

So, where does this leave us? Reducing popularity bias is not just about surfacing more niche content. It’s a question of treating diverse user interests equitably—especially since these users are vital for effective recommendations. Mitigation strategies need to move beyond post-hoc re-ranking or minor tweaks. Algorithms should directly account for user engagement patterns and intentionally correct for this imbalance—otherwise, systems may keep failing their most engaged and distinctive users.

[Download PDF](2022_ECIR_bias.pdf)
