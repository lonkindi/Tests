import unittest
import api_app
import requests
from io import StringIO
from unittest.mock import patch

class TestAPI(unittest.TestCase):

    def test_ya_api(self):
        output = api_app.translate_it('Hi!').json()
        self.assertEqual(output['text'][0], 'Привет!')
        self.assertEqual(output['code'], 200)

    # def test_wrong_args(self):
    #     self.assertRaises(TypeError, api_app.translate_it())
        # self.assertRaises(TypeError, api_app.translate_it('A', 'B'))
        # self.assertRaises(TypeError, api_app.translate_it('A', 'B', 'C', 'D'))
        # self.assertRaises(TypeError, api_app.translate_it('#'))

    def test_connection(self):
        r_code = api_app.translate_it('Hi!', 'API_KEY', api_app.URL).status_code
        self.assertEqual(r_code, 403)
        # r_code = api_app.translate_it('Hi!', api_app.API_KEY, 'URL')
        # print('r_code=', r_code)
        r_err = requests.exceptions.MissingSchema
        self.assertRaises(requests.exceptions.MissingSchema, api_app.translate_it('Hi!', api_app.API_KEY, 'URL'))





