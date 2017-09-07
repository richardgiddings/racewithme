# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 11:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_name', models.CharField(max_length=50)),
                ('race_site_link', models.URLField()),
                ('race_date', models.DateField()),
                ('race_time', models.TimeField()),
                ('race_distance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Distance')),
                ('race_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Location')),
            ],
        ),
        migrations.CreateModel(
            name='UserRace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Not Interested'), ('1', 'Interested'), ('2', 'Going'), ('3', 'Completed')], default='0', max_length=14)),
                ('just_for_fun', models.BooleanField()),
                ('target_hours', models.IntegerField(blank=True, null=True)),
                ('target_minutes', models.IntegerField(blank=True, null=True)),
                ('target_seconds', models.IntegerField(blank=True, null=True)),
                ('achieved_hours', models.IntegerField(blank=True, null=True)),
                ('achieved_minutes', models.IntegerField(blank=True, null=True)),
                ('achieved_seconds', models.IntegerField(blank=True, null=True)),
                ('race_results_external', models.URLField(blank=True, null=True)),
                ('race_photos_external', models.URLField(blank=True, null=True)),
                ('race', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Race')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]