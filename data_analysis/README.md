# Data analysis - mentions

By default, if a value is not filled in the Excel file, in will be interpreted as NaN by the pandas library.
Pandas will recognize both empty cells and “NA” types as missing values.

The `iloc` indexer for Pandas Dataframe is used for integer-location based indexing / selection by position.

I have normalized the words present in the data set, in order to remove diacritics and any specific language accents.

# Cleaned data
For now, the only columns that I succeeded to purify are the ones stating if a person came in contact with someone
infected and if any transportation was used.
All of these features are implemented in the `data_cleaner.py` file, which also contains several helpful methods for
further investigating the data set. 

# Accuracy
In order to ensure a proper level of accuracy for our algorithm, it is mandatory to have a data set as smooth as
possible. Therefore, we should find a way to standardise all the values with identical meanings but different
expressions. Equally, it is extremely important to decide which details are useful for the algorithm computation and
which are not. For now, I consider that information like gender or age might be redundant.
Moreover, we need to pay attention at the fact that some values have nothing to do with COVID disease. In the same
manner, some words were incorrectly introduced in inappropriate columns and we will need to decide how to tream them.

# Statistics

I have managed to realise some stats about the:
* number of missing values from a column
* number of tests done per institution
* number of people tested for COVID-19 and their test result
* the number of women and men tested
* the number of people that used transportation
* the number of people who came in contact with an infected person

### Resources
* [Natural Language Processing (NLP) with Python — Tutorial](https://medium.com/towards-artificial-intelligence/natural-language-processing-nlp-with-python-tutorial-for-beginners-1f54e610a1a0).
* [Pythonic Data Cleaning With Pandas and NumPy](https://realpython.com/python-data-cleaning-numpy-pandas/)
* [Data Cleaning with Python and Pandas: Detecting Missing Values](https://towardsdatascience.com/data-cleaning-with-python-and-pandas-detecting-missing-values-3e9c6ebcf78b)
* [Practical Guide to Data Cleaning in Python](https://towardsdatascience.com/practical-guide-to-data-cleaning-in-python-f5334320e8e)

