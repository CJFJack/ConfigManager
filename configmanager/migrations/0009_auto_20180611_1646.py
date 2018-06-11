# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 08:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0008_auto_20180609_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteRace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RaceID', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='site',
            name='siterace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configmanager.SiteRace'),
        ),
    ]
