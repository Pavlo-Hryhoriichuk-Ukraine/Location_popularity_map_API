from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from reviews.models import Review


class IsReviewAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Review) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(getattr(request.user, 'is_staff', False)) or (
            request.user.is_authenticated and obj.author.pk == request.user.pk
        )
