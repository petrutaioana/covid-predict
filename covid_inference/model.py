import sys
import data_processor
import improved_data_cleaner
import data_encoder
import model_trainer
import model_evaluator
import constants


def main():
    file = sys.argv[1]

    ds = data_processor.read_file(file)

    training_ds, validation_ds, testing_ds = data_processor.split_ds(ds)

    train(training_ds, validation_ds)
    test(testing_ds)
    infer()


def train(training_ds, validation_ds):
    training_ds = improved_data_cleaner.clean(training_ds)
    validation_ds = improved_data_cleaner.clean(validation_ds)

    training_ds = data_encoder.encode(training_ds)
    validation_ds = data_encoder.encode(validation_ds)

    inference = model_trainer.train_and_predict(training_ds, validation_ds, 2)

    evaluation = model_evaluator.evaluate(inference, validation_ds.getResults())

    print("### TRAINING & VALIDATION  RESULTS  ###")
    print(evaluation)
    print()


def test(testing_ds):
    testing_ds = improved_data_cleaner.clean(testing_ds)
    testing_ds = data_encoder.encode(testing_ds)

    inference_testing = model_trainer.test_predict(testing_ds)

    evaluation_testing = model_evaluator.evaluate(inference_testing, testing_ds.getResults())

    print("### TESTING RESULTS  ###")
    print(evaluation_testing)
    print()


def infer():
    file = sys.argv[2]

    ds = data_processor.read_file(file)

    results = ds[constants.LABEL_COLUMN_NAME]
    features = ds.drop(constants.LABEL_COLUMN_NAME, axis='columns')

    dataset = data_processor.DataSet(features, results)

    test(dataset)

if __name__ == '__main__':
    main()
