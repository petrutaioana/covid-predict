from data_processor import data_processor


def main():
    data = data_processor.read_file('../mps.dataset.xlsx')

    training_data_features, training_data_results, \
        dev_validation_data_features, dev_validation_data_results, \
        testing_data_features, testing_data_results = \
        data_processor.split_data(data)


if __name__ == '__main__':
    main()
