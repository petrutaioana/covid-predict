"""
Functions used for generating data reports
"""

import numpy as np


def compute_unique_values_number(data_frame):
    print(data_frame.nunique())


def compute_unique_values_percentage(data_frame):
    counts = data_frame.nunique()
    (rows, cols) = data_frame.shape

    print('[Nume coloana] [Valori unice in obs] [Procent raportat la nr. linii]\n')
    for i in range(cols):
        percentage = float(counts[i]) / rows * 100
        if percentage < 1:
            print('%s: %d, %.1f%%' % (counts.index[i], counts[i], percentage))


def compute_missing_values_from_column(index, data_frame, data_frame_columns):
    counter = 0
    for elem in data_frame[data_frame_columns[index]].isnull():
        if elem:
            counter += 1
    return counter


def get_missing_values_from_column(data_frame):
    # get number of columns from data frame
    nr_cols = len(data_frame.axes[1])
    # select all columns from the data frame
    columns = data_frame.select_dtypes(include=[np.object]).columns
    idx = 0
    while idx < nr_cols:
        column_missing_info = compute_missing_values_from_column(idx, data_frame, columns)
        print("Column " + str(columns[idx]).upper() + " has " + str(column_missing_info) + " missing values.")
        idx += 1


def get_people_gender(data_frame, gender):
    counter = 0
    for elem in data_frame['sex']:
        if str(elem).lower() == str(gender):
            counter += 1
    return counter


def get_people_result(data_frame, result):
    counter = 0
    for elem in data_frame['rezultat testare']:
        if str(elem).lower() == str(result):
            counter += 1
    return counter


def get_number_of_transport_used(data_frame, answer):
    counter = 0
    for elem in data_frame['mijloace de transport folosite']:
        if str(elem).lower() == answer:
            counter += 1
    return counter


def get_number_of_contacted_with_infected_people(data_frame, answer):
    counter = 0
    for elem in data_frame['confirmare contact cu o persoană infectată']:
        if str(elem).lower() == answer:
            counter += 1
    return counter


def get_institution_tests(data_frame, institution):
    counter = 0
    for elem in data_frame['instituția sursă']:
        if str(elem).lower() == institution:
            counter += 1
    return counter


def get_statistics(data_frame):
    print("########## STATISTICS ##########")
    # compute people's gender
    men = get_people_gender(data_frame, "masculin")
    print("Number of men is " + str(men))
    women = get_people_gender(data_frame, "feminin")
    print("Number of women is " + str(women))

    # compute people's diagnostic
    negatives = get_people_result(data_frame, "negativ")
    print("Number of negative people is " + str(negatives))
    positives = get_people_result(data_frame, "pozitiv")
    print("Number of positive people is " + str(positives))
    inconclusive = get_people_result(data_frame, "neconcludent")
    print("Number of inconclusive people is " + str(inconclusive))

    # get the number of people who came in contact with someone infected
    positive_contact = get_number_of_contacted_with_infected_people(data_frame, "da")
    print(str(positive_contact) + " people came in contact with someone infected.")
    negative_contact = get_number_of_contacted_with_infected_people(data_frame, "nu")
    print(str(negative_contact) + " people did not come in contact with someone infected.")

    # get the number of people who used transport
    positive_transport = get_number_of_transport_used(data_frame, "da")
    print(str(positive_transport) + " people used transportation.")
    negative_transport = get_number_of_transport_used(data_frame, "nu")
    print(str(negative_transport) + " people did not use transportation.")

    # get the number of tests done by each institution
    institution_x = get_institution_tests(data_frame, "x")
    print("Institution X has done " + str(institution_x) + " tests.")
    institution_y = get_institution_tests(data_frame, "y")
    print("Institution Y has done " + str(institution_y) + " tests.")
    institution_z = get_institution_tests(data_frame, "z")
    print("Institution Z has done " + str(institution_z) + " tests.")
