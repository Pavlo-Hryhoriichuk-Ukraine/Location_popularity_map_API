from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from locations.models import Category, Location
from reviews.models import Review


class ReviewApiTests(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = User.objects.create_user(username='reviewer', password='strong-password')
		category = Category.objects.create(name='Museums')
		self.location = Location.objects.create(
			name='City Museum',
			description='A museum',
			category=category,
			address='2 Main Street',
			latitude='50.450000',
			longitude='30.523000',
			author=self.user,
		)

	def test_authenticated_user_can_create_one_review(self) -> None:
		self.assertTrue(self.client.login(username='reviewer', password='strong-password'))
		response = self.client.post(
			'/api/reviews/',
			{'location': self.location.pk, 'rating': 5, 'comment': 'Excellent'},
			format='json',
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(Review.objects.count(), 1)
