from rest_framework import serializers

from locations.models import Category, Location


class CategorySerializer(serializers.ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class LocationSerializer(serializers.ModelSerializer[Location]):
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    recent_view_count = serializers.IntegerField(read_only=True)
    popularity_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'description',
            'category',
            'address',
            'latitude',
            'longitude',
            'author',
            'created_at',
            'updated_at',
            'average_rating',
            'review_count',
            'recent_view_count',
            'popularity_score',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
