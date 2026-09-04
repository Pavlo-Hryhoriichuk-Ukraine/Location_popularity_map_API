from django.contrib import admin

from locations.models import Category, Location, LocationViewEvent


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'created_at']
	search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'category', 'author', 'created_at', 'deleted_at']
	list_filter = ['category', 'deleted_at']
	search_fields = ['name', 'description', 'address']


@admin.register(LocationViewEvent)
class LocationViewEventAdmin(admin.ModelAdmin):
	list_display = ['location', 'user', 'created_at']
	list_filter = ['created_at']
	readonly_fields = ['location', 'user', 'created_at']
