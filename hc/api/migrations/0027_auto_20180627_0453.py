# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-27 04:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_after',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='check',
            name='nag_interval',
            field=models.DurationField(default=datetime.timedelta(1, 3600)),
        ),
    ]