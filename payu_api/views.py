# payu_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payu_api.services.payu_service import create_payment

class PayUCreateOrderAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            order = create_payment(
                order_id=data["order_id"],
                amount=float(data["amount"]),
                buyer_email=data["email"],
                description=data["description"]
            )
            return Response(order, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
