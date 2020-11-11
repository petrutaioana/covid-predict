import sys
import data_processor
import data_cleaner
import data_encoder
import model_trainer
import model_evaluator


def main():
    file = sys.argv[1]

    ds = data_processor.read_file(file)

    training_ds, validation_ds, testing_ds = data_processor.split_ds(ds)

    train(training_ds, validation_ds)

    inference = infer(testing_ds.getFeatures())

    # evaluation = model_evaluator.evaluate(inference, testing_ds.getResults())


def train(training_ds, validation_ds):
    training_ds = data_cleaner.clean_for_training(training_ds)
    validation_ds = data_cleaner.clean_for_training(validation_ds)

    # print("Cleaned data")
    # print(validation_ds.getResults())
    # print(validation_ds.getFeatures())

    training_ds = data_encoder.encode(training_ds)
    validation_ds = data_encoder.encode(validation_ds)

    # print("Encoded data")
    # print(validation_ds.getResults())
    # print(validation_ds.getFeatures())

    inference = model_trainer.train(training_ds, validation_ds, 1)
    #inference = model_trainer.predict(validation_ds.getFeatures())

    evaluation = model_evaluator.evaluate(inference, validation_ds.getResults())
    print(evaluation)

def infer(features):
    pass


if __name__ == '__main__':
    main()
