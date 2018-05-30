# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('value', models.FloatField()),
                ('value_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='WarcFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=256)),
                ('filesizeBytes', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WarcFileEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='WarcInstrumentRecord',
            fields=[
                ('instrumentrecord_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='api_app.InstrumentRecord')),
                ('url', models.URLField()),
                ('warc_entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api_app.WarcFileEntry')),
            ],
            bases=('api_app.instrumentrecord',),
        ),
        migrations.AddField(
            model_name='warcfileentry',
            name='warc_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.WarcFile'),
        ),
    ]
