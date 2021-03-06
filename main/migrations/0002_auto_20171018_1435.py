# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='city',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='race',
            name='location',
            field=location_field.models.plain.PlainLocationField(default='', max_length=63),
            preserve_default=False,
        ),
    ]
