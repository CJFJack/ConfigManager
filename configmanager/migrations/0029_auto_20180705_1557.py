# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-05 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0028_auto_20180704_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='wishdeploy_time',
            field=models.DateField(blank=True, null=True, verbose_name='\u671f\u671b\u53d1\u5e03\u65e5\u671f'),
        ),
    ]
