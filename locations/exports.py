from io import StringIO

import pandas as pd
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.request import Request

from locations.serializers import LocationSerializer
from locations.views import LocationViewSet


def export_locations_json(request: HttpRequest) -> JsonResponse:
    view = LocationViewSet()
    view.request = Request(request)
    queryset = view.filter_queryset(view.get_queryset())
    return JsonResponse(LocationSerializer(queryset, many=True).data, safe=False)


def export_locations_csv(request: HttpRequest) -> HttpResponse:
    view = LocationViewSet()
    view.request = Request(request)
    queryset = view.filter_queryset(view.get_queryset())
    rows = LocationSerializer(queryset, many=True).data
    frame = pd.DataFrame(rows)
    output = StringIO()
    frame.to_csv(output, index=False)
    response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="locations.csv"'
    return response
