# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0036_auto_20180712_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecs',
            name='instancename',
        ),
    ]