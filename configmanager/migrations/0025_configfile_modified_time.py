# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-19 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0024_configfile_sitecluster'),
    ]

    operations = [
        migrations.AddField(
            model_name='configfile',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
