from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from locations.models import Location


class Review(models.Model):
	location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
	rating = models.PositiveSmallIntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(5)],
	)
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		constraints = [
			models.UniqueConstraint(
				fields=['location', 'author'],
				name='one_review_per_user_location',
			),
		]
		indexes = [
			models.Index(fields=['location', 'created_at']),
			models.Index(fields=['rating']),
		]

	def __str__(self) -> str:
		return f'{self.location.name}: {self.rating}/5'


class ReviewVote(models.Model):
	class VoteType(models.TextChoices):
		LIKE = 'like', 'Like'
		DISLIKE = 'dislike', 'Dislike'

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_votes')
	vote_type = models.CharField(max_length=7, choices=VoteType.choices)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['review', 'user'],
				name='one_vote_per_user_review',
			),
		]

	def __str__(self) -> str:
		return f'{self.user.username}: {self.vote_type}'
