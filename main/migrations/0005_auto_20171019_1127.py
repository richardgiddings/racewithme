# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_delete_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='race_location',
            field=models.CharField(default='Bristol', help_text='Enter a location then select on map', max_length=255),
        ),
    ]
