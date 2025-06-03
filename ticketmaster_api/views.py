from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ticketmaster_api.services.ticketmaster_service import get_events_by_city
from .serializers import TicketmasterEventSerializer

class TicketmasterEventsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city', 'Warsaw')
        events = get_events_by_city(city)
        serializer = TicketmasterEventSerializer(events, many=True)
        return Response(serializer.data)
