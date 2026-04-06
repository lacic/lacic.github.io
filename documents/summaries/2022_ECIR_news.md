# What Drives Readership? An Online Study on User Interface Types and Popularity Bias Mitigation in News Article Recommendations

The usual assumption is clear: mobile news readers just mindlessly scroll and rarely tap. But the findings from our live study at DiePresse flip that on its head. While desktop users are more likely to even see the recommendations (RSR 26.9% vs. 17.6% on mobile), it’s the mobile users who click through most aggressively: a click-through rate of 13.4% (mobile) versus only 10.5% (desktop). Turns out, the effort of scrolling to the recommendations filters out casuals; those who make it, engage.

We ran a two-week experiment in October 2020, setting up personalized, content-based recommendations for over a million DiePresse readers. The overwhelming majority—89%—were anonymous, cold-start visitors, reading on mobile. Two real-life events, the COVID-19 lockdown and a major terror attack, happened during this window, giving us a rare stress-test of user attention and news needs.

But there’s another twist. “Popular” news algorithms—usually considered safe bets—skew the playing field, flooding user feeds with the same stories. By injecting personalization (based on recent and editor-selected articles, recommended via LDA topic vectors), we watched the long tail come to life—at least, for anonymous users. Over two weeks, the popularity distribution (skewness and kurtosis) flattened notably for them, reducing bias and boosting lesser-read articles. Subscribers, with clearer interests, stayed fairly balanced all along.

The messy reality: user interface matters more than most labs admit. Mobile has high engagement but low visibility; desktop is the opposite. And those massive news events? They still blow every metric out of the water, making the population chase headlines en masse, personalization be damned.

Honestly, the most actionable insight is that generalizing from offline metrics or even desktop ideas alone misses the real-world messiness of contemporary news reading. Popularity bias can be mitigated, but only if the system design—and user context—are taken seriously.

[Download PDF](2022_ECIR_news.pdf)
