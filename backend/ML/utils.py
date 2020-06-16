import os
from datetime import datetime as dt, timedelta

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

COLNAMES = ['ISO_2_CODE', 'ADM0_NAME', 'date_epicrv',
            'NewCase', 'CumCase', 'NewDeath',
            'CumDeath']
NEW_COLUMN_NAMES = ['country_region_code', 'country_region', 'date',
                    'new_cases', 'cum_cases', 'new_deaths', 'cum_deaths']
DATASET_DIR = f'{os.path.dirname(__file__)}/../datasets'
FILENAME = 'who_cases_deaths.csv'
DATE_FORMAT = '%Y-%m-%d'

np.random.seed(7)
SCALER = MinMaxScaler(feature_range=(0, 1))


def load_data():
    """
        Load a dataframe from a CSV file.
        Loaded with selected columns.
        TODO (second priority): switch database or cloud

        :return:    dataframe: pandas.core.frame.DataFrame
    """
    return pd.read_csv(f'{DATASET_DIR}/{FILENAME}', usecols=COLNAMES)


def preprocess(dataframe):
    """
        Preprocess the dataset to contain formatted date;
            renamed columns for better integrity among other services, data
            storages and scripts;

            trimmed dataframe to work only with country, its new cases of
            COVID-19 with respect to dates.

        :param      dataframe: pandas.core.frame.DataFrame
        :return:    dataframe: pandas.core.frame.DataFrame
    """

    # rename column names
    mapped_columns = dict(zip(COLNAMES, NEW_COLUMN_NAMES))
    dataframe = dataframe.rename(columns=mapped_columns)

    # format date
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    dataframe['date'] = dataframe['date'].dt.strftime(DATE_FORMAT)

    # select used columns
    dataframe = dataframe[['country_region_code', 'date', 'new_cases']]

    return dataframe


def filter_by_country(dataframe, country_code):
    """
        Selects record only for specified country.

        Trims the dataset to contain new COVID-19 cases with respect to dates.
            Country code is no longer used in the data frame.

        :param      dataframe:      pandas.core.frame.DataFrame
        :param      country_code:   str
        :return:    filtered_df:    pandas.core.frame.DataFrame
    """
    filtered_df = dataframe[
        dataframe['country_region_code'] == country_code][
        ['date', 'new_cases']]
    return filtered_df


def separate(dataframe):
    """
        Separate dates from values of new cases of COVID-19.


        :param  dataframe:      pandas.core.frame.DataFrame
        :return:dates:          numpy.ndarray
                values:         numpy.ndarray

                dates.shape:    (N, 1)
                values.shape:   (N, 1)
    """

    dates = dataframe['date'].values.reshape(-1, 1)

    dataframe['new_cases'] = dataframe['new_cases'].astype('float32')
    values = dataframe['new_cases'].values.reshape(-1, 1)

    return dates, values


def normalize(y):
    """
        Normalize the values to be in range 0..1

        Shapes should remain identical: (N, 1)

        :param      y:  numpy.ndarray
        :return:        numpy.ndarray
    """

    return SCALER.fit_transform(y)


def denormalize(sample):
    """
        Denormalize the values to be actual number of COVID-19 cases.

        Shapes should remain identical: (1, 1)

        :param      sample: numpy.ndarray
        :return:            numpy.ndarray
    """

    return SCALER.inverse_transform(sample)


def apply_lookback(dataset, look_back=1):
    """
        Creates 2 datasets.
            X contains look_back number of columns. I.e., if look_back is 3,

            X would contain 3 columns.
            Y would contain 1 column.

            Each sample (row) is a sequence of look_back number of COVID-19
            cases for look_back time steps.
            X:  | x(t-2) | x(t-1) | x(t) |

            Y:  |x(t+1)|
            Y contains real values at t+1.

        Shapes: N is the length.
            N in dataset has lookback more number of samples more than X and Y.

            dataset.shape   is (N, 1)
            X.shape         is (N-look_back, 1)
            Y.shape         is (N-look_back, )

        :param      dataset:    numpy.ndarray
        :param      look_back:  int
        :return:                numpy.ndarray, numpy.ndarray
    """

    data_x, data_y = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        data_x.append(a)
        data_y.append(dataset[i + look_back, 0])

    return np.array(data_x), np.array(data_y)


def reshape(x):
    """
        Reshape to fit a recurrent neural network's input shape.

        :param      x:                  numpy.ndarray
                    x.shape:            (N, look_back)

        :return     reshaped:           numpy.ndarray
                    reshaped.shape:     (N, 1, look_back)
    """
    reshaped = np.reshape(x, (x.shape[0], 1, x.shape[1]))

    return reshaped


def unite_dates_samples(dates, samples):
    """
        Horizontally unites dates for x(t+1)
            and samples for | x(t-k) | ... | x(t) |,
            where k is look_back-1.

        Shapes:     dates:      (N, 1)
                    samples:    (N, look_back)
                    hstacked:   (N, 1 + look_back)

        :param      dates:      numpy.ndarray
        :param      samples:    numpy.ndarray
        :return    hstacked:   numpy.ndarray
    """

    hstacked = np.hstack((dates, samples))

    return hstacked


def change_date(date, delta_days=0):
    """
        Gets a date in delta_days number of days.
            delta_days can be positive or negative.

        :param      date:           datetime.datetim
        :param      delta_days:     int
        :return     next_date:      str
    """

    detla = timedelta(days=delta_days)

    date = dt.strptime(date, DATE_FORMAT)

    next_date = date + detla
    next_date = dt.strftime(next_date, DATE_FORMAT)

    return next_date


def append_sample(array, predicted, look_back, requested_day):
    """
        Appends a predicted number of COVID-19 cases to the end of all samples;
            Creates the next date for t+1.

            Generate a new sample as  | x(t-k) | ... | x(t) |
            where   k is look_back-1
            and     x(t) is the predicted value.


        :param      array:              numpy.ndarray
                    array.shape:        (N, 4)
        :param      predicted:          numpy.ndarray
                    predicted.shape:    (1, 1)

        :param      look_back:          int
        :param      requested_day:      str

        :return:    numpy.ndarray,      str
    """

    # next date
    next_date_formatted = change_date(requested_day, delta_days=1)
    next_date_formatted = np.array([next_date_formatted])

    # generate next sample
    selected = array[array[:, 0] == requested_day, 2:].reshape(look_back - 1, )
    selected = np.append(selected, predicted.reshape(1, ))
    next_sample = np.append(next_date_formatted, selected)

    # append next sample
    if len(array[array[:, 0] == next_date_formatted, :]) == 0:
        array = np.vstack((array, next_sample))
    else:
        array[array[:, 0] == next_date_formatted] = next_sample

    return array, next_date_formatted[0]


def get_sample(united_samples, requested_date):
    """
        Extracts a sample for a prediction for a given date.
            If no such date is found, extract the last available sample.

            If it is available, extract the sample for this date

    :param      united_samples:         numpy.ndarray
                united_samples.shape:   (N, 1 + look_back)
    :param      requested_date:         str

    :return     sample:                 numpy.ndarray
                sample.shape:           (look_back, )
                day_taken:              str
    """
    search_res = np.where(united_samples[:, 0] == requested_date)[0]
    if len(search_res) == 0:
        sample = united_samples[-1:, :]
        day_taken = sample[0, 0]
    else:
        sample = united_samples[united_samples[:, 0] == requested_date]
        day_taken = requested_date

    sample = sample[0, 1:]  # eliminate date in the first column

    return sample, day_taken
