import logging

from instrument_history_api.api_app.models import InstrumentRecord
from rest_framework import serializers

logger = logging.getLogger(__name__)

class InstrumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstrumentRecord
        fields = ('name', 'value', 'value_date')
