import sys
import data_processor
import numpy as np
import pandas as pd


def clean(df):
    cleaned_features = clean_features(df.getFeatures())
    df.setFeatures(cleaned_features)

    cleaned_results = clean_test_result(df.getResults())
    df.setResults(cleaned_results)
    return df


"""
Training function drop observations/features
"""


def clean_features(df):
    df = drop_irrelevant_columns(df)

    df = clean_sex(df)

    df = clean_age(df)

    df = clean_declared_symptoms(df)

    df = clean_declared_symptoms_hospitalization(df)

    df = clean_diagnostic(df)

    # leave shit where it should be
    df = drop_irrelevant_columns_symptoms(df)

    df = clean_travel_history(df)
    df = df.drop('istoric de călătorie', 1)

    df = clean_transportation(df)
    df = df.drop('mijloace de transport folosite', 1)

    df = clean_contacted_someone_infected(df)
    df = df.drop('confirmare contact cu o persoană infectată', 1)

    return df


def drop_irrelevant_columns(df):
    df = df.drop('instituția sursă', 1)

    df = df.drop('dată debut simptome declarate', 1)

    df = df.drop('dată internare', 1)

    df = df.drop('data rezultat testare', 1)

    return df


def clean_sex(df):
    df['sex'] = df['sex'].str.replace(r'^(M|m).*$', 'M')
    df['sex'] = df['sex'].str.replace(r'^(F|f).*$', 'F')

    df = df.fillna('M')
    return df


def convert(age):
    age = list(age.split(" "))
    index = len(age) - 1
    sum = 0
    while index > 0:
        if age[index] == 'L':
            sum += int(age[index - 1]) / 12
            index -= 2
            continue
        if age[index] == 'A':
            sum += int(age[index - 1])
            index -= 2
            continue
        if age[index] == 'S':
            sum += int(age[index - 1]) / 52
            index -= 2
            continue
        if age[index] == 'O':
            sum += int(age[index - 1]) / 8760
            index -= 2
            continue
        index -= 1
    return str(sum)


def clean_age(df):
    df = df.fillna({"vârstă": 52})
    df["vârstă"] = df["vârstă"].astype(str)
    df["vârstă"] = df["vârstă"].str.strip()
    # L = numar de luni
    # S = numar de saptamani
    # A = numar de ani
    # O = numar de ore
    # Z = numar de zile
    # NOU NASCUT = 0 ani

    df['vârstă'] = df['vârstă'].str.replace(r'( Luni| LUNI| luni| LUNA| luna)', ' L')
    df['vârstă'] = df['vârstă'].str.replace(r'(Luni|LUNI|luni|LUNA|luna)', ' L')
    df['vârstă'] = df['vârstă'].str.replace(r'SAP', 'S')
    df['vârstă'] = df['vârstă'].str.replace(r'ani|ANI|AN', 'A')
    df['vârstă'] = df['vârstă'].str.replace(r'ORE|ore', 'O')
    df['vârstă'] = df['vârstă'].str.replace(r' ZILE| zi', ' Z')
    df['vârstă'] = df['vârstă'].str.replace(r'ZILE|zi', ' Z')
    df['vârstă'] = df['vârstă'].str.replace(r'NOU NASCUT', '0')

    df['vârstă'] = df['vârstă'].apply(lambda x: convert(x) if ' ' in x else x)
    # df['vârstă'] = df['vârstă'].apply(lambda x: '100' if int(x) > 100 else x)

    # df['vârstă'] = df['vârstă'].astype(float).astype(int)

    return df


def clean_declared_symptoms(df):
    # simptome declarate -> just the important ones df['fever'], df['cough'], df['diarrhea'], df['muscle_soreness'], df['shortness_of_breath']

    df['simptome declarate'] = df['simptome declarate'].fillna('X')
    df["simptome declarate"] = df["simptome declarate"].str.strip()
    df['simptome declarate'] = df['simptome declarate'].str.replace(
        r'.*(ASIMPTOMATICA|ASIMPTOMATICĂ|Asimptomatica|ASIMPTOMATIC|Asimptomatic|asimptomatic|asimptomatica).*', 'X')
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'(-|nu are)', 'X')
    df['simptome declarate'] = df['simptome declarate'].str.lower()

    df['fever'] = df['simptome declarate'].apply(
        lambda x: True if 'febra' in str(x) or 'subfebrilitati' in str(x) else False)

    df['cough'] = df['simptome declarate'].apply(
        lambda x: True if 'tuse' in str(x) or 'tuse seaca' in str(x) else False)

    df['diarrhea'] = df['simptome declarate'].apply(lambda x: True if 'diaree' in str(x) else False)

    df['muscle_soreness'] = df['simptome declarate'].apply(
        lambda x: True if 'musculare' in str(x) or 'abdominale' in str(x) else False)

    df['shortness_of_breath'] = df['simptome declarate'].apply(lambda x: True if 'dispnee' in str(x) else False)
    return df


