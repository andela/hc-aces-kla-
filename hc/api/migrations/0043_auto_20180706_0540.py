# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-06 05:40
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20180705_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='escalate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='check',
            name='protocol',
            field=django.contrib.postgres.fields.JSONField(),
        ),
    ]