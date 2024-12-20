# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-19 20:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simplex', '0016_auto_20160419_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 53, 47, 317016, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 53, 47, 316013, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='job',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 53, 47, 329778, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='print',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 53, 47, 321485, tzinfo=utc)),
        ),
    ]
