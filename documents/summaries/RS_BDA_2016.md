# Recommending Social Care Institutions

## What problem are we addressing?

Social care institutions, despite their essential role, often become information haystacks. People seeking help struggle to find the right provider; social workers face a mountain of time-consuming inquiries. Add strong privacy requirements—no personal data, full anonymity—and it's easy to see why automated solutions are rare in this sector.

## How does our approach work?

We designed a hybrid content-based recommender system specifically for recommending social care institutions. The system pulls from three data sources: (1) institution metadata, (2) institution FAQs, and (3) a record of resolved user questions. Each source is modeled using TF-IDF-based text similarity. The system combines these scores, but we added two crucial factors: **time context** and **negative feedback**. The time context (using a Base-Level Learning/activation equation) means that more recent and relevant matches are ranked higher, reducing obsolete or misleading recommendations when institutions change focus. Negative feedback from users (easy to collect thanks to the system's UI) actively reduces an institution's score, so repeated mismatches make that option less likely for future searchers.

## Why does this matter?

A key finding: this kind of hybrid, feedback-aware approach is feasible and effective even when forced to operate under strict privacy constraints. There is no user profiling—just content matching and feedback loops. In our real-world deployment (an Austrian district), 85+ institutions were included, and within 8 months we saw nearly 3,000 user questions and as many feedback responses. The system is live, not just theoretical.

## What’s interesting or challenging?

Without the ability to track individuals, methods like collaborative filtering aren't usable. Our method's reliance on multi-source content, freshness, and real-time feedback is not only practical, it's necessary here. This also means that handling cold starts (new institutions, new question types) becomes possible, since we're not waiting on user history to build up. 

Moving forward, we're interested in dynamically re-weighting data sources based on feedback and in exploring sentiment analysis on user queries.

[Download PDF](RS_BDA_2016.pdf)
