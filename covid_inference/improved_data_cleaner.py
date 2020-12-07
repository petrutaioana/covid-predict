import sys
import data_processor
import numpy as np


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

    df['vârstă'] = df['vârstă'].astype(float).astype(int)

    index_names = df[df['vârstă'] > 100].index
    df.drop(index_names, inplace=True)

    return df


def clean_test_result(df):
    df['rezultat testare'] = df['rezultat testare'].fillna('NECONCLUDENT')
    df['rezultat testare'] = df['rezultat testare'].replace(['NEGATIB'], 'NEGATIV')
    return df


def clean_sex(df):
    df['sex'] = df['sex'].str.replace(r'^(M|m).*$', 'M')
    df['sex'] = df['sex'].str.replace(r'^(F|f).*$', 'F')

    # cleanup_nums = {"sex":{"M": 0, "F": 1}}
    # df = df.replace(cleanup_nums)

    df = df.dropna(subset=['sex'])  # we lost only 2 rows so it's cool
    # print(df['sex'])
    # print(len(df) - df['sex'].count()) -> we lost only 2 rows
    return df


# TODO choose best method for cleaning declared symptoms
def clean_declared_symptoms(df):
    # simptome declarate -> just the important ones df['fever'], df['cough'], df['diarrhea'], df['muscle_soreness']
    # print(df["simptome declarate"].value_counts())
    df['simptome declarate'] = df['simptome declarate'].fillna('X')
    df["simptome declarate"] = df["simptome declarate"].str.strip()
    df['simptome declarate'] = df['simptome declarate'].str.replace(
        r'.*(ASIMPTOMATICA|ASIMPTOMATICĂ|Asimptomatica|ASIMPTOMATIC|Asimptomatic|asimptomatic|asimptomatica).*', 'X')
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'(-|nu are)', 'X')
    df['simptome declarate'] = df['simptome declarate'].str.lower()
    # print(df["simptome declarate"].unique())

    df['fever'] = df['simptome declarate'].apply(lambda x: True if 'febra' in str(x) else False)
    df['cough'] = df['simptome declarate'].apply(lambda x: True if 'tuse' in str(x) else False)
    df['diarrhea'] = df['simptome declarate'].apply(lambda x: True if 'diaree' in str(x) else False)
    df['muscle_soreness'] = df['simptome declarate'].apply(lambda x: True if 'musculare' in str(x) else False)
    return df


def clean_symptoms_column(data_frame):
    i = 0
    asymptomatic = ["asimptomatica", "asimptomatic", "asimptomatică", "asimptomatic covid", "nu", "nu are", "-", ""]
    fever = ["febra", "subfebra", "subfebrilitati"]
    cough = ["tuse", "tuse seaca"]
    tiredness = ["fatigabilitate"]
    muscular_pain = ["dureri musculare", "dureri abdominale", "durere", "durere locala"]
    shortness_of_breath = ["dispnee", "dispnee marcata"]

    for elem in data_frame['simptome declarate']:
        if any(i in str(elem).lower() for i in asymptomatic):
            data_frame.loc[i, 'simptome declarate'] = "asymptomatic"
        elif any(i in str(elem).lower() for i in fever):
            data_frame.loc[i, 'simptome declarate'] = "fever"
        elif any(i in str(elem).lower() for i in cough):
            data_frame.loc[i, 'simptome declarate'] = "cough"
        elif any(i in str(elem).lower() for i in tiredness):
            data_frame.loc[i, 'simptome declarate'] = "tiredness"
        elif any(i in str(elem).lower() for i in muscular_pain):
            data_frame.loc[i, 'simptome declarate'] = "muscular_pain"
        elif any(i in str(elem).lower() for i in shortness_of_breath):
            data_frame.loc[i, 'simptome declarate'] = "shortness_of_breath"
        i += 1
    return data_frame


def drop_irrelevant_columns(df):
    # instituția sursă ? drop
    df = df.drop('instituția sursă', 1)
    # dată debut simptome declarate ? drop
    df = df.drop('dată debut simptome declarate', 1)
    # dată internare ? drop
    df = df.drop('dată internare', 1)
    # data rezultat testare ? drop
    df = df.drop('data rezultat testare', 1)
    return df


# TODO choose best method for cleaning transportation
def clean_transportation(df):
    df['mijloace de transport folosite'] = df['mijloace de transport folosite'].fillna('xx')
    df["mijloace de transport folosite"] = df["mijloace de transport folosite"].str.strip()
    df["mijloace de transport folosite"] = df["mijloace de transport folosite"].str.lower()
    df['mijloace de transport folosite'] = df['mijloace de transport folosite'].str.replace(r'^nu.*', 'xx')
    df['mijloace de transport folosite'] = df['mijloace de transport folosite'].str.replace(
        r'^(o|0|fara|masina personala|masina|afebril, neo vezical)$', 'xx')
    df['travel_history_2'] = df['mijloace de transport folosite'].apply(lambda x: False if 'xx' in str(x) else True)
    # print(df['travel_history_2'].value_counts())
    return df


def clean_transport_used_column(data_frame):
    i = 0
    no = ["nu", "neaga", "-", "fara", "0", "O"]
    yes = ["da", "masina", "tren", "autocar", "avion", "ambulanta"]

    for elem in data_frame['mijloace de transport folosite']:
        if any(i in str(elem).lower() for i in no):
            data_frame.loc[i, 'mijloace de transport folosite'] = "nu"
        elif any(i in str(elem).lower() for i in yes):
            data_frame.loc[i, 'mijloace de transport folosite'] = "da"
        i += 1
    return data_frame


def clean_travel_history(df):
    # print(df['istoric de călătorie'].unique())
    df['istoric de călătorie'] = df['istoric de călătorie'].fillna('none')
    df["istoric de călătorie"] = df["istoric de călătorie"].str.strip()
    df["istoric de călătorie"] = df["istoric de călătorie"].str.lower()
    df['istoric de călătorie'] = df['istoric de călătorie'].str.replace(
        r'(asimptomatic|ne|nu|nu e cazul|neaga|neagă|nu a calatorit|nu  este cazul|nu are|fara|0|mu|durere).*', 'none')
    df['travel_history'] = df['istoric de călătorie'].apply(lambda x: False if 'none' in str(x) else True)
    # print(df['travel_history'].value_counts())
    # print(df['istoric de călătorie'].value_counts())
    return df


def clean_declared_symptoms_hospitalization(df):
    # simptome raportate la internare -> just the important ones, a merge with the ones from above should be done
    # df['fever_internare'], df['cough_internare'], df['diarrhea_internare'], df['muscle_soreness_internare']
    df['simptome raportate la internare'] = df['simptome raportate la internare'].fillna('X')
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.strip()
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.replace(
        r'.*(ASIMPTOMATICA|ASIMPTOMATICĂ|Asimptomatica|ASIMPTOMATIC|Asimptomatic|asimptomatic|asimptomatica).*', 'X')
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.replace(r'(-|nu are)', 'X')
    df["simptome raportate la internare"] = df["simptome raportate la internare"].str.lower()

    df['fever_internare'] = df['simptome raportate la internare'].apply(lambda x: 1 if 'febra' in str(x) else 0)
    df['cough_internare'] = df['simptome raportate la internare'].apply(lambda x: 1 if 'tuse' in str(x) else 0)
    df['diarrhea_internare'] = df['simptome raportate la internare'].apply(lambda x: 1 if 'diaree' in str(x) else 0)
    df['muscle_soreness_internare'] = df['simptome raportate la internare'].apply(
        lambda x: 1 if 'musculare' in str(x) else 0)
    return df


# TODO choose best method for cleaning contacted someone infected column
def clean_contacted_someone_infected(df):
    df['confirmare contact cu o persoană infectată'] = df['confirmare contact cu o persoană infectată'].fillna('xx')
    df["confirmare contact cu o persoană infectată"] = df["confirmare contact cu o persoană infectată"].str.strip()
    df["confirmare contact cu o persoană infectată"] = df["confirmare contact cu o persoană infectată"].str.lower()
    df['confirmare contact cu o persoană infectată'] = df['confirmare contact cu o persoană infectată'].str.replace(
        r'^nu.*', 'xx')
    df['confirmare contact cu o persoană infectată'] = df['confirmare contact cu o persoană infectată'].str.replace(
        r'^(-|o|0|fara|venita din lombardia|nou nascut din mama hiv pozitiva)$', 'xx')
    # print(df['confirmare contact cu o persoană infectată'].value_counts())
    df['contact'] = df['confirmare contact cu o persoană infectată'].apply(
        lambda x: False if 'xx' in str(x) else True)
    # print(df['contact'].value_counts())
    return df


def clean_contact_with_infected_person_column(data_frame):
    i = 0
    no = ["nu", "neaga", "-", "fara", "0"]
    yes = ["da", "covid", "posibil", "focar", "pozitiv"]

    for elem in data_frame['confirmare contact cu o persoană infectată']:
        if any(i in str(elem).lower() for i in no):
            data_frame.loc[i, 'confirmare contact cu o persoană infectată'] = "nu"
        elif any(i in str(elem).lower() for i in yes):
            data_frame.loc[i, 'confirmare contact cu o persoană infectată'] = "da"
        i += 1
    return data_frame


def clean(df):
    df = drop_irrelevant_columns(df)
    df = clean_age(df)
    df = clean_test_result(df)
    df = clean_sex(df)
    df = clean_declared_symptoms(df)
    df = clean_transportation(df)
    df = clean_travel_history(df)
    df = clean_declared_symptoms_hospitalization(df)
    df = clean_contacted_someone_infected(df)
    return df


if __name__ == '__main__':
    # get the data frame from the Excel file
    data = data_processor.read_file(sys.argv[1])

    # get number of columns from data frame
    nr_cols = len(data.axes[1])

    # select all columns from the data frame
    columns = data.select_dtypes(include=[np.object]).columns

    # diagnostic și semne de internare -> TODO

    data = clean(data)
    data.to_excel('../data/cleaned_dataset.xlsx')
