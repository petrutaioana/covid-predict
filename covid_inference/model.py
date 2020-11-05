import sys
import data_processor
import data_cleaner
import data_encoder
import model_trainer
import model_evaluator


def main():
    file = sys.argv[1]

    dataset = data_processor.read_file(file)

    # Clean data
    data_cleaner.clean(dataset)

    # training_dataset, validation_dataset, testing_dataset = \
    #     data_processor.split_dataset(dataset)
    #
    # train(training_dataset, validation_dataset)
    # inference = infer(testing_dataset.getFeatures())
    #
    # evaluation = model_evaluator.evaluate(inference, testing_dataset.getResults())


def train(training_dataset, validation_dataset):
    # training_dataset = data_cleaner.clean(training_dataset)
    # validation_dataset = data_cleaner.clean(validation_dataset)

    training_dataset = data_encoder.encode(training_dataset)
    validation_dataset = data_encoder.encode(validation_dataset)

    model_trainer.train(training_dataset)
    inference = model_trainer.predict(validation_dataset.getFeatures())

    evaluation = model_evaluator.evaluate(inference, validation_dataset.getResults())


def infer(features):
    pass


if __name__ == '__main__':
    main()
