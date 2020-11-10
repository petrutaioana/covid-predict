import pandas
from sklearn.model_selection import train_test_split
import constants


class DataSet:
    def __init__(self, features, results):
        self.__features = features
        self.__results = results

    def getFeatures(self):
        return self.__features

    def getResults(self):
        return self.__results

    def setFeatures(self, features):
        self.__features = features

    def setResults(self, results):
        self.__results = results


def read_file(file):
    return pandas.read_excel(file)


def split_ds(ds):
    results = ds[constants.LABEL_COLUMN_NAME]
    features = ds.drop(constants.LABEL_COLUMN_NAME, axis='columns')

    training_ds_features, testing_ds_features, training_ds_results, testing_ds_results = \
        train_test_split(features, results, train_size=0.9, random_state=0)

    training_ds_features, validation_ds_features, training_ds_results, validation_ds = \
        train_test_split(training_ds_features, training_ds_results, train_size=0.9, random_state=0)

    training_ds = DataSet(training_ds_features, training_ds_results)
    validation_ds = DataSet(validation_ds_features, validation_ds)
    testing_ds = DataSet(testing_ds_features, testing_ds_results)

    return training_ds, validation_ds, testing_ds
