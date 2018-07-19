# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-04 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20180703_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='checks',
        ),
        migrations.RemoveField(
            model_name='report',
            name='user',
        ),
        migrations.AddField(
            model_name='check',
            name='runs_too_often',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
 