# What is data cleaning?

Data cleaning refers to identifying and correcting errors in the dataset that may negatively impact a predictive model.

Although critically important, data cleaning is not exciting, not does it involve fancy techniques. Just a good knowledge of the dataset.

There are many types of errors that exist in a dataset, although some of the simplest errors include columns that don’t contain much information and duplicated rows.

There are X observations (lines in the dataset) with Y input variables and 1 output variable (target class variable).

# Identify Columns That Contain a Single Value

Columns that have a single observation or value are probably useless for modeling.
These columns or predictors are referred to zero-variance predictors as if we measured the variance (average value from the mean), it would be zero.

A single value means that each row for that column has the same value. Columns that have a single value for all rows do not contain any information for modeling.

You can detect rows that have this property using the nunique() Pandas function function that will report the number of unique values in each column.

```
# summarize the number of unique values in each column
print(df.nunique())
```
# Consider Columns That Have Very Few Values

We can refer to these columns or predictors as near-zero variance predictors, as their variance is not zero, but a very small number close to zero.

> … near-zero variance predictors or have the potential to have near zero variance during the resampling process. These are predictors that have few unique values (such as two values for binary dummy variables) and occur infrequently in the data.

To help highlight columns of this type, you can calculate the number of unique values for each variable as a percentage of the total number of rows in the dataset.

Summarize those variables that have unique values that are less than 1 percent of the number of rows.
This does not mean that these rows and columns should be deleted, but they require further attention.

# Remove Columns That Have A Low Variance

Variance is a statistic calculated on a variable as the average squared difference of values on the sample from the mean.
The variance can be used as a filter for identifying columns to removed from the dataset. A column that has a single value has a variance of 0.0, and a column that has very few unique values will have a small variance value.

### Resources
* Most of the information is taken from [here](https://machinelearningmastery.com/basic-data-cleaning-for-machine-learning/). 

### Disclaimer 
* All the info will be edited, right now it's just a information dump file.
* This file will contain only the algorithms/methods used for constructing the final model.