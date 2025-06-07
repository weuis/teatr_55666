from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch


class PayUCreateOrderAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('payu-create')
        self.valid_payload = {
            "order_id": "123ABC",
            "amount": "99.99",
            "email": "buyer@example.com",
            "description": "Test order"
        }

    @patch('payu_api.views.create_payment')
    def test_create_order_success(self, mock_create_payment):
        mock_create_payment.return_value = {
            "status": "SUCCESS",
            "redirectUri": "https://payment-gateway.com/pay"
        }

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("redirectUri", response.data)
        mock_create_payment.assert_called_once_with(
            order_id="123ABC",
            amount=99.99,
            buyer_email="buyer@example.com",
            description="Test order"
        )

    @patch('payu_api.views.create_payment')
    def test_create_order_failure(self, mock_create_payment):
        mock_create_payment.side_effect = Exception("PayU error")

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

