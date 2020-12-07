from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score 
from numpy import unique


def evaluate(inference, results):
    accuracy = accuracy_score(results, inference)
    precision = precision_score(results, inference, average='macro', labels=unique(inference))
    recall = recall_score(results, inference)
    f1 = f1_score(results, inference)
    confusion = confusion_matrix(results, inference)
    auc = roc_auc_score(results, inference)
    metrics = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1, "confusion": confusion, "auc": auc}
    print(unique(results))
    return metrics
