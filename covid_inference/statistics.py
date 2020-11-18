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
