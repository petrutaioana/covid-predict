from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

model = None


def train_and_predict(training_ds, validation_ds, algorithm):
    global model
    if algorithm == 1:
        model = DecisionTreeClassifier(random_state=0)
    elif algorithm == 2:
        model = KNeighborsClassifier()

    model.fit(training_ds.getFeatures(), training_ds.getResults().values.ravel())

    prediction = model.predict(validation_ds.getFeatures())

    return prediction


def test_predict(testing_ds):
    return model.predict(testing_ds.getFeatures())
