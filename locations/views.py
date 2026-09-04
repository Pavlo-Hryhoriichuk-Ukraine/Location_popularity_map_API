from rest_framework.permissions import IsAuthenticatedOrReadOnly
from datetime import timedelta

from django.core.cache import cache
from django.db.models import Avg, Count, F, Q, Value
from django.db.models.functions import Coalesce, Least
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from locations.models import Category, Location, LocationViewEvent
from locations.cache import LOCATION_LIST_TIMEOUT, get_location_list_cache_key, invalidate_location_list_cache
from locations.filters import LocationFilter
from locations.permissions import IsAuthorOrAdmin
from locations.serializers import CategorySerializer, LocationSerializer


class CategoryViewSet(ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer) -> None:
		serializer.save()
		invalidate_location_list_cache()

	def perform_update(self, serializer) -> None:
		serializer.save()
		invalidate_location_list_cache()

	def perform_destroy(self, instance) -> None:
		instance.delete()
		invalidate_location_list_cache()


class LocationViewSet(ModelViewSet):
	queryset = Location.objects.select_related('category', 'author').all()
	serializer_class = LocationSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
	filterset_class = LocationFilter
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	search_fields = ['name', 'description']
	ordering_fields = ['created_at', 'name', 'average_rating', 'popularity_score']
	ordering = ['-created_at']

	def get_queryset(self):
		seven_days_ago = timezone.now() - timedelta(days=7)
		return Location.objects.select_related('category', 'author').annotate(
			average_rating=Coalesce(Avg('reviews__rating'), Value(0.0)),
			review_count=Count('reviews', distinct=True),
			recent_view_count=Count(
				'view_events',
				filter=Q(view_events__created_at__gte=seven_days_ago),
				distinct=True,
			),
		).annotate(
			popularity_score=(
				(F('average_rating') / Value(5.0) * Value(0.5))
				+ (Least(F('review_count'), Value(10)) / Value(10.0) * Value(0.3))
				+ (Least(F('recent_view_count'), Value(20)) / Value(20.0) * Value(0.2))
			)
		)

	def list(self, request: Request, *args, **kwargs) -> Response:
		cache_key = get_location_list_cache_key(request.query_params.urlencode())
		cached_data = cache.get(cache_key)
		if cached_data is not None:
			return Response(cached_data)

		response = super().list(request, *args, **kwargs)
		cache.set(cache_key, response.data, timeout=LOCATION_LIST_TIMEOUT)
		return response

	def retrieve(self, request, *args, **kwargs) -> Response:
		location = self.get_object()
		if request.user.is_authenticated:
			cache_key = f'location-view:{location.pk}:user:{request.user.pk}'
			if cache.add(cache_key, True, timeout=60 * 60):
				LocationViewEvent.objects.create(location=location, user=request.user)
		serializer = self.get_serializer(location)
		return Response(serializer.data)

	def perform_create(self, serializer) -> None:
		serializer.save(author=self.request.user)
		invalidate_location_list_cache()

	def perform_update(self, serializer) -> None:
		serializer.save()
		invalidate_location_list_cache()

	def perform_destroy(self, instance) -> None:
		instance.delete()
		invalidate_location_list_cache()
