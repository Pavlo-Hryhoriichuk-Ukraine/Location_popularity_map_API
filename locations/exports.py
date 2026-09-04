from io import StringIO

import pandas as pd
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response

from locations.serializers import LocationSerializer
from locations.views import LocationViewSet


def export_locations_json(request: Request) -> Response:
    view = LocationViewSet()
    view.request = request
    queryset = view.filter_queryset(view.get_queryset())
    return Response(LocationSerializer(queryset, many=True).data)


def export_locations_csv(request: Request) -> HttpResponse:
    view = LocationViewSet()
    view.request = request
    queryset = view.filter_queryset(view.get_queryset())
    rows = LocationSerializer(queryset, many=True).data
    frame = pd.DataFrame(rows)
    output = StringIO()
    frame.to_csv(output, index=False)
    response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="locations.csv"'
    return response
