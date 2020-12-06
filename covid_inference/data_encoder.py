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

    encodedFeatures = features.apply(lambda col: le.fit_transform(col.astype(str)), axis=0, result_type='expand')
    encodedResults = results.apply(lambda col: le.fit_transform(col.astype(str)), axis=0, result_type='expand')

    return data_processor.DataSet(encodedFeatures, encodedResults)


def clean_symptoms_column(data_frame):
    i = 0
    asymptomatic = ["asimptomatica", "asimptomatic", "asimptomatică", "asimptomatic covid", "nu", "nu are", "-", ""]
    fever = ["febra", "subfebra", "subfebrilitati"]
    cough = ["tuse", "tuse seaca"]
    tiredness = ["fatigabilitate"]
    muscular_pain = ["dureri musculare", "dureri abdominale", "durere", "durere locala"]
    shortness_of_breath = ["dispnee", "dispnee marcata"]

    for elem in data_frame['simptome delcarate']:
        if any(i in str(elem).lower() for i in asymptomatic):
            data_frame.loc[i, 'simptome delcarate'] = "asymptomatic"
        elif any(i in str(elem).lower() for i in fever):
            data_frame.loc[i, 'simptome delcarate'] = "fever"
        elif any(i in str(elem).lower() for i in cough):
            data_frame.loc[i, 'simptome delcarate'] = "cough"
        elif any(i in str(elem).lower() for i in tiredness):
            data_frame.loc[i, 'simptome delcarate'] = "tiredness"
        elif any(i in str(elem).lower() for i in muscular_pain):
            data_frame.loc[i, 'simptome delcarate'] = "muscular_pain"
        elif any(i in str(elem).lower() for i in shortness_of_breath):
            data_frame.loc[i, 'simptome delcarate'] = "shortness_of_breath"
        i += 1
    return data_frame