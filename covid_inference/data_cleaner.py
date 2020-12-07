import pandas as pd

import constants as c


def clean(df, for_training):
    if not for_training:
        cleaned_features = clean_features(df.getFeatures())
        df.setFeatures(cleaned_features)

        cleaned_results = clean_results(df.getResults())
        df.setResults(cleaned_results)
    else:
        cleaned_features = clean_features_training(df.getFeatures())
        df.setFeatures(cleaned_features)

        cleaned_features_indexes = cleaned_features.index

        cleaned_results = clean_results_training(df.getResults(), cleaned_features_indexes, cleaned_features)
        df.setResults(cleaned_results)
    return df


def clean_features(df):
    # Fill null values with "NO GENDER".
    df[c.FEATURE_SEX_COLUMN_NAME] = df[c.FEATURE_SEX_COLUMN_NAME].fillna(c.NO_GENDER_VALUE)
    clean_sex_column(df)

    # Values: Z, X, y, z
    df[c.FEATURE_INSTITUT_COLUMN_NAME] = df[c.FEATURE_INSTITUT_COLUMN_NAME].fillna(0)
    df[c.FEATURE_DATA_DEBUT_COLUMN_NAME] = df[c.FEATURE_DATA_DEBUT_COLUMN_NAME].fillna(0)
    df[c.FEATURE_DATA_INTERNARE_COLUMN_NAME] = df[c.FEATURE_DATA_INTERNARE_COLUMN_NAME].fillna(0)
    df[c.FEATURE_DIAGNOSTIC_INTERNARE_COLUMN_NAME] = df[c.FEATURE_DIAGNOSTIC_INTERNARE_COLUMN_NAME].fillna(0)
    df[c.FEATURE_ISTORIC_CALATORIE_COLUMN_NAME] = df[c.FEATURE_ISTORIC_CALATORIE_COLUMN_NAME].fillna(0)
    df[c.FEATURE_TRANSPORT_COLUMN_NAME] = df[c.FEATURE_TRANSPORT_COLUMN_NAME].fillna(0)
    df[c.FEATURE_CONTACT_PERS_INFECTATA_COLUMN_NAME] = df[c.FEATURE_CONTACT_PERS_INFECTATA_COLUMN_NAME].fillna(0)
    df[c.FEATURE_DATA_REZULTAT_COLUMN_NAME] = df[c.FEATURE_DATA_REZULTAT_COLUMN_NAME].fillna(0)

    clean_symptoms_columns(df)

    return df


def clean_results(results):
    df = pd.DataFrame(results)
    df[c.LABEL_COLUMN_NAME] = df[c.LABEL_COLUMN_NAME].fillna(c.NO_RESULT)
    clean_results_column(df)

    return df


"""
Training function drop observations/features
"""


def clean_features_training(df):
    # Remove irrelevant columns.
    df = df.drop(c.FEATURE_INSTITUT_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_DATA_DEBUT_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_DATA_INTERNARE_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_DIAGNOSTIC_INTERNARE_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_ISTORIC_CALATORIE_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_TRANSPORT_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_CONTACT_PERS_INFECTATA_COLUMN_NAME, 1)
    df = df.drop(c.FEATURE_DATA_REZULTAT_COLUMN_NAME, 1)

    # Remove observations that have null values for gender.
    df = df.dropna(subset=[c.FEATURE_SEX_COLUMN_NAME])
    clean_sex_column(df)

    # Remove observations that have null values for symptoms.
    df = df.dropna(subset=[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME, c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME])
    clean_symptoms_columns(df)

    # Save to a new file.
    df.to_excel("../data/data_set_training.xlsx")

    return df


def clean_results_training(results, cleaned_features_indexes, features):
    # Print unique result values: ['NEGATIV' 'NECONCLUDENT' nan 'POZITIV' 'NEGATIB'].

    df = pd.DataFrame(results)
    to_delete = []

    # Reach the same number of observations in results after dropping lines from features
    for i in range(0, len(df.index)):
        found = False
        for j in cleaned_features_indexes:
            if df.index[i] == j:
                found = True
        if not found:
            to_delete.append(i)

    rows = df.index[to_delete]
    df.drop(rows, inplace=True)

    clean_results_column(df)

    # Remove items without a conclusive result.
    df = df.dropna(subset=[c.LABEL_COLUMN_NAME])
    df = df.drop(df[(df[c.LABEL_COLUMN_NAME] == c.NO_RESULT)].index)

    # Remove these observations from the features.
    to_delete = []
    cleaned_results_indexes = df.index
    for i in range(0, len(features.index)):
        found = False
        for j in cleaned_results_indexes:
            if features.index[i] == j:
                found = True
        if not found:
            to_delete.append(i)

    rows = features.index[to_delete]
    features.drop(rows, inplace=True)

    return df


def clean_sex_column(df):
    df[c.FEATURE_SEX_COLUMN_NAME] = df[c.FEATURE_SEX_COLUMN_NAME].str.replace(r'^M.*$', c.SEX_MASCULIN_VALUE)
    df[c.FEATURE_SEX_COLUMN_NAME] = df[c.FEATURE_SEX_COLUMN_NAME].str.replace(r'^m.*$', c.SEX_MASCULIN_VALUE)
    df[c.FEATURE_SEX_COLUMN_NAME] = df[c.FEATURE_SEX_COLUMN_NAME].str.replace(r'^F.*$', c.SEX_FEMININ_VALUE)
    df[c.FEATURE_SEX_COLUMN_NAME] = df[c.FEATURE_SEX_COLUMN_NAME].str.replace(r'^f.*$', c.SEX_FEMININ_VALUE)


def clean_symptoms_columns(df):
    # Replace all the "Asimptomatic" variants to "ASIMPTOMATIC".
    df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME].str.replace(r'^ASI.*$',
                                                                                                            c.ASIMPTOMATIC_VALUE)
    df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME].str.replace(r'^asi.*$',
                                                                                                            c.ASIMPTOMATIC_VALUE)
    df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME].str.replace(r'^Asi.*$',
                                                                                                            c.ASIMPTOMATIC_VALUE)

    df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME].str.replace(r'^ASI.*$',
                                                                                                            c.ASIMPTOMATIC_VALUE)
    df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME].str.replace(r'^asi.*$',
                                                                                                            c.ASIMPTOMATIC_VALUE)
    df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME].str.replace(r'^Asi.*$',
                                                                                                            c.ASIMPTOMATIC_VALUE)

    # Remove all number values.
    df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME].str.replace(r'\d+\,\d+', '')
    df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME].str.replace(r'\d+\.\d+', '')

    df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME].str.replace(r'\d+\,\d+', '')
    df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME].str.replace(r'\d+\.\d+', '')

    # Split the symptoms string by comma and remove heading white spaces.
    df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_DECLARATE_COLUMN_NAME].astype(str).apply(
        lambda x: x.lstrip(' ').split(','))
    df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME] = df[c.FEATURE_SIMPTOME_RAPORTATE_COLUMN_NAME].astype(str).apply(
        lambda x: x.lstrip(' ').split(','))


def clean_results_column(df):
    df[c.LABEL_COLUMN_NAME] = df[c.LABEL_COLUMN_NAME].replace(['NEGATIB'], 'NEGATIV')
