# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-04 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0026_auto_20180704_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apply',
            old_name='wishapply_time',
            new_name='wishdeploy_time',
        ),
    ]