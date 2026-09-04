from django.test import SimpleTestCase
from rest_framework.test import APIClient


class HealthApiTests(SimpleTestCase):
    def test_health_endpoint(self) -> None:
        response = APIClient().get('/health/', HTTP_HOST='localhost')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
