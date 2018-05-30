import logging

from django.db.transaction import atomic
from django.conf import settings
import warcat.model
import scrapy

from instrument_history_api.api_app.models import InstrumentRecord, WarcInstrumentRecord, WarcFile, WarcFileEntry
from instrument_history_api.warc_utils import text_content_from_record, filter_response_records
from instrument_history_api.html_parsers import parse_overview_key_stats


LOGGER = logging.getLogger(__name__)

DUMP_ERRORING = False


def instrument_records_from_warc_file(path_obj, url_predicate=settings.HAS_INSTRUMENT_URL):
    warc_file, file_created = WarcFile.objects.get_or_create(
        filename=path_obj.name,
        defaults={'filesizeBytes': path_obj.stat().st_size},
    )
    if not file_created:
        # File has been read already, skip processing it
        return []

    warc = warcat.model.WARC()
    try:
        warc.load(path_obj.path)
    except:
        LOGGER.exception('Error loading file %s', path_obj.path)
        return []
    response_records = filter_response_records(warc.records)
    parsed_response_records = 0
    for response_record in response_records:
        url = response_record.header.fields['WARC-Target-URI']
           
        if not url_predicate(url):
            # The URL is not of interest -> skip
            continue
        
        name = settings.GET_INSTRUMENT_NAME(url)
        response_text = text_content_from_record(response_record)
        selector = scrapy.Selector(text=response_text)

        try:
            with atomic():
                warc_entry, entry_created = WarcFileEntry.objects.get_or_create(
                    record_id=response_record.record_id,
                    warc_file=warc_file
                )
                if not entry_created:
                    # Entry processed before, skip!
                    continue
                key_stats = parse_overview_key_stats(selector)
        except:
            LOGGER.exception('Error parsing %s in WARC record %s in file %s', url, response_record.record_id, path_obj.path)            
            if DUMP_ERRORING:
                fname = '/tmp/' + path_obj.name + '_' + response_record.record_id + '.html'
                LOGGER.error('Dumping erroring html to %s', fname)
                with open(fname, 'w') as f:
                    f.write(response_text)
            continue
        else:
            parsed_response_records += 1
            # Create WARC entry only if we do not have any value for this instrument (not even a InstrumentRecord that is not instance of WarcInstrumentRecord)
            # https://stackoverflow.com/questions/4064808/django-model-inheritance-create-sub-instance-of-existing-instance-downcast            
            with atomic():
                base_record, created = InstrumentRecord.objects.get_or_create(
                    name=name,
                    value_date=key_stats['value_date'],
                    defaults={'value': key_stats['value']}
                )
                if not created:
                    LOGGER.info("Already entry for %s @ %s. Skipping this WARC entry", name, key_stats['value_date'])
                    continue
                
                new_record = WarcInstrumentRecord(**{
                    '%s_ptr_id' % InstrumentRecord.__name__.lower(): base_record.pk})
                new_record.__dict__.update(base_record.__dict__)
                new_record.url = url
                new_record.warc_entry = warc_entry
            
            yield new_record
        LOGGER.info('Parsed %d entries in file %s', parsed_response_records, path_obj.path)


def chunks(l, n):
    """Yield successive n-sized chunks from l.

    From https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def process_warc_files(*path_objs):
    # For performance reasons, commit on every 10 files
    file_index = 0
    for path_objs_chunk in chunks(path_objs, 10):
        with atomic():
            for path_obj in path_objs_chunk:
                for record in instrument_records_from_warc_file(path_obj):
                    record.save()
                file_index += 1
                LOGGER.debug("Processed file %d: %s", file_index, path_obj.path)
