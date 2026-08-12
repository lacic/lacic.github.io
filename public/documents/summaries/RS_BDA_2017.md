# Studo Jobs: Enriching Data With Predicted Job Labels

## What's the challenge?

Modern job platforms struggle with messy, unstructured data. For students especially, navigating job listings is tough—the free-text descriptions vary wildly, and relevant filters are missing. Automatic labeling could turn this influx of ads into something much easier to search and recommend, but the question is: which algorithms actually work for job ad classification?

## What did we try?

We tackled this practical headache by running a head-to-head comparison of classic and modern classifiers on real job listings. We gathered over 5,600 ads from Austrian job platforms, focusing on four key categories used in Studo Jobs: Software, Catering, Technology, and Business. For each label, we constructed balanced datasets and evaluated everything from Naive Bayes and Decision Trees to SVMs and deep neural networks—including CNNs and multi-layer perceptrons. Metrics: accuracy, F1, and AUC, all with rigorous cross-validation.

## What actually worked?

Linear SVM and especially SVM with stochastic gradient descent consistently outperformed the rest—achieving F1 scores up to 0.92 for the most common labels. Deep CNNs looked promising (and outperformed for some cases like Catering), but honestly, without careful tuning or early stopping they didn't eclipse the refined linear baselines. Naive Bayes, while simple, still provided competitive results for certain labels. The catch: model effectiveness varied by label size and definition, and some categories (like "Business") muddied the waters due to label merging.

## Takeaways and next steps

If you need to enrich job data for a real-world platform, start with SVM and careful dataset balancing. CNNs aren’t magic here until you’ve really dialed in the hyperparameters. Automatic labels substantially improve browse-ability and recommendation potential—a practical win for students. In the future, we're extending the study with more features, refined deep learning models, and eventually live user testing to see if this leads to faster, more relevant job discovery.

[Download PDF](RS_BDA_2017.pdf)
