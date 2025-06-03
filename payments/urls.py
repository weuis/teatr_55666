from django.urls import path
from payments.views import PayUCreateOrderAPIView

urlpatterns = [
    path("payu/create/", PayUCreateOrderAPIView.as_view(), name="payu-create"),
]
