# -*- coding: utf-8 -*-
"""assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uB0aJJL6uImV20cTT946HmHD_l6Os11a

# Assignment 2 ― Classification

## 0. Introduction

In this second assigment, we will explore another cornerstone of machine learning: supervised classification. We will be specifically classifying IMDB movie reviews by their positive (1) or negative (-1) score. To do this, we will first pre-process the raw data by cleaning and turning each review into a vector. Then, we will explore and fine-tune our use of the following learning algorithms for classification: naive Bayes classifiers, support vector machines, and random forests. 

* [Question 1.1](#scrollTo=m0QxxH3KngAg)
* [Question 2.1](#scrollTo=6VWSBN37uXod)
* [Question 2.2](#scrollTo=CuW0ahvaJtOt)
* [Question 2.3](#scrollTo=co54Ubd5QJDN)
* [Question 3.1](#scrollTo=fN-dse1NBQnk)
* [Question 3.2](#scrollTo=wfCjr-JrEJya)
* [Question 3.3](#scrollTo=l1iGVZtkE5fF)
* [Question 4.1](#scrollTo=YKLBuWjmAKoJ)
* [Question 5.1](#scrollTo=Myn-42J9ACsH)
* [Question 5.2](#scrollTo=1LAqa9be_3vR)
* [Question 6.1](#scrollTo=C144CYOeYPca) [Optional] 
* [Question 6.2](#scrollTo=rnIbpGe-Z52z) [Optional] 
* [Question 6.3](#scrollTo=W6CdJGpjcK2r) [Optional] 



$% latex commands for later use$
$\newcommand{\R}{\mathbb{R}}$
$\newcommand{\B}{\mathbb{B}}$
$\newcommand{\argmax}{\operatorname*{arg\ max}}$
$\newcommand{\given}{\; \vert \;}$

## 1. Importing Libraries and Data

For this assignment, we will be using a dataset of IMDB reviews. The data consists of a csv file where the first column is a string containing a user review and the second column specifies whether the review was positve (1) o negative (-1). First, we will import any libraries that we might use.

**Note:** You may use any library you would like unless specified otherwise.

### Question 1.1 Importing Libraries

Keep on adding in the section below any modules you use as you are completing the assignment.
"""

import csv
import random
### Answer starts here ###
from sklearn.metrics import accuracy_score
from sklearn import svm
import re
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
### Answer ends here ###font

"""Let's download the dataset:"""

!wget https://raw.githubusercontent.com/McGillAISociety/BootcampAssignmentDatasets/master/data/assignment2/train_reviews.csv

"""And create a function to print a review:"""

def print_review(review, score):
  print('--------------- Review with score of {} ---------------'.format(score))
  print(review)
  print('------------------------------------------------------')
  print()

"""Let's load the data and see what the first 10 reviews look like:"""

with open('train_reviews.csv') as csv_file:
  csv_reader = csv.reader(csv_file)
  colnames = next(csv_reader)  # skip column names
  data = list(csv_reader)

for review, score in random.sample(data, 10):
  print_review(review, score)

"""## 2. Preprocessing
 We will be converting our data into a binary bag-of-words representation (Google "binary bag-of-words"). To do this, we will perform two steps beforehand.

### Question 2.1 Cleaning the train data
Create a function called `clean`, which takes a string and then:

 1. lower-case all words 
 2. only keeps letters and spaces
 

 We also need to get rid of [HTML tags](https://www.javatpoint.com/html-tags) as they do not hold valuable information for classifying the review. A quick Google search on removing HTML tags with `regular expressions` will show you how to do this! 
  
  For example, the following review...
  
  >`This was the WORST movie I have EVER SEEN!! <br/>`
  
  ...will be cleaned to become:
  
  >`this was the worst movie i have ever seen`
  
   Of course, you could do more pre-processing steps if you would like, such as lemmatization, stemming, etc... but TOTALLY OPTIONAL!
"""

def clean(review):
  ### Start of Answer ###
  cleanr = re.compile('<.*?>|[^a-zA-Z\d\s]')
  review = re.sub(cleanr, '', review)
  return review.lower()
  ### End of Answer ###

"""Test your function with this example string"""

print(clean("This was the WORST movie I have EVER SEEN!! <br/> "))

"""Now, we'll use the function to clean the whole dataset. We'll also turn the scores from strings to integers while we're at it."""

