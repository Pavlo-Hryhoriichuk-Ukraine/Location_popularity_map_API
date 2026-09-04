from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from locations.models import Location


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Location) -> bool:
        is_admin = bool(getattr(request.user, 'is_staff', False))
        is_author = request.user.is_authenticated and obj.author.pk == request.user.pk
        return is_admin or is_author
