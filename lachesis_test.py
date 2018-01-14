from http import HTTPStatus
import json
import unittest

import lachesis


class LachesisTest(unittest.TestCase):

    def setUp(self):
        lachesis.app.testing = True
        self.c = lachesis.app.test_client()
        with lachesis.app.app_context():
            lachesis.clear_db()
            lachesis.init_db()
        self.good_observation = {
            "id": 1,
            "observation": {
                "birth date": "1983-12-26",
                "job type": "private",
                "school level": "secondary",
                "domestic status": "single",
                "profession": "mechanic",
                "domestic relationship type": "never married",
                "ethnicity": "afro american",
                "gender": "Female",
                "earned dividends": 0,
                "interest earned": 0,
                "monthly work": 160,
                "country of origin": "u.s."
            }
        }

    def _public_api_request(self, method, url, *args, **kwargs):
        """
        Perform an API request.
        :param method: Method to use ('GET', 'POST' etc).
        :param url: Relative URL.
        """
        kwargs.setdefault('headers', {})
        kwargs['method'] = method
        res = self.c.open(url, *args, **kwargs)
        return res

    def _public_api_json_request(self, method, url, data, *args, **kwargs):
        """
        Perform an HTTP request with a JSON body payload.
        :param method: Method to use ('POST', 'PUT' etc).
        :param url: Relative URL.
        :param data: Dictionary containing data to send.
        """
        res = self._public_api_request(
            method,
            url,
            data=json.dumps(data),
            content_type='application/json',
            *args,
            **kwargs
        )
        return res

    def test_predict_health(self):
        r = self._public_api_json_request('POST', '/predict', self.good_observation)
        self.assertEqual(HTTPStatus.OK, r.status_code)

    def test_predict_sanity(self):
        r = self._public_api_json_request('POST', '/predict', self.good_observation)
        self.assertTrue(
            json.loads(r.data)['prediction'] >= 0
        )
        self.assertTrue(
            json.loads(r.data)['prediction'] <= 1.0
        )

    def test_predict_duplicate(self):
        r = self._public_api_json_request('POST', '/predict', self.good_observation)
        self.assertEqual(HTTPStatus.OK, r.status_code)
        r = self._public_api_json_request('POST', '/predict', self.good_observation)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    def test_predict_missing_id(self):
        r = self._public_api_json_request(
            'POST',
            '/predict',
            {'observation': {'meh': 'hah!'}}
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    def test_predict_missing_observation(self):
        r = self._public_api_json_request(
            'POST',
            '/predict',
            {'id': 2345}
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

if __name__ == '__main__':
    unittest.main()