X_train = []
y_train = []
for review, score in data:
  X_train.append(clean(review))
  y_train.append(int(score))

"""### Question 2.2 Picking features

We now need to turn each review into vectors. We will pick the 10,000 most recurring words in the train set as features

Using those 10,000 features, create a function called `vectorize` which will take a string as an input, and convert it to a vector using the binary bag of words representation.

For example, the string `"This movie made me cry"` will become a vector of size 10,000 with 5 elements being 1 (assuming each word is part of the 10,000 most common) and 9995 being 0, that it, is i will look something like

 > `[0, 0, ..., 0, 1, 0, ..., 0, 1, 0..., 0, 1, 0, ..., 0, 1, 0 ..., 0, 1, 0, ..., 0, 0]`
 
 In order to accomplish this task, you will
 
 1. write a `get_vocab` function which takes as an argument a list of (cleaned) reviews and the vocabulary size and outputs the a list of size `vocab_size` containing the most common words.
 2. write a `vectorize` function which takes as an argument a review and the vocabulary and turns the review into its binary bag of words representation.
 3. use the `vectorize` function to create a new variable called `X_train_vect` which will contain the bag-of-words representation of each data point contained in the `X_train` variable rather than its string representation.

**Warning**: the last step may take up to 15 minutes depending on your implementation. Despite the execution speed not being evaluated in this assignment, do try your best to have fast and efficient code!
"""

def get_vocab(reviews, vocab_size):
  ### Answer starts here ###
  splitrs = []
  for review in reviews:
    splitrs += review.split()
  return [word for word, word_counter in Counter(splitrs).most_common(vocab_size)]
  ### Answer ends here ###

"""Test your function with the following code. The `vocabulary` variable should have a length of 10,000 and the most common words should be "the", "and", "a", etc."""

num_features = 10000
vocabulary = get_vocab(X_train, num_features)
print(len(vocabulary))
print(vocabulary)

def vectorize(review_string, vocab):
  ### Answer starts here ###
  splitr = review_string.split()
  vector = [0]*num_features
  for word in splitr:
    if word in vocab:
      vector[vocab.index(word)] = 1
  return vector
  ### Answer ends here ###

"""Test your function with the following input. The vector should have four "1"s."""

vector = vectorize("the and a of zyxw", vocabulary)
print(vector)
print(sum(vector))

"""Now, vectorize the whole dataset."""

### Answer starts here ###
X_train_vect = [vectorize(x, vocabulary) for x in X_train]
### Answer ends here ###

for i in range(5):
  print_review(X_train_vect[i], y_train[i])

"""For convenience, we will write a function called `preprocess_sample_point` which takes as input a single raw review and ouputs its binary bag-of-words representation."""

def preprocess_sample_point(review, vocab):
  return vectorize(clean(review), vocab)

vectorized_review = preprocess_sample_point(
    'The movie was not bad, it was really good!', vocabulary)
print(sum(vectorized_review))
print(vectorized_review)

"""### Question 2.3 Preparing the test set

Now that we have defined a cleaning function and extracted the features from the train set, we are ready to preprocess the test set. Implement the `preprocess` function below such that it:

1. Loads the raw data from a csv file 
2. Cleans and vectorizes the reviews
3. Converts the scores to `int`
4. Returns the data into a  `(X_test, y_test)` tuple
"""

def preprocess(csv_filename, vocab):
  ### Answer starts here ###
  with open(csv_filename) as csv_file:
    csv_reader = csv.reader(csv_file)
    colnames = next(csv_reader)  # skip column names
    data = list(csv_reader)
  
  X = []
  y = []
  for review, score in data:
    X.append(vectorize(clean(review), vocab))
    y.append(int(score))

  return (X, y)
  ### Answer ends here ###

!wget https://raw.githubusercontent.com/McGillAISociety/BootcampAssignmentDatasets/master/data/assignment2/test_reviews.csv

X_test, y_test = preprocess('test_reviews.csv', vocabulary)

for i in range(5):
  print_review(X_test[i], y_test[i])

