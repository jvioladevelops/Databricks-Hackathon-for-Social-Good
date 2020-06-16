import unittest

from flask import json

from backend.app import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_post_survey(self):
        # bad request call
        res = self.client().post('/survey')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['name'], 'Bad Request')

        # successful call
        request_data = json.dumps({
              "country_region_code": "US",
              "look_forward_days": 3,
              "starting_day": "2020-05-01"
        })

        res = self.client().post('/survey', data=request_data)
        data = json.loads(res.data)

        self.assertEqual(data['prediction'], str(26489))
        # self.assertEqual(data['message'], '')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == '__main__':
    unittest.main()
