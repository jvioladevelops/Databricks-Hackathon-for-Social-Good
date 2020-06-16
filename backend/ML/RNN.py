import os
import numpy as np
from tensorflow import keras
from werkzeug.exceptions import abort

from backend.ML.utils import load_data, preprocess, filter_by_country, \
    separate, normalize, apply_lookback, reshape, unite_dates_samples, \
    denormalize, append_sample, change_date, get_sample


class RNN:
    def __init__(self, country_code, look_forward=3):
        """
        """
        if not country_code:
            abort(422)

        self.look_back = look_forward
        self.look_forward = look_forward + 1
        self.country_code = country_code
        self.models_src = f'{os.path.dirname(__file__)}/models'
        self.model = keras.models.load_model(
            f'{self.models_src}/{self.country_code}-RNN.h5')

    def predict(self, requested_day):
        """
            Make predictions starting at the requested date
                for the next look_froward number of days.

                look_forward is look_back + 1, since the predictions are made
                for the requested day too.

                If the requested date is ahead of the last available date,
                the last available date will be taken as the starting date.

            :param      requested_day:  str
            :return     predicted:      int
                        message:        str
        """

        df = load_data()

        # preprocess
        df = preprocess(df)
        df = filter_by_country(df, self.country_code)

        # separate cases from data
        dates, Y = separate(df)

        # normalize Y
        Y = normalize(Y)

        # apply look_back and generate needed samples
        X, _ = apply_lookback(Y, look_back=self.look_back)

        # reshape to fit the model
        X = reshape(X)
        dates = reshape(dates)
        dates = dates[self.look_back:]

        # unite samples (X) with dates
        # a date of a sample corresponds to the future prediction value (Y)
        united_samples = unite_dates_samples(dates.reshape(-1, 1),
                                             X.reshape(-1, self.look_back))

        last_day = requested_day
        predicted = 0

        for step in range(self.look_forward):
            sample, last_day = get_sample(united_samples, last_day)
            sample = sample.reshape(1, 1, self.look_back)

            predicted = self.model.predict(sample.astype(np.float32))

            united_samples, last_day = append_sample(united_samples, predicted,
                                                     self.look_back,
                                                     last_day)

        # date of the prediction
        last_day = change_date(last_day, delta_days=-1)

        # chosen starting date
        start_avail_day = change_date(last_day,
                                      delta_days=-self.look_back)

        # convert to a real number of COVID-19 cases
        predicted = denormalize(predicted)[0, 0]
        predicted = int(predicted)

        prediction_info = {
            'prediction_date': last_day,
            'starting_date': start_avail_day,
            'prediction_new_cases': predicted
        }

        return prediction_info, united_samples


