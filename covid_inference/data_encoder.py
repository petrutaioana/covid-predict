from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import data_processor


# def encode(dataset):
#     values = array(dataset.getFeatures())

#     #print(dataset.getFeatures())
#     #print(values)

#     #label_encoder = LabelEncoder()
#     #integer_encoded = label_encoder.fit_transform(dataset.getFeatures().values.flatten())
#     #print(integer_encoded)
#     # one hot encoding

#     onehot_encoder = OneHotEncoder()
#     #integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)


#     onehot_encoded = onehot_encoder.fit_transform(values)
#     print(onehot_encoded)
#     # invert
#     # inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
#     # print(inverted)

#     values = array(dataset.getResults())
#     integer_encoded = label_encoder.fit_transform(values)
#     integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
#     onehot_encoded2 = onehot_encoder.fit_transform(integer_encoded)

#     print(onehot_encoded2)

#     return DataSet(onehot_encoded, onehot_encoded2)

def encode(dataset):
    features = dataset.getFeatures()
    results = dataset.getResults()

    le = LabelEncoder()

    encoded_features = features.apply(lambda col: le.fit_transform(col.astype(str)), axis=0, result_type='expand')
    encoded_results = results.apply(lambda col: le.fit_transform(col.astype(str)), axis=0, result_type='expand')

    return data_processor.DataSet(encoded_features, encoded_results)
