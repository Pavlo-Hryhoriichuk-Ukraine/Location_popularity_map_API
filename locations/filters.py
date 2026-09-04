import django_filters

from locations.models import Location


class LocationFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category_id')
    author = django_filters.NumberFilter(field_name='author_id')
    rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')

    class Meta:
        model = Location
        fields = ['category', 'author', 'rating']
