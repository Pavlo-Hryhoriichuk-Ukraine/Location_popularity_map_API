from rest_framework import serializers

from reviews.models import Review, ReviewVote


class ReviewSerializer(serializers.ModelSerializer[Review]):
    class Meta:
        model = Review
        fields = [
            'id',
            'location',
            'author',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class ReviewVoteSerializer(serializers.ModelSerializer[ReviewVote]):
    class Meta:
        model = ReviewVote
        fields = ['id', 'review', 'user', 'vote_type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'review', 'user', 'created_at', 'updated_at']
