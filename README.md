# Ember
## Tinder for Jobs (DSI - Capstone Project 2018)

#### Table of Contents
[Overview](Overview)

[Methodology](Methodology)


#### _Overview_

  The search for a new job is a long and tedious process filled with several frustrations. Job sites attempt to alleviate some of this frustration with advanced filters such as: location, salary range, size of company, and company ranking. Even with these filters however, users continue to face job postings that do not meet their criteria. This problem forces people to scan through dozens of jobs and save the ones they like and discard the rest.
  
  A potential solution would be to sort the postings from most similar to your criteria to least similar. This way you wouldn't be reading postings at random and ideally the first postings you would be shown would be the most likely to be saved for application later. In order to implement this solution however, each user would need a proxy for their criteria without having to write down specifically what they are looking for and what they are trying to avoid. A user's Linked In profile is a suitable choice due to the fact that most people will update their profile before or during their search for new work. Unfortunately this solution does solve the problem completely because even when sorted, a user will still have to read through several postings that will not be saved and the order is now fixed.

  A further solution would be to resort the order of postings with every user-given input. In other words, if a user chose to save or discard a job, the order of postings would be resorted based on the choice. With this algorithm in place, the first few jobs may or may not be saved by the user however, after categories have been assigned for those jobs, the user will be shown postings that are more and more likely to be saved and not discarded. It is important to note that even with this sorting algorithm job postings are not removed from the list just reordered. Therefore if one were to go through the entire stack of job postings available the last several jobs would most likely fall into the "discard" category because they have been pushed to the end of the stack. This solution is getting better, but it still involves scanning through dozens of jobs and encountering bad jobs although at a least frequent rate. What would be nice was if there was a percentage chance that a given user would save a job displayed with each job posting. This would allow the user to make a judgement about the posting without reading it. 

  The final addition to the solution is a statistical classifcation model that predicts the probability that a job will be in either the "save" category or the "discard" category. As a user continues to go through the sorted list of job postings and labels them, a training set will be created on the backend with labels. Using this training set, a model can be fit and used to predict on newly posted jobs.

#### _Methodology_     