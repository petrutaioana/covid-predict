import sys
import numpy as np
import data_processor


def clean_contact_with_infected_person_column(data_frame):
    i = 0
    no = ["nu", "neaga", "-", "fara", "0"]
    yes = ["da", "covid", "posibil", "focar", "pozitiv"]

    for elem in data_frame['confirmare contact cu o persoană infectată']:
        if any(i in str(elem).lower() for i in no):
            data_frame.loc[i, 'confirmare contact cu o persoană infectată'] = "nu"
        elif any(i in str(elem).lower() for i in yes):
            data_frame.loc[i, 'confirmare contact cu o persoană infectată'] = "da"
        i += 1
    return data_frame


def clean_transport_used_column(data_frame):
    i = 0
    no = ["nu", "neaga", "-", "fara", "0", "O"]
    yes = ["da", "masina", "tren", "autocar", "avion", "ambulanta"]

    for elem in data_frame['mijloace de transport folosite']:
        if any(i in str(elem).lower() for i in no):
            data_frame.loc[i, 'mijloace de transport folosite'] = "nu"
        elif any(i in str(elem).lower() for i in yes):
            data_frame.loc[i, 'mijloace de transport folosite'] = "da"
        i += 1
    return data_frame


def clean(data_frame):
    # get the data frame without columns that contain numbers
    table = data_frame.drop(data_frame.columns[[2, 3, 5, 11]], axis='columns')

    # select columns from the data frame without containing numbers
    columns_without_numbers = table.select_dtypes(include=[np.object]).columns

    # standardize data frame characters to ASCII values
    data_frame[columns_without_numbers] = data_frame[columns_without_numbers].apply(
        lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    # clean contact with infected person column data
    data_frame = clean_contact_with_infected_person_column(data_frame)

    # clean transport used column data
    data_frame = clean_transport_used_column(data_frame)

    return data_frame


def get_missing_values_from_column(index, data_frame, data_frame_columns):
    counter = 0
    for elem in data_frame[data_frame_columns[index]].isnull():
        if elem:
            counter += 1
    return counter


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


if __name__ == '__main__':
    # get the data frame from the Excel file
    data = data_processor.read_file(sys.argv[1])

    # get number of columns from data frame
    nr_cols = len(data.axes[1])

    # select all columns from the data frame
    columns = data.select_dtypes(include=[np.object]).columns

    data = clean(data)

    # compute the number of missing values from every column in the data set
    idx = 0
    while idx < nr_cols:
        column_missing_info = get_missing_values_from_column(idx, data, columns)
        print("Column " + str(columns[idx]).upper() + " has " + str(column_missing_info) + " missing values.")
        idx += 1

    get_statistics(data)
