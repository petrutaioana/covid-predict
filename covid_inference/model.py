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


def train(training_ds, validation_ds):
    training_ds = data_cleaner.clean(training_ds, True)
    validation_ds = data_cleaner.clean(validation_ds, True)

    training_ds = data_encoder.encode(training_ds)
    validation_ds = data_encoder.encode(validation_ds)

    inference = model_trainer.train_and_predict(training_ds, validation_ds, 2)

    evaluation = model_evaluator.evaluate(inference, validation_ds.getResults())
    print(validation_ds.getResults())
    print(inference)
    print(evaluation)


def infer(features):
    pass


if __name__ == '__main__':
    main()
