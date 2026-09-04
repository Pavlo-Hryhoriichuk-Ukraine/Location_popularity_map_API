from django.contrib import admin
from django.urls import path

from config.health import health_check

urlpatterns = [ # type: ignore
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
]
