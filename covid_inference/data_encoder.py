from sklearn.preprocessing import LabelEncoder
import data_processor


def encode(dataset):
    features = dataset.getFeatures()
    results = dataset.getResults()

    le = LabelEncoder()

    encodedFeatures = features.apply(lambda col: le.fit_transform(col.astype(str)), axis=0, result_type='expand')
    encodedResults = results.apply(lambda col: le.fit_transform(col.astype(str)), axis=0, result_type='expand')

    return data_processor.DataSet(encodedFeatures, encodedResults)