"""##3. Naive Bayes
Later in this assignment, we will use pre-existing implementations of two types of models: random forests and support vector machines. However, we will start first by implementing from sratch a third type of classifier: naive Bayes classifers. Unfortunately, Naives Bayes performs poorly on this dataset and you should expect accuracies around ~40%. Regardless, implementing it from scratch will be a good learning experience. 

Naive Bayes classifiers are part of a larger family of classifiers which are called 'probabilistic classifiers': not only do they try to predict classes given features, but they also estimate probability distributions over a set of classes.

First, let's will go over some definitions:

**Definition:** A *prior probability* is the likelihood of an event given no further assumptions. For instance, the probability that it's raining is relatively low.

**Definiton:** A *posterior probability* or *conditional probability* is the likelihood of an event given that some other event has occurred. For instance, the probability that it's raining given that there are clouds is higher than if we don't make that assumption.

Now we will go over some motivation:

For the purpose of argument, imagine we had access to the probability distribution $\Pr$. That is, we know how likely features and classes are. For example, $\Pr(x_1 = 1)$ is the probability that the most common word, i.e. "the", is in a random movie review. Presumably, this probability is relatively high. As a second example, $\Pr(y = 1)$ is the probability that a random movie review is 'good'. In our case, this would be somewhere close to 0.67.

Since we hypothetically have access to the whole probability distribution, we also know conditional probabilities. For instance, we would know $\Pr(y = 0 \; \vert \; x_1 = 0)$, which is the probability that a random review is 'bad', given that it does not contain the word "the".

Given a probability distribution, we can find an optimal classifier which simply picks the class which maximizes the probability that we will see that class given the observed features, in other words our classifier $f: \B^n \to \B$ is given by:

$$ f(x_1, \ldots, x_n) = \argmax_{c \in \B} \Pr(y = c \given x_1, \ldots, x_n ).$$

Where $\argmax$ returns the element in $\B$ which maximizes the expression to its right, and $\B$ is the set with two elements, $\{0, 1\}$. For example, we have
$$ \argmax_{x \in \R} (x - x^2) = \frac 1 2, $$
since $\frac 1 2$ maximizes the expression $x - x^2$.

It would be great if we had access to the probability distribution $\Pr$, but unfortunately we don't in almost every case. This means we wish to try to estimate it given some samples, i.e. the training data.

However, we run into another issue: estimating the probability distribution is computionally expensive. Therefore, we assume that the different features are independent from one another. This is called the *naive conditional independence assumption*. In other words, we assume that

$$ \forall i \in \{1, \ldots, n\} : \Pr (x_i \given y, x_1, \ldots, x_{i-1}, x_{i+1}, \ldots, x_n) = \Pr(x_i \given y).$$

Using Bayes' Theorem, we can simplify the conditional independence assumption to:

$$\Pr(y \given x_1, \ldots, x_n) = \frac{\Pr(y) \prod_{i=1}^n \Pr(x_i \given y)}{\Pr(x_1, \ldots, x_n)}.$$

However, we can observe that the denominator is constant for a given input, so it's not actually necesarry to estimate it if all we want is to find the class with the maximum posterior probability. In other words,

$$ \Pr(y \given x_1, \ldots, x_n) \propto \Pr(y) \prod_{i=1}^n \Pr(x_i \given y), $$

so, our classification rule becomes

$$ f(x_1, \ldots, x_n) = \argmax_{y \in \B} \Pr(y) \prod _{i=1}^n \Pr(x_i \given y).$$

Where $\propto$ means "proportional to" and  $\prod_{i = 1}^n g(i)$ is like summation $\left(\sum_{i=1}^n g(i)\right)$, except that addition is replaced with multiplication. For example,

$$\prod_{i = 1}^5 i^2 = 1^2 \cdot 2^2 \cdot 3^2 \cdot 4^2 \cdot 5^2.$$

**Note**: To estimate prior and conditional probabilities, we use the ratios of occurence counts found in the dataset. For example, to estimate $\Pr(x_1 = 0 \; \vert \; y = 0)$, we have to calculate the number of instances of class zero for which $x_1 = 0$ and divide them by the number of instances of class 0.

**Note**: The naive independence assumption is usually false in practice for most features. Therefore, the resulting estimated probability distribution is usually a bad approximation of the true distribution. However, the resulting classifier often has a good performance, depending on the dataset.

### Quesiton 3.1 Estimating the Probability Distribution

It would be expensive to re-estimate prior and posterior probabilities every time, so we should save probabilities in memory.

Thus, you will need to save
1. $\Pr(y)$ for each $y \in \B$, and
2. $\Pr(x_i = u \; \vert \; y)$ for each $ i \in \{1, \ldots, n\}$, $u \in \mathbb{B}$ and $y \in \mathbb{B}$.

Remember that you are *estimating* the probabilities using the training set only.
"""

