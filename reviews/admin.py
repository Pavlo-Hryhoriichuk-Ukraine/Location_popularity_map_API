from django.contrib import admin

from reviews.models import Review, ReviewVote


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['location', 'author', 'rating', 'created_at']
	list_filter = ['rating', 'created_at']
	search_fields = ['location__name', 'author__username', 'comment']


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
	list_display = ['review', 'user', 'vote_type', 'created_at']
	list_filter = ['vote_type', 'created_at']
	readonly_fields = ['review', 'user', 'created_at']
