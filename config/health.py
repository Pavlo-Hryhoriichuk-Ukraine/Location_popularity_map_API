from django.http import JsonResponse
from rest_framework.request import Request

def health_check(request: Request) -> JsonResponse:
    return JsonResponse({'status': 'ok'})
