from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


model = ''


def train(training_ds, algorithm):
    if algorithm == 1:
        model = DecisionTreeClassifier(random_state=0)
    elif algorithm == 2:
        model = KNeighborsClassifier()

    model.fit(training_ds.getFeatures(), training_ds.getResults())


def predict(features):
    prediction = model.predict(features)

    return prediction
