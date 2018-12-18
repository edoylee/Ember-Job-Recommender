# Ember
## Tinder for Jobs (DSI - Capstone Project 2018)

#### Table of Contents
[Overview](#overview)  
[Methodology](#methodology)  
[Modeling](#modeling)  
[Technology](#technology)  
[Next Steps](#nextsteps)  
[Conclusion](#conclusion)

<a name="overview"></a>
#### _Overview_

  The search for a new job is a long and tedious process filled with several frustrations. Job sites attempt to alleviate some of this frustration with advanced filters such as: location, salary range, size of company, and company ranking. Even with these filters however, users continue to face job postings that do not meet their criteria. This problem forces people to scan through dozens of jobs and save the ones they like and discard the rest.
  
  A potential solution would be to sort the postings from most similar to your criteria to least similar. This way you wouldn't be reading postings at random and ideally the first postings you would be shown would be the most likely to be saved for application later. In order to implement this solution however, each user would need a proxy for their criteria without having to write down specifically what they are looking for and what they are trying to avoid. A user's Linked In<sup>[1][linkedin]</sup> profile is a suitable choice due to the fact that most people will update their profile before or during their search for new work. Unfortunately this solution does solve the problem completely because even when sorted, a user will still have to read through several postings that will not be saved and the order is now fixed.

  A further solution would be to resort the order of postings with every user-given input. In other words, if a user chose to save or discard a job, the order of postings would be resorted based on the choice. With this algorithm in place, the first few jobs may or may not be saved by the user however, after categories have been assigned for those jobs, the user will be shown postings that are more and more likely to be saved and not discarded. It is important to note that even with this sorting algorithm job postings are not removed from the list just reordered. Therefore if one were to go through the entire stack of job postings available the last several jobs would most likely fall into the "discard" category because they have been pushed to the end of the stack. This solution is getting better, but it still involves scanning through dozens of jobs and encountering bad jobs although at a least frequent rate. What would be nice was if there was a percentage chance that a given user would save a job displayed with each job posting. This would allow the user to make a judgement about the posting without reading it. 

  The final addition to the solution is a statistical classifcation model that predicts the probability that a job will be in either the "Save" category or the "Discard" category. As a user continues to go through the sorted list of job postings and labels them, a training set will be created on the backend with labels. Using this training set, a model can be fit and used to predict on newly posted jobs.
<a name="methodology"></a>
#### _Methodology_

  1. Use Selenium Webdriver<sup>[2][selenium]</sup> to scrape a user's LinkedIn<sup>[3][linkedin]</sup> profile and corresponding jobs from Glassdoor<sup>[4][glass]</sup>.
  2. Use SciKit Learn's CountVectorizer<sup>[5][cv]</sup> to preprocess the profile document and remove stopwords.
  3. Use the vocabulary_ from the CountVectorizer<sup>[6][cv]</sup> as a preset "vocabulary" for a TFIDF vectorizer.
  4. Use SciKit Learn's TfidfVectorizer<sup>[7][tfidf]</sup> with the preset vocabulary to fit the profile document as well as all of the Glassdoor<sup>[8][glass]</sup> postings.
  5. Use SciPy's cosine distance metric<sup>[9][cosine]</sup> to calculate the distances between the profile vector and each of the job vectors.
  6. Use NumPy to sort the jobs from smallest distance to largest distance.
  7. Use the closest job as the first recommendation to the user.
  8. Based on the label assigned by the user, specifically "Yes" or "No", calculate a new set of distances from that job to all other jobs and add or subtract it to the original set of distances.
  9. Use the job with the new minimum distance as the next recommendation to the user.
  10. After the user exits the recommendation loop, train a classification model on the labeled jobs.
  11. Scrape recently added jobs on Glassdoor<sup>[10][glass]</sup> at regular 24 hour periods to create a suitable test set for the user.
  12. Use the trained model to predict the probability of being in the "Yes" category for the jobs in the test set.
<a name="modeling"></a>
#### _Modeling_

  Using just the tfidf numbers for the job postings, a Random Forest classification<sup>[11][forest]</sup> model was fit on the labeled training data.
  > Why Random Forest?:  
  >    * The Decision Trees can be fit in parallel which cuts down on training time.
  >    * Random Forests cannot overfit to training data by increasing the number of trees, which makes them easier to tune.
  >    * Random Forests specialize in cutting down variance across decorrelated trees.

  After the Random Forest<sup>[12][forest]</sup> is fit on the training data, extracting the feature importances will indicate which specific terms were split on in the model. Using these terms as an updated vocabulary, another classification model can be fit on the training data.

  The Gradient Boosted Classification<sup>[13][gradboost]</sup> model was fit on the training data with the updated vocabulary that was extracted from the Random Forest.

  > Why Gradient Boosting?:
  >    * Gradient Boosted models on average perform better than Random Forest and Bagging models in terms of cross validated loss metrics.
  >    * After reducing the dimensions in the model with the Random Forest, the learning rate hyperparameter can be set low to prevent overfitting, without taking too much time.
  >    * The model can be tuned to make better predictions by minimizing loss.

  The Gradient Boosted Classifier<sup>[14][gradboost]</sup> was used as the final model to predict on new job postings that were recently added to Glassdoor<sup>[15][glass]</sup>.
<a name="technology"></a>
#### _Technology_

  This project was written in Python and used several support packages such as:
* Pandas
* NumPy
* SciKit Learn
* SciPy
* Selenium Webdriver
* Flask
<a name="nextsteps"></a>
#### _Next Steps_

* Host the front end development on AWS  
  
  This project is currently being hosted on a local server, and all data collected is also being stored locally.

* Initiate an AWS Cluster equiped with PySpark
  
  If a large number of jobs are brought down from Glassdoor<sup>[16][glass]</sup> the distance calculations computed at every step may become too slow for an easy user experience. Therefore creating an AWS cluster to handle the computations will improve the speed of the program and increase user accessibility.

* Conduct Further Model Evaluation
  
  The models used in this project were chosen because they were the most practical given the number of resources. Further model evaluation is needed to find the best performing model for this specific data. Further data engineering may also be neede to improve performance.

* Explore suitable alternatives to Webscraping
  
  Due to a limit on available resources, webscraping was the most practical method of gathering data however, webscraping is temperamental at times, and may not always result in useful data collection. A potential solution to this problem would be to encourage users to fill out a new profile on this specific framework as opposed to Linked In<sup>[17][linkedin]</sup> and make an agreement with Glassdoor<sup>[18][glass]</sup> or other job sites to more reliably gather data on a ongoing basis.
<a name="conclusion"></a>
#### _Conclusion_

  Through this platform people who are searching for work can automate a frustrating and ongoing process of determining which jobs they like and intend to apply for and which ones they will discard. The data gathered for this project was from Linked In<sup>[19][linkedin]</sup>, and Glassdoor<sup>[20][glass]</sup>. A Bootstrap template was used for the front end development, combined with Flask.   

[glass]: https://www.glassdoor.com
[linkedin]: https://www.linkedin.com
[selenium]: https://www.seleniumhq.org/docs/03_webdriver.jsp
[cv]:https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
[tfidf]: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
[cosine]: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.cosine.html
[forest]: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
[gradboost]: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html 



