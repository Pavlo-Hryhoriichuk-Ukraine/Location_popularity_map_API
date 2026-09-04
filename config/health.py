from django.http import JsonResponse
from rest_framework.request import Request

def health_check(request: Request) -> JsonResponse:
    return JsonResponse({'status': 'ok'})


def api_root(request: Request) -> JsonResponse:
    return JsonResponse(
        {
            'health': '/health/',
            'auth': {
                'register': '/auth/register/',
                'login': '/auth/login/',
                'logout': '/auth/logout/',
                'password_reset': '/auth/password-reset/',
            },
            'categories': '/api/categories/',
            'locations': '/api/locations/',
            'reviews': '/api/reviews/',
            'admin': '/admin/',
        }
    )
