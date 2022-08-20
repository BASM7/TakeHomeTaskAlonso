from django.test import TestCase
from collections import OrderedDict

import requests


class StripeManagerTestCase(TestCase):
    api_endpoint = 'http://localhost:8000/api/'

    def setUp(self) -> None:
        self.payload = OrderedDict()

    def _fill_payload(self):
        pass

    def test_valid_payment(self):
        self._fill_payload()

        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '2222'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        print('API RESPONSE: {}'.format(api_response.json()))
        self.assertEqual(api_response.json()['result'], 'success')


