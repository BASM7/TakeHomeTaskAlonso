import requests
from api.models import StripeLog


class StripeManager:
    """ StripeManager is a class that handles the Stripe API calls."""
    def __init__(self, request_data):
        self._secret_key = 'sk_test_51LR1cNLfbiNnohHKRYuDIG9aE1oKjj8KEaDNSnlhwgA97GFkNkFxMIH8o9Kc' \
                           '8lsGMiFCTijkVi4cA5RNzZsj3uLQ00Ztt9JFcM '
        self.request_data = request_data
        self.currency = 'usd'
        self.payment_method = 'card'
        self.stripe_api_endpoint = 'https://api.stripe.com/v1/payment_intents'
        self.stripe_payload = dict()

    def get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.secret_key),
            'Content-Type': 'application/json'
        }

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, secret_key):
        self._secret_key = secret_key

    def tokenize_card(self):
        """ Tokenize the card details. """
        card_info_payload = dict()
        card_info_payload['card[number]'] = self.request_data['card_number']
        card_info_payload['card[exp_month]'] = self.request_data['card_expiry_month']
        card_info_payload['card[exp_year]'] = self.request_data['card_expiry_year']
        card_info_payload['card[cvc]'] = self.request_data['card_cvv']

        card_token_endpoint = 'https://api.stripe.com/v1/tokens'
        card_token_response = requests.post(
            card_token_endpoint,
            headers=self.get_headers(),
            params=card_info_payload)

        if card_token_response.status_code == 200:
            self.stripe_payload['payment_method_data[type]'] = self.payment_method
            self.stripe_payload['payment_method_data[card][token]'] = card_token_response.json()['id']
            self.stripe_payload['amount'] = self.request_data['amount_in_cents']
            self.stripe_payload['currency'] = self.currency

    def confirm_payload(self):
        self.stripe_payload['confirm'] = True

    def process_payment(self):
        self.tokenize_card()
        self.confirm_payload()
        payment_response = self.execute_stripe_request(self.stripe_api_endpoint, self.stripe_payload)

        if payment_response.status_code == 200:
            return {
                'result': 'success',
                'transaction_id': payment_response.json()['id']
            }
        else:
            return {
                'result': 'failure',
                'transaction_id': '',
                'errors': payment_response.json()['error']['message']
            }

    def execute_stripe_request(self, endpoint, payload):
        StripeLog.objects.create(data=payload)
        request_response = requests.post(
            endpoint,
            params=payload,
            headers=self.get_headers())
        StripeLog.objects.create(data=request_response.json())
        return request_response

