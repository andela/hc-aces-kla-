
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-29 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20180629_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='value',
            field=models.TextField(blank=True, max_length=25),
        ),
    ]