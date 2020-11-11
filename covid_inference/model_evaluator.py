from sklearn.metrics import accuracy_score


def evaluate(inference, results):
    print(inference)
    print(results)
    
    return accuracy_score(results, inference)
