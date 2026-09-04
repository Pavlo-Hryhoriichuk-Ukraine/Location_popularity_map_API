from rest_framework import serializers

from locations.models import Category, Location


class CategorySerializer(serializers.ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class LocationSerializer(serializers.ModelSerializer[Location]):
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
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
