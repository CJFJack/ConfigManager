# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-17 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0011_auto_20180517_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecs',
            name='modified_user',
            field=models.CharField(max_length=20),
        ),
    ]