def clean_declared_symptoms_hospitalization(df):
    # simptome raportate la internare -> just the important ones, a merge with the ones from above should be done

    df['simptome raportate la internare'] = df['simptome raportate la internare'].fillna('X')
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.strip()
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.replace(
        r'.*(ASIMPTOMATICA|ASIMPTOMATICĂ|Asimptomatica|ASIMPTOMATIC|Asimptomatic|asimptomatic|asimptomatica).*', 'X')
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.replace(r'(-|nu are)', 'X')
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.lower()

    df['fever_internare'] = df['simptome raportate la internare'].apply(
        lambda x: True if 'febra' in str(x) or 'subfebrilitati' in str(x) else False)

    df['cough_internare'] = df['simptome raportate la internare'].apply(
        lambda x: True if 'tuse' in str(x) or 'tuse seaca' in str(x) else False)

    df['muscle_soreness_internare'] = df['simptome raportate la internare'].apply(
        lambda x: True if 'musculare' in str(x) or 'abdominale' in str(x) else False)

    df['shortness_of_breath'] = df['simptome raportate la internare'].apply(
        lambda x: True if 'dispnee' in str(x) else False)

    return df


def clean_diagnostic(df):
    # diagnostic și semne de internare -> df[diagnostic]

    df['diagnostic și semne de internare'] = df['diagnostic și semne de internare'].fillna('X')
    df['diagnostic și semne de internare'] = df['diagnostic și semne de internare'].str.strip()
    df['diagnostic și semne de internare'] = df['diagnostic și semne de internare'].str.replace(
        r'.*(ASIMPTOMATICA|ASIMPTOMATICĂ|Asimptomatica|ASIMPTOMATIC|Asimptomatic|asimptomatic|asimptomatica).*',
        'X')

    df['diagnostic și semne de internare'] = df['diagnostic și semne de internare'].str.replace(r'(-|nu are)', 'X')
    df['diagnostic și semne de internare'] = df['diagnostic și semne de internare'].str.lower()

    df['diagnostic și semne de internare'] = df['diagnostic și semne de internare'].str.replace(
        r'.*(afebril|fara).*',
        'x')

    df['diagnostic'] = df['diagnostic și semne de internare'].apply(
        lambda x: True if 'confirmata' in str(x) or 'confirma' in str(x) or 'suspiciune' in str(x) or 'suspect' in str(
            x) else False)

    return df


def drop_irrelevant_columns_symptoms(df):
    df = df.drop('simptome declarate', 1)
    df = df.drop('simptome raportate la internare', 1)
    df = df.drop('diagnostic și semne de internare', 1)

    return df


def clean_travel_history(df):
    df['istoric de călătorie'] = df['istoric de călătorie'].fillna('none')
    df["istoric de călătorie"] = df["istoric de călătorie"].str.strip()
    df["istoric de călătorie"] = df["istoric de călătorie"].str.lower()
    df['istoric de călătorie'] = df['istoric de călătorie'].str.replace(
        r'(asimptomatic|ne|nu|nu e cazul|neaga|neagă|nu a calatorit|nu  este cazul|nu are|fara|0|mu|durere).*', 'none')
    df['travel_history'] = df['istoric de călătorie'].apply(lambda x: False if 'none' in str(x) else True)

    return df


def clean_transportation(df):
    df['mijloace de transport folosite'] = df['mijloace de transport folosite'].fillna('xx')
    df["mijloace de transport folosite"] = df["mijloace de transport folosite"].str.strip()
    df["mijloace de transport folosite"] = df["mijloace de transport folosite"].str.lower()
    df['mijloace de transport folosite'] = df['mijloace de transport folosite'].str.replace(r'^nu.*', 'xx')
    df['mijloace de transport folosite'] = df['mijloace de transport folosite'].str.replace(
        r'^(o|0|fara|masina personala|masina|afebril, neo vezical)$', 'xx')

    df['transportation_history'] = df['mijloace de transport folosite'].apply(
        lambda x: False if 'xx' in str(x) else True)
    return df


def clean_contacted_someone_infected(df):
    df['confirmare contact cu o persoană infectată'] = df['confirmare contact cu o persoană infectată'].fillna('xx')
    df["confirmare contact cu o persoană infectată"] = df["confirmare contact cu o persoană infectată"].str.strip()
    df["confirmare contact cu o persoană infectată"] = df["confirmare contact cu o persoană infectată"].str.lower()
    df['confirmare contact cu o persoană infectată'] = df['confirmare contact cu o persoană infectată'].str.replace(
        r'^nu.*', 'xx')
    df['confirmare contact cu o persoană infectată'] = df['confirmare contact cu o persoană infectată'].str.replace(
        r'^(-|o|0|fara|venita din lombardia|nou nascut din mama hiv pozitiva)$', 'xx')

    df['confirmare_contact'] = df['confirmare contact cu o persoană infectată'].apply(
        lambda x: False if 'xx' in str(x) else True)

    return df


def clean_test_result(df):
    df1 = pd.DataFrame(df)

    df1['rezultat testare'] = df1['rezultat testare'].fillna('NECONCLUDENT')
    df1['rezultat testare'] = df1['rezultat testare'].replace(['NEGATIB'], 'NEGATIV')
    df1['rezultat testare'] = df1['rezultat testare'].replace(['NECONCLUDENT'], 'NEGATIV')
    return df1

#
# if __name__ == '__main__':
#     # get the data frame from the Excel file
#     data = data_processor.read_file(sys.argv[1])
#
#     # get number of columns from data frame
#     nr_cols = len(data.axes[1])
#
#     # select all columns from the data frame
#     columns = data.select_dtypes(include=[np.object]).columns
#
#     # diagnostic și semne de internare -> TODO
#
#     data = clean_features_training(data)
#     data.to_excel('./data/cleaned_dataset.xlsx')
