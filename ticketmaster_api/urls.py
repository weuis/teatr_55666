from django.urls import path
from .views import TicketmasterEventsView

urlpatterns = [
    path('events/', TicketmasterEventsView.as_view(), name='ticketmaster-events'),
]