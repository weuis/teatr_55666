import requests
from django.conf import settings

def get_access_token():
    url = f"{settings.PAYU_API_URL}/pl/standard/user/oauth/authorize"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.PAYU_CLIENT_ID,
        "client_secret": settings.PAYU_CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def create_payment(order_id, amount, buyer_email, description):
    access_token = get_access_token()
    url = f"{settings.PAYU_API_URL}/api/v2_1/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "notifyUrl": "https://yourdomain.com/api/payments/notify/",
        "customerIp": "127.0.0.1",
        "merchantPosId": settings.PAYU_POS_ID,
        "description": description,
        "currencyCode": "PLN",
        "totalAmount": str(int(amount * 100)),
        "extOrderId": order_id,
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

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
