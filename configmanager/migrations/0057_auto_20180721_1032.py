# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-21 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0056_auto_20180721_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyoperatelog',
            name='OperationTime',
            field=models.DateTimeField(),
        ),
    ]