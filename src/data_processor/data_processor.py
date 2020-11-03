import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def read_file(file):
    data = pd.read_excel(file)

    return data


def split_data(data):
    results = data['rezultat testare']
    features = data.drop('rezultat testare', axis='columns')

    training_data_features, testing_data_features, \
        training_data_results, testing_data_results = \
        train_test_split(features, results, train_size=0.9, random_state=0)

    training_data_features, dev_validation_data_features, \
        training_data_results, dev_validation_data_results = \
        train_test_split(training_data_features, training_data_results,
                         train_size=0.9, random_state=0)

    return training_data_features, training_data_results, \
        dev_validation_data_features, dev_validation_data_results, \
        testing_data_features, testing_data_results
