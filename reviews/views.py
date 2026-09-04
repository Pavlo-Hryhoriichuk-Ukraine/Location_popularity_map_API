from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from reviews.models import Review, ReviewVote
from reviews.permissions import IsReviewAuthorOrAdmin
from reviews.serializers import ReviewSerializer, ReviewVoteSerializer


class ReviewViewSet(ModelViewSet):
	queryset = Review.objects.select_related('location', 'author').all()
	serializer_class = ReviewSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsReviewAuthorOrAdmin]
	filterset_fields = ['location', 'author', 'rating']

	def perform_create(self, serializer) -> None:
		serializer.save(author=self.request.user)

	@action(
		detail=True,
		methods=['post'],
		permission_classes=[IsAuthenticated],
		url_path='vote',
	)
	def vote(self, request, pk=None) -> Response:
		vote_type = request.data.get('vote_type')
		if vote_type not in ReviewVote.VoteType.values:
			return Response(
				{'detail': 'vote_type must be either like or dislike.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		review = self.get_object()
		vote, _ = ReviewVote.objects.update_or_create(
			review=review,
			user=request.user,
			defaults={'vote_type': vote_type},
		)
		return Response(ReviewVoteSerializer(vote).data)
