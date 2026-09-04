from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from locations.models import Category, Location
from locations.permissions import IsAuthorOrAdmin
from locations.serializers import CategorySerializer, LocationSerializer


class CategoryViewSet(ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


class LocationViewSet(ModelViewSet):
	queryset = Location.objects.select_related('category', 'author').all()
	serializer_class = LocationSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

	def perform_create(self, serializer) -> None:
		serializer.save(author=self.request.user)
