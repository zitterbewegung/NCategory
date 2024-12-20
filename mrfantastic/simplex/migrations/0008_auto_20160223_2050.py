# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplex', '0007_auto_20160223_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('started', 'started'), ('finished', 'finished'), ('failed', 'failed')], max_length=20),
        ),
        migrations.AlterField(
            model_name='job',
            name='type',
            field=models.CharField(choices=[('fibonacci', 'fibonacci'), ('power', 'power')], max_length=20),
        ),
    ]