### Answer starts here ###
prob_y = []
prob_x_if_y = []

good_prob = 0
bad_prob = 0
good_prob_x = np.zeros(num_features)
bad_prob_x = np.zeros(num_features)
for i in range(len(X_train_vect)):
  if y_train[i] == 1:
    good_prob +=1
    good_prob_x = np.add(good_prob_x, X_train_vect[i]) 
  if y_train[i] == -1:
    bad_prob += 1
    bad_prob_x = np.add(bad_prob_x, X_train_vect[i])

good_prob = good_prob/len(X_train_vect)
bad_prob = bad_prob/len(X_train_vect)
good_prob_x = np.true_divide(good_prob_x,len(X_train_vect))
bad_prob_x = np.true_divide(bad_prob_x,len(X_train_vect))

prob_y.append([-1 ,bad_prob])
prob_y.append([1 ,good_prob])
prob_x_if_y.append([-1, bad_prob_x])
prob_x_if_y.append([1, good_prob_x])

print(prob_y)
print(prob_x_if_y)
### Answer ends here ###

print(np.array(prob_y).shape)
print(np.array(prob_x_if_y).shape)
print(prob_x_if_y[0])

"""### Question 3.2 Creating the Naive Bayes Classifier

Create a function called `naive_bayes` which will take as input a list of features $x_1, \ldots, x_n$ and outputs the class with the largest posterior probability given the input features.
"""

def naive_bayes(vec):
  ### Answer starts here ###
  prob_good = prob_y[1][1]
  prob_bad = prob_y[0][1]
  for i in range(len(vec)):
    if vec[i] == 1:
      prob_good = prob_good * prob_x_if_y[1][1][i]
      prob_bad = prob_bad * prob_x_if_y[0][1][i]
  if prob_good >= prob_bad:
    return 1
  else:
    return -1
  ### Answer ends here ###

"""### Question 3.3 Measuring Performance

Using the naive Bayes classifier, predict the classes for each sample point in the training set as well as the test set and print accuracies.

**Note:** You should get train and test accuracies of about 40-45%.

**Hint:** You can use the `accuracy_score` function provided by `sklearn.metrics`
"""

### Answer starts here ###
y_pred = []
for x in X_test:
  y_pred.append(naive_bayes(x))
print(accuracy_score(y_test, y_pred))
### Answer ends here ###

print(naive_bayes(preprocess_sample_point(
    'Terrible. Horrible. Boring. This movie is bad', vocabulary)))

print(naive_bayes(preprocess_sample_point(
    'very nice good amazing good', vocabulary)))

"""## 4. Support Vector Machines

Quick recap of SVM: A support vector classifier tries to find the best separating hyperplane through the data. If the data is linearly separable, it finds a hyperplane that maximizes the margin. If it isn't, the classifier tries to minimize the cost associated with misclassifying points.

### Question 4.1 Creating a Support Vector Classifier
Using `scikit-learn`, create a support vector classifier for our review data.

1. Use `scikit-learn` to create a linear support vector classifer (name it `svm_clf`)
2. Fit the model to our training set
3. Print training accuracy
4. Print test accuracy
"""

### Answer starts here ###
svm_clf = svm.LinearSVC()
svm_clf.fit(X_train_vect, y_train)
### Answer ends here ###

print(accuracy_score(y_train, svm_clf.predict(X_train_vect)))

print(accuracy_score(y_test, svm_clf.predict(X_test)))

print(svm_clf.predict([preprocess_sample_point(
    'Boring. Such a bad movie. It was terrible and predictable', vocabulary)]))

print(svm_clf.predict([preprocess_sample_point(
    'I really liked this movie, it\'s great!', vocabulary)]))

"""## 5. Random Forests

Random forests are a type of ensemble classifier, i.e. they are made up of a number of 'weak' learners where the final classification is a combination of the classifications of each learner.

### Question 5.1 Creating a Random Forest Classifier
Using `scikit-learn`, create a radom forest classifier for our review data.

1. Use `scikit-learn` to create a random forest classifier (name it `rfc`)
2. Fit the model to our training set
3. Print training accuracy
4. Print test accuracy



Be sure to check the [documentation](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html). Try to play around with the hyperparameters to see if you can get higher accuracy. Specifically, try finding good values for `n_estimators`, `min_samples_split`, `max_depth` and `max_features`. Try to get accuracies close to the SVM's!
"""

### Answer starts here ###
rfc = RandomForestClassifier(n_estimators=1200,
                             max_depth=25, 
                             max_features='auto', 
                             min_samples_split=12)
rfc.fit(X_train_vect, y_train)
### Answer ends here ###

print(accuracy_score(y_train, rfc.predict(X_train_vect)))

print(accuracy_score(y_test, rfc.predict(X_test)))

print(rfc.predict([preprocess_sample_point(
    'Boring. This movie is terrible', vocabulary)]))

print(rfc.predict([preprocess_sample_point(
    'This movie was pretty good', vocabulary)]))

"""### Question 5.2 Manual hyperparameter tuning

Tell us about your hyperparamter tuning in a few sentences! What was your approach? Which paramters did you try changing? Were you able to improve your accuracies? (no right answer, just tell us what you experiemented with!)

#############

I've played with the parameters with no clear theoretical understanding. As far as I know, increasing the n_estimators, max_depth and min_samples_split as much as possible increased the accuracy by 10%.

#############

## 6. [Optional] Tuning hyperparameters with GridSearchCV
In this **optional** section, we will explore how to exhaustively tune the hyperparameters of a new classifier using `sklearn's` [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html).

### Question 6.1 Creating an Adaboost classifier
In this section, we will be tuning the hyperparameters of an `adaboost` model. 

As its `sklearn` [documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html) mentions, this classifier "begins by fitting a classifier on the original dataset and then fits additional copies of the classifier on the same dataset but where the weights of incorrectly classified instances are adjusted such that subsequent classifiers focus more on difficult cases." 

For this question, simply create an instance of the classifer and name it `abc`.
"""

### Answer starts here ###

### Answer ends here ###

"""### Question 6.2 Finding the best parameters
In order to use GridSearchCV, we need to provide it with a classifier (here, `abc`) and lists of different values for the hyperparameters we want to tune. GridSearchCV will run a fit using each possible parameter and get crossvalidation scores. 

For this question, use the GridSearchCV documentation to:
1. Create a dict of parameters to tune with their respective list of values
2. Create an instance of GridSearchCV with `abc` as the estimator and the following arguments: `cv=5, refit=False, verbose=3`
3. Print the resulting scores and determine which parameters are best!
"""

### Answer starts here ###

### Answer ends here ###

"""### Question 6.3 Final result with best parameters
Using the best parameters found in the previous question, reinstantiate an `adaboost` classifier, fit it to the train data, and print the the accuracy score on the test set.
"""

### Answer starts here ####

### Answer ends here ####

"""## 7. Recap and conclusion
Congratulations on reaching the end of Assignment 2! We hope you enjoyed it. 

Here's a recap of tasks and concepts explored in this assignment:


1.   **Preprocessing**
*   Cleaning train data: removing punctuation and HTML tags
*   Basic feature engineering: vectorizing data, bag-of-words representation 
*   Using learned vocabulary to preprocess test data

Preprocessing and data representation are very important in Natural Language Processing (NLP) projects. For more advanced preprocessing techniques, we highly recommend checking online the concepts of **stemming**, **n-gramming**, **stopwords removal**!

2.   **Naive Bayes**
*   Naive Bayes: recap of theory
*   Implementing model from scratch

Find out more about Naive Bayes implementations in `sklearn`: [GaussianNB](http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html), [MultinomialNB](http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html), and more!

3.   **Support Vector Machine**
*   SVM: brief recap of theory and testing
*   First introduction to `sklearn`: using already implemented models to classify data

4.   **Random Forests**
*   Random Forests: brief recap of theory and testing
*   Introduction to hyperparameter tuning

The default parameters are not always good enough! Find out more about how to tune hyperparameters in `sklearn` [here](https://scikit-learn.org/stable/modules/grid_search.html) or do the optional section 6 of this assignment. 

5.   **Tuning Adaboost with GridSearchCV**
*   Adaboost: bried recap of theory and testing 
*   Tuning hyperparameters using GridSearchCV

## 8. Submission

To submit your work, please download as a .py file and upload it to its respective okpy assignment.
"""