from sklearn.metrics import accuracy_score


def evaluate(inference, results):
    return accuracy_score(results, inference)
