# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-04 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_merge_20180704_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='priority',
            field=models.IntegerField(default=1),
        ),
    ]
