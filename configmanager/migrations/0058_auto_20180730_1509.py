# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-30 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0057_auto_20180721_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecs',
            name='IP',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='IPv4'),
        ),
    ]
