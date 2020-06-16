import os
import pandas as pd

from flask import Flask, request, abort, json, jsonify, render_template
from werkzeug.exceptions import HTTPException

from backend.ML.PolyReg import get_trend_pred
from backend.ML.RNN import RNN

from bokeh.client import pull_session
from bokeh.embed import server_session

template_dir = os.path.abspath('frontend/templates')
static_dir = os.path.abspath('frontend/static')


def create_app():
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    @app.route('/codes')
    def get_country_names_codes():
        """
            Loads a file to be served in JS in the frontend.

            Contains Access-Control-Allow-Origin, because otherwise
                requests are blocked by the frontend.

            :return: JSON
        """

        try:
            df = pd.read_csv('backend/datasets/countryCodesNames.txt')
        except Exception as e:
            abort(404)  # not found

        try:
            records = json.loads(df.to_json(orient='records'))
            response = {
                'results': records
            }

            response = jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
        except Exception as e:
            abort(422)  # unprocessable entity

        return response

    @app.route('/survey', methods=['POST'])
    def post_survey():
        """
            Captures user's request for a prediction with a date,
                a number of days to look forward
                and a country code.

            Returns a predicted number of new COVID-19 cases into the future,
                and its trend direction.

            :return: application/json
        """

        response_data = {}

        if len(request.form) == 0:
            abort(400)  # bad request

        data = request.form.to_dict()
        data['look_forward_days'] = int(data['look_forward_days'])

        try:
            rnn = RNN(country_code=data['country_region_code'],
                      look_forward=data['look_forward_days'])

            requested_day = data['requested_date']
            prediction_info, samples = rnn.predict(requested_day)
            trend = get_trend_pred(samples, data['look_forward_days'])

            response_data['prediction_new_cases'] = \
                str(prediction_info['prediction_new_cases'])
            response_data['prediction_date'] = \
                str(prediction_info['prediction_date'])
            response_data['starting_date'] = \
                str(prediction_info['starting_date'])

            response_data['country_region_code'] = data['country_region_code']
            response_data['trend'] = trend
            response_data['success'] = True

        except Exception as e:
            abort(422)  # unprocessable entity

        return jsonify(response_data)

    @app.route('/')
    # def present():
    #     return render_template("world.html")
    def dkapp_page():
        session = pull_session(url="https://coprevent-bokeh.herokuapp.com/main")
        script = server_session(None, session.id,
                                url='https://coprevent-bokeh.herokuapp.com/main')
        return render_template("world.html", script=script, template="Flask")

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()

        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)
