# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-21 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0052_auto_20180719_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slb',
            name='ip',
            field=models.GenericIPAddressField(protocol='IPv4'),
        ),
    ]