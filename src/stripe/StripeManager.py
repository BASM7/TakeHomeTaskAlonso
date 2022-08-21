import requests
from api.models import StripeLog
from api.utils import mask_card_number, mask_card_cvv


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
        self.stripe_response = None
        self.validation_errors = []

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

    def request_is_valid(self):
        required_fields = ['card_number', 'card_expiry_month', 'card_expiry_year', 'card_cvv', 'amount_in_cents']
        for field in required_fields:
            if field not in self.request_data:
                self.validation_errors.append('{} is a required field'.format(field))

        if len(self.validation_errors) > 0:
            return False
        return True

    def tokenize_card(self):
        """ Tokenize the card details. """
        card_info_payload = dict()
        card_info_payload['card[number]'] = self.request_data['card_number']
        card_info_payload['card[exp_month]'] = self.request_data['card_expiry_month']
        card_info_payload['card[exp_year]'] = self.request_data['card_expiry_year']
        card_info_payload['card[cvc]'] = self.request_data['card_cvv']

        card_token_endpoint = 'https://api.stripe.com/v1/tokens'
        self.stripe_response = self.execute_stripe_request(card_token_endpoint, card_info_payload)

        if self.stripe_response.status_code == 200:
            self.stripe_payload['payment_method_data[type]'] = self.payment_method
            self.stripe_payload['payment_method_data[card][token]'] = self.stripe_response.json()['id']
            self.stripe_payload['amount'] = self.request_data['amount_in_cents']
            self.stripe_payload['currency'] = self.currency
            return True
        return False

    def confirm_payload(self):
        self.stripe_payload['confirm'] = True

    def process_payment(self):
        if not self.request_is_valid():
            return {
                'result': 'failure',
                'transaction_id': '',
                'errors': ','.join(self.validation_errors)
            }
        if self.tokenize_card():
            self.confirm_payload()
            self.stripe_response = self.execute_stripe_request(self.stripe_api_endpoint, self.stripe_payload)
            if self.stripe_response.status_code == 200:
                return self.parse_response('success', self.stripe_response.json()['id'])
            else:
                return self.parse_response('failure')
        else:
            return self.parse_response('failure')

    def parse_response(self, result, transaction_id=''):
        message = 'Payment successful' if result == 'success' else self.stripe_response.json()['error']['message']
        return {
            'result': result,
            'transaction_id': transaction_id,
            'message': message
        }

    def execute_stripe_request(self, endpoint, payload):
        request_response = requests.post(
            endpoint,
            params=payload,
            headers=self.get_headers())

        if 'card[number]' in payload:
            payload['card[number]'] = mask_card_number(payload['card[number]'])
        if 'card[cvc]' in payload:
            payload['card[cvc]'] = mask_card_cvv(payload['card[cvc]'])
        StripeLog.objects.create(data=payload, log_type='request')
        StripeLog.objects.create(data=request_response.json(), log_type='response')
        return request_response

