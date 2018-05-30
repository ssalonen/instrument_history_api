import logging

from django.db.transaction import atomic
from django.conf import settings

import pandas as pd
from pytz import UTC

from instrument_history_api.api_app.models import InstrumentRecord

LOGGER = logging.getLogger(__name__)


@atomic
def process_seligson():
    for url in settings.SELIGSON_URLS:
        for record in parse_records_in_seligson(url):
            record.save()


def parse_records_in_seligson(url):
    if not settings.HAS_INSTRUMENT_URL(url):
        msg = "Unknown seligson URL %s" % url
        LOGGER.error(msg)
        raise ValueError(msg)
    name = settings.GET_INSTRUMENT_NAME(url)

    try:
        last_parsed_date = getattr(InstrumentRecord.objects.filter(
            name=name).order_by('-value_date').first(), 'value_date', None)
    except IndexError:
        last_parsed_date = None
    
    LOGGER.info('last_parsed_date: %s', last_parsed_date)

    data = pd.read_csv(url, sep=';', names=['date', 'value'], dayfirst=True, parse_dates=['date'],
                       index_col='date')
    try:
        data.index = data.index.tz_localize(UTC)
    except TypeError: pass

    if last_parsed_date:
        new_data = data.loc[last_parsed_date:, :].iloc[1:]
    else:
        new_data = data
    
    for date, value in new_data.itertuples():
        entry, entry_created = InstrumentRecord.objects.get_or_create(
                name=name, value_date=date, 
                defaults={'value': value})
        if not entry_created:
            continue
        yield entry
