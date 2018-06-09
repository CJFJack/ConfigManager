# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-09 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0007_auto_20180605_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configfile',
            name='sitecluster',
        ),
        migrations.RemoveField(
            model_name='historicalconfigfile',
            name='sitecluster',
        ),
        migrations.RemoveField(
            model_name='site',
            name='configfiles',
        ),
        migrations.AddField(
            model_name='configfile',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configmanager.Site'),
        ),
        migrations.AddField(
            model_name='historicalconfigfile',
            name='site',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='configmanager.Site'),
        ),
    ]
