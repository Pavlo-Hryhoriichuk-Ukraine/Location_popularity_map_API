from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class ActiveLocationQuerySet(models.QuerySet['Location']):
	def delete(self) -> tuple[int, dict[str, int]]:
		updated = self.update(deleted_at=timezone.now())
		return updated, {'locations.Location': updated}


class ActiveLocationManager(models.Manager['Location']):
	def get_queryset(self) -> ActiveLocationQuerySet:
		return ActiveLocationQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class Location(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='locations')
	address = models.CharField(max_length=300)
	latitude = models.DecimalField(
		max_digits=9,
		decimal_places=6,
		validators=[MinValueValidator(-90), MaxValueValidator(90)],
	)
	longitude = models.DecimalField(
		max_digits=9,
		decimal_places=6,
		validators=[MinValueValidator(-180), MaxValueValidator(180)],
	)
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='locations')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	objects = ActiveLocationManager()
	all_objects = models.Manager['Location']()

	class Meta:
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['category', 'created_at']),
			models.Index(fields=['author', 'created_at']),
			models.Index(fields=['deleted_at']),
		]

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		self.deleted_at = timezone.now()
		self.save(update_fields=['deleted_at'], using=using)
		return 1, {'locations.Location': 1}

	def restore(self) -> None:
		self.deleted_at = None
		self.save(update_fields=['deleted_at'])

	def __str__(self) -> str:
		return self.name
