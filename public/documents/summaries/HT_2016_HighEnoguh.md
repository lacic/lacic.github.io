# High Enough? Explaining and Predicting Traveler Satisfaction Using Airline Reviews

## What is the real question here?

Air travelers now write piles of reviews, but what actually drives their satisfaction? Which parts of all that data are truly useful for understanding and predicting whether someone would recommend an airline or airport? That's what we set out to untangle using the Skytrax review dataset.

## So, what features matter most?

From a careful feature correlation analysis, a few patterns are clear. For airports, queuing time, shopping options, and terminal cleanliness are surprisingly predictive—much more than, for instance, WiFi quality. In lounges, it's all about comfort, catering, staff, and cleanliness. As for airlines, value-for-money dominates. And for seats: legroom, width, and space trump everything else. If a review says, “cramped for 10 hours,” you can guess the rest.

But here's a twist I found especially practical: The *sentiment* of free-text reviews is almost as predictive as any explicit star rating. In some categories, it’s even the second-best signal. When structured features are missing, sentiment saves the day. Not obvious, but it matches what you see anecdotally—tone often tells you everything.

## Does this let us predict satisfaction?

We formulated a binary classification task: will the user recommend, or not? Using the optimal combination of high-correlation rating features, we get very high accuracy (F1 score up to 0.96 for airports). Sentiment-only models trail slightly but remain surprisingly competitive—hugely useful when no rating metadata exists. For realistic testing, we trained on past reviews and predicted on the most recent data to simulate live environments.

## Anything unexpected?

Cluster analysis of review text revealed overlooked topics (like immigration controls, boarding, or gate labeling) that users care about but that aren’t in the current rating scheme. Airlines and platforms can use this to expand their feedback forms—always something missing in the tick-boxes.

**Bottom line:** Focusing on the right mix of features (not just overall star ratings, but targeted categories plus sentiment) provides a robust basis for both analyzing and predicting traveler satisfaction. This is good news for both industry practitioners and researchers looking for practical, explainable signals—not just black-box accuracy.

[Download PDF](HT_2016_HighEnoguh.pdf)
