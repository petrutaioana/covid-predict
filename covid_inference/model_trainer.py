from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


def train(training_ds, validation_ds, algorithm):
    if algorithm == 1:
        model = DecisionTreeClassifier(random_state=0)
    elif algorithm == 2:
        model = KNeighborsClassifier()

    model.fit(training_ds.getFeatures(), training_ds.getResults())

    prediction = model.predict(validation_ds.getFeatures())

    return prediction


def predict(features):
    pass
