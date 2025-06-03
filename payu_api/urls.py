from django.urls import path
from payu_api.views import PayUCreateOrderAPIView

urlpatterns = [
    path("payu/create/", PayUCreateOrderAPIView.as_view(), name="payu-create"),
]
