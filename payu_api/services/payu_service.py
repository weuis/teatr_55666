import requests
from urllib.parse import urlencode
from django.conf import settings

def get_access_token():
    return "test_token_123"

def create_payment(order_id, amount, buyer_email, description):
    access_token = get_access_token()
    url = "https://httpbin.org/post"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "customerIp": "127.0.0.1",
        "merchantPosId": settings.PAYU_POS_ID,
        "description": description,
        "currencyCode": "PLN",
        "totalAmount": str(int(amount * 100)),
        "extOrderId": str(order_id),
        "buyer": {
            "email": buyer_email,
            "language": "pl"
        },
        "products": [
            {
                "name": description,
                "unitPrice": str(int(amount * 100)),
                "quantity": "1"
            }
        ]
    }

    print("Request URL:", url)
    print("Request headers:", headers)
    print("Request payload:", payload)

    response = requests.post(url, headers=headers, json=payload)
    print("PayU response text:", response.text)
    response.raise_for_status()
    return response.json()
