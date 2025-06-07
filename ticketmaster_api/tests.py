from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch

class TicketmasterEventsViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('ticketmaster-events')

    @patch('ticketmaster_api.views.get_events_by_city')
    def test_get_events_default_city(self, mock_get_events):
        mock_get_events.return_value = [
            {
                "name": "Event 1",
                "url": "https://example.com/event1",
                "dates": {"start": {"localDate": "2025-06-07"}},
                "images": [{"url": "https://example.com/image1.jpg"}],
                "_embedded": {"venues": [{"name": "Venue 1"}]}
            },
            {
                "name": "Event 2",
                "url": "https://example.com/event2",
                "dates": {"start": {"localDate": "2025-07-01"}},
                "images": [{"url": "https://example.com/image2.jpg"}],
                "_embedded": {"venues": [{"name": "Venue 2"}]}
            }
        ]

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn("url", response.data[0])
        self.assertIn("dates", response.data[0])
        self.assertIn("_embedded", response.data[0])
        mock_get_events.assert_called_once_with("Warsaw")

    @patch('ticketmaster_api.views.get_events_by_city')
    def test_get_events_with_custom_city(self, mock_get_events):
        mock_get_events.return_value = [
            {
                "name": "Berlin Concert",
                "url": "https://example.com/berlin",
                "dates": {"start": {"localDate": "2025-08-15"}},
                "images": [{"url": "https://example.com/berlin.jpg"}],
                "_embedded": {"venues": [{"name": "Berlin Hall"}]}
            }
        ]

        response = self.client.get(self.url, {'city': 'Berlin'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Berlin Concert")
        self.assertIn("url", response.data[0])
        mock_get_events.assert_called_once_with("Berlin")
