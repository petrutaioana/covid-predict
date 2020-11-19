from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import data_processor

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