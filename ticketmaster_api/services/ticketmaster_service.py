import requests
from django.conf import settings

BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'

def get_events_by_city(city: str, size: int = 10):
    params = {
        'apikey': settings.TICKETMASTER_API_KEY,
        'city': city,
        'size': size,
        'locale': '*',
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        events = data.get('_embedded', {}).get('events', [])
        return events
    except requests.RequestException:
        return []
