from django.urls import path
from rest_framework.routers import DefaultRouter

from locations.exports import export_locations_csv, export_locations_json
from locations.views import CategoryViewSet, LocationViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('locations', LocationViewSet, basename='location')

urlpatterns = [
	path('locations/export/json/', export_locations_json, name='locations-export-json'),
	path('locations/export/csv/', export_locations_csv, name='locations-export-csv'),
	*router.urls,
]
