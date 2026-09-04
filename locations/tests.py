from typing import Any, cast

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from locations.models import Category


class LocationApiTests(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = User.objects.create_user(username='owner', password='strong-password')
		self.category = Category.objects.create(name='Parks')

	def test_anonymous_user_can_list_locations(self) -> None:
		response = self.client.get('/api/locations/')

		self.assertEqual(response.status_code, 200)

	def test_authenticated_user_can_create_location(self) -> None:
		cast(Any, self.client).force_authenticate(self.user)
		response = self.client.post(
			'/api/locations/',
			{
				'name': 'Central Park',
				'description': 'A city park',
				'category': self.category.pk,
				'address': '1 Main Street',
				'latitude': '50.450000',
				'longitude': '30.523000',
			},
			format='json',
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(cast(Any, response).data['author'], self.user.pk)
