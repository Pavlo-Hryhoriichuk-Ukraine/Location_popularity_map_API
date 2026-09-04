from django.contrib import admin
from django.urls import include, path

from config.auth_api import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
)
from config.health import health_check

urlpatterns = [ # type: ignore
    path('health/', health_check, name='health-check'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path(
        'auth/password-reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password-reset-confirm',
    ),
    path('api/', include('locations.urls')),
    path('api/', include('reviews.urls')),
    path('admin/', admin.site.urls),
]
