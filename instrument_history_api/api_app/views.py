from django.shortcuts import render
from django.conf import settings


from rest_framework import viewsets
#from rest_framework import generics
from rest_framework.filters import FilterSet, OrderingFilter

from rest_framework.views import APIView
from rest_framework.response import Response


import django_filters

from instrument_history_api.api_app.serializers import InstrumentSerializer
from instrument_history_api.api_app.models import InstrumentRecord
from instrument_history_api.warc_loader import process_warc_files
from instrument_history_api.seligson_loader import process_seligson
import os


class InstrumentFilter(FilterSet):
    value_date_gte = django_filters.DateTimeFilter(name="value_date", lookup_expr='gte')
    value_date_lte = django_filters.DateTimeFilter(name="value_date", lookup_expr='lte')
    class Meta:
        model = InstrumentRecord
        fields = ['value_date_gte']



class InstrumentView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = InstrumentRecord.objects.all()
    serializer_class = InstrumentSerializer
    ordering_fields = ('value_date',)
    filter_backends = (OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = InstrumentFilter


class Refresh(APIView):
    """
    Refresh WARC files
    """

    def iter_paths(self, root):
        paths = os.scandir(root)
        for entry in paths:
            if entry.is_file() and entry.name.endswith('.warc.gz'):
                yield entry

    def get(self, request, format=None):
        """
        Refresh warc cache
        """
        process_seligson()
        process_warc_files(*self.iter_paths(settings.WARC_FOLDER))
        return Response('Success')
    

# e.g.  http://localhost:8000/instruments/?ordering=value_date&value_date_gte=2017-02-01&value_date_lte=2017-02-02