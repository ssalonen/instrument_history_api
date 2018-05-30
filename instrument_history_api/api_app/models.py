from django.db import models


# Create your models here.
class WarcFile(models.Model):
    """
    Warc file
    """
    filename = models.CharField(max_length=256)
    filesizeBytes = models.PositiveIntegerField()


class WarcFileEntry(models.Model):
    """
    Warc file entry (record)
    """
    warc_file = models.ForeignKey(WarcFile, on_delete=models.CASCADE)
    record_id = models.CharField(max_length=256)


class InstrumentRecord(models.Model):
    """
    Record of instrument value at a given date
    """
    name = models.CharField(max_length=512)
    value = models.FloatField()
    value_date = models.DateTimeField()


# Warc loader code assumes that this class inherits InstrumentRecord (ptr_id)
class WarcInstrumentRecord(InstrumentRecord):
    """
    Record of instrument value at a given date, in a warc file
    """
    url = models.URLField()
    warc_entry = models.OneToOneField(WarcFileEntry, on_delete=models.CASCADE, primary_key=True)
