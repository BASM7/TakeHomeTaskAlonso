from django.test import TestCase
from collections import OrderedDict

import requests


class StripeManagerTestCase(TestCase):
    api_endpoint = 'http://localhost:8000/api/'

    def setUp(self):
        self.payload = OrderedDict()

    def test_valid_payment(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '2222'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'success')

    def test_expired_card(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '1'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '458'
        self.payload['amount_in_cents'] = '3333'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_missing_card_number(self):
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '4444'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_missing_card_expiry_month(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '5555'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_missing_card_expiry_year(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '6666'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_missing_card_cvv(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['amount_in_cents'] = '7777'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_missing_amount_in_cents(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_invalid_amount_in_cents(self):
        self.payload['card_number'] = '4242424242424242'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '-1'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')

    def test_invalid_card_number(self):
        self.payload['card_number'] = '1254789632145874'
        self.payload['card_expiry_month'] = '12'
        self.payload['card_expiry_year'] = '2022'
        self.payload['card_cvv'] = '123'
        self.payload['amount_in_cents'] = '8888'

        api_response = requests.post(self.api_endpoint, json=self.payload)
        self.assertEqual(api_response.json()['result'], 'failure')
