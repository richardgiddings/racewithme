# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20171018_1443'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
    ]