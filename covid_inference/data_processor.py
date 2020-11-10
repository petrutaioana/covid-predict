import pandas
from sklearn.model_selection import train_test_split
import constants


class Dataset:
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


def split_dataset(dataset):
    results = dataset[constants.LABEL_COLUMN_NAME]
    features = dataset.drop(constants.LABEL_COLUMN_NAME, axis='columns')

    training_dataset_features, testing_dataset_features, \
        training_dataset_results, testing_dataset_results = \
        train_test_split(features, results, train_size=0.9, random_state=0)

    training_dataset_features, validation_dataset_features, \
        training_dataset_results, validation_dataset_results = \
        train_test_split(training_dataset_features, training_dataset_results,
                         train_size=0.9, random_state=0)

    training_dataset = Dataset(training_dataset_features, training_dataset_results)
    validation_dataset = Dataset(validation_dataset_features, validation_dataset_results)
    testing_dataset = Dataset(testing_dataset_features, testing_dataset_results)

    return training_dataset, validation_dataset, testing_dataset
