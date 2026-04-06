# Tackling Cold-Start Users in Recommender Systems with Indoor Positioning Systems

## What's the challenge?

Recommender systems are notorious for struggling with "extreme" cold-start users—people who have provided no item interactions and thus leave algorithms with nothing to personalize on. Popular remedies like interaction onboarding surveys and matrix factorization only help when there's at least a sliver of user activity. When no history exists, most systems fall back on unpersonalized MostPopular lists. Nobody loves those.

## What did we try instead?

This work explores using indoor positioning system (IPS) data—specifically BLE beacon traces—instead of explicit item interactions. By tracking user locations in spaces like shopping centers or conferences (without explicit user input), it's possible to infer meaningful co-location patterns. We use this location data to compute user similarity and drive a collaborative filtering recommender, with variants for raw location overlap and temporal-location-aware user networks.

## Did it help?

Yes, even when simulating "extreme" cold-start (zero-item-history) users in the FourSquare dataset, all forms of IPS-based collaborative filtering substantially outperformed the MostPopular baseline on nDCG metrics. The best gains came from an Adamic-Adar-enhanced location network, reaching about 15% nDCG@10—impressive for users where traditional personalization is impossible.

## Why does this matter?

If IPS data is available, recommender systems no longer have to settle for generic lists when facing new users. This approach adds automatic, frictionless context by leveraging users' movements—especially valuable in locations where beacons are deployed and explicit feedback is rare or annoying to collect.

We see this as just the beginning; real-world deployment (like our planned i-KNOW conference assistant) and richer context signals (movement direction, dwell time) are next on the horizon. The message is clear: Spatial context isn't just a fallback—it can drive personalization when everything else fails.

[Download PDF](RecSys_2015_CS.pdf)
