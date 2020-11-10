import pandas as pd


def clean_for_training(df):
    cleaned_features = clean_features(df.getFeatures())
    df.setFeatures(
        features=cleaned_features
    )

    cleaned_results = clean_results(df.getResults())
    # Convert back to the type returned by <code>train_test_split</code>
    converted_cleaned_results = cleaned_results['rezultat testare'].convert_dtypes()
    df.setResults(
        results=converted_cleaned_results
    )

    return df


def clean_features(df):
    # Remove irrelevant columns
    df = df.drop('instituția sursă', 1)
    df = df.drop('dată debut simptome declarate', 1)
    df = df.drop('dată internare', 1)
    df = df.drop('diagnostic și semne de internare', 1)
    df = df.drop('istoric de călătorie', 1)
    df = df.drop('mijloace de transport folosite', 1)
    df = df.drop('confirmare contact cu o persoană infectată', 1)
    df = df.drop('data rezultat testare', 1)

    # Clean sex column
    df = df.dropna(subset=['sex'])
    df['sex'] = df['sex'].str.replace(r'^M.*$', 'MASCULIN')
    df['sex'] = df['sex'].str.replace(r'^m.*$', 'MASCULIN')
    df['sex'] = df['sex'].str.replace(r'^F.*$', 'FEMININ')
    df['sex'] = df['sex'].str.replace(r'^f.*$', 'FEMININ')

    df = df.dropna(subset=['simptome declarate', 'simptome raportate la internare'])

    # Replace all the "Asimptomatic" variants to "ASIMPTOMATIC"
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'^ASI.*$', 'ASIMPTOMATIC')
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'^asi.*$', 'ASIMPTOMATIC')
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'^Asi.*$', 'ASIMPTOMATIC')
    df['simptome raportate la internare'] = df['simptome raportate la internare'].str.replace(r'^ASI.*$',
                                                                                              'ASIMPTOMATIC')
    df['simptome raportate la internare'] = df['simptome raportate la internare'].str.replace(r'^asi.*$',
                                                                                              'ASIMPTOMATIC')
    df['simptome raportate la internare'] = df['simptome raportate la internare'].str.replace(r'^Asi.*$',
                                                                                              'ASIMPTOMATIC')

    # Remove all number values
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'\d+\,\d+', '')
    df['simptome declarate'] = df['simptome declarate'].str.replace(r'\d+\.\d+', '')
    df['simptome raportate la internare'] = df['simptome raportate la internare'].str.replace(r'\d+\,\d+', '')
    df['simptome raportate la internare'] = df['simptome raportate la internare'].str.replace(r'\d+\.\d+', '')

    # Split the symptoms string by comma and remove heading white spaces
    df['simptome declarate'] = df['simptome declarate'].astype(str).apply(lambda x: x.lstrip(' ').split(','))
    df['simptome raportate la internare'] = df['simptome raportate la internare'].astype(str).apply(
        lambda x: x.lstrip(' ').split(','))

    # Save to a new file
    df.to_excel("./data/new_data_set.xlsx")

    return df


def clean_results(results):
    # Print unique result values: ['NEGATIV' 'NECONCLUDENT' nan 'POZITIV' 'NEGATIB']

    df = pd.DataFrame(results)
    df['rezultat testare'] = df['rezultat testare'].replace(['NEGATIB'], 'NEGATIV')

    # Remove items without a conclusive result
    df = df.dropna(subset=['rezultat testare'])
    df = df.drop(df[(df['rezultat testare'] == 'NECONCLUDENT')].index)

    return df


"""
Functions used for generating data reports
"""


def compute_unique_values_number(data_frame):
    print(data_frame.nunique())


def compute_unique_values_percentage(data_frame):
    counts = data_frame.nunique()
    (rows, cols) = data_frame.shape

    print('[Nume coloana] [Valori unice in obs] [Procent raportat la nr. linii]\n')
    for i in range(cols):
        percentage = float(counts[i]) / rows * 100
        if percentage < 1:
            print('%s: %d, %.1f%%' % (counts.index[i], counts[i], percentage))
