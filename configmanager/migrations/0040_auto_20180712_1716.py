# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0039_auto_20180712_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecs',
            name='memory',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
