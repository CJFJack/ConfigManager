# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-13 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0041_slb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slb',
            name='createdate',
            field=models.DateTimeField(),
        ),
    ]