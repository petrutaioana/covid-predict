# Inference for Covid suspected pacients
This project implements a solution for computing the inference for patients suspected of Covid.

## Project dependencies
To install the dependencies needed to run the project, from the project's root folder run:
```
pip3 install -r requirements.txt
```

## Coding style
To check the code against good coding style practices, from the project's root folder run:
```
pycodestyle covid_inference
```

## Performance Metrics
Performance metrics measurements are decisive when dealing with imbalanced data sets, to form an idea of the
effectiveness of the algorithm implemented to detect patients suspected of COVID. Therefore, we analyzed the
following elements: accuracy, precision, recall, F1 score, confusion matrix and AUC (Area Under the Curve).

### Accuracy
Accuracy represents the rate of our model being correct, by calculating the sum
of True Positive (TP) and True Negative (TN) values and then dividing by total
number of individuals.\
In our case, the values obtained for accuracy are:
 * training stage: `0.8982758620689655`
 * testing stage: `0.9100775193798449`
### Precision
Precision is the rate of values that measures the accuracy of positive predictions.
This information can be obtained after dividing True Positives (TP) by total
number of positive people. Precision value lies between 0 and 1 and indicates
what percentage is truly positive out of all the positive predicted.
* Precision = TP / (TP + FP)

In our case, the values obtained for precision are:
 * training stage: `0.5170454545454546`
 * testing stage: `0.6244131455399061`
 
### Recall
Recall represents the rate of values that measures positive instances that were
correctly identified by our model. It is also called sensitivity, or the true
positive rate. In other words, this notion informs us about what percentage of
individuals are predicted positive out of the total number of positives.
* Recall = TP / (TP + FN)

In our case, the values obtained for recall are:
 * training stage: `0.5027925960402421`
 * testing stage: `0.514461557118603`

### F1 score
Represents the harmonic mean of precision and recall. It takes both false positive
and false negatives into account. Therefore, it performs well on an imbalanced
data set.
* F1 score = 2 / (1 / Precision + 1 / Recall)

In our case, the F1 scores obtained are:
 * training stage: `0.4895508584555259`
 * testing stage: `0.508642429336976`

### Confusion matrix
This notion refers to a matrix of size 2x2 for classifying individuals in the data
set, more precisely actual values are located on one axis and predicted ones on
another. Therefore, the 4 terms that make up this matrix refer to patients labeled
as true positive (TP), true negative (TN), false positive (FP) and false negative
(FN).

![Confusion matrix](/doc/Confusion_matrix.png)

* True Positive (TP): model correctly predicts the positive tested people.
* True Negative (TN): model correctly predicts the negative tested people.
* False Positive (FP): model gives a wrong prediction for an individual, 
estimating that someone is positive although in reality is negative.
* False Negative (FN): model gives a wrong prediction for an individual, 
estimating that someone is negative although in reality is positive.

With the help of these four values, it is possible to calculate True Positive
Rate (TPR), False Negative Rate (FPR), True Negative Rate (TNR), and False
Negative Rate (FNR).
* TPR = TP / Actual Positive = TP / (TP + FN)
* FNR = FN / Actual Positive = FN / (TP + FN)
* TNR = TN / Actual Negative = TN / (TN + FP)
* FPR = FP / Actual Negative = FP / (TN + FP)

Even if data is imbalanced, we can figure out that our model is working well or
not. For that, the values of TPR and TNR should be high, whereas FPR and FNR should
be as low as possible.

The resulting confusion matrices for our model are:
 * training stage: `[[520,   7], [ 52,   1]]` --> 520 people were classified as 
True Negatives (TN), 52 False Negatives (FN), 7 False Positives (FP) and 1
True Positive (TP)

    TPR = `0.0188679245283019`\
    FNR = `0.9811320754716981`\
    TNR = `0.9867172675521822`\
    FPR = `0.0132827324478178`
 
 * testing stage: `[[585,   4], [ 54,   2]]` --> 585 people were classified as 
True Negatives (TN), 54 False Negatives (FN), 4 False Positives (FP) and 2
True Positives (TP)

    TPR = `0.0357142857142857`\
    FNR = `0.9642857142857143`\
    TNR = `0.9932088285229202`\
    FPR = `0.0067911714770798`

### AUC (Area under the ROC Curve)
An ROC (Receiver Operating Characteristic) curve is a graph showing the performance
of a classification model at all classification thresholds.
 
This curve plots two parameters, True Positive Rate (TPR) and False Positive Rate
(FPR).

![AUC](/doc/AUC.svg)

AUC measures the entire two-dimensional area underneath the entire ROC curve
from (0,0) to (1,1). The more it is closer to 1, the better the classification
has been performed. One way of interpreting AUC is as the probability that
model ranks a random positive example more highly than a random negative example.
A model whose predictions are 100% wrong has an AUC of 0.0. Contrariwise, one 
whose predictions are 100% correct has an AUC of 1.0.

In our case, the values obtained for AUC are:
 * training stage: `0.502792596040242`
 * testing stage: `0.514461557118603`
