# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-12 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0011_siterace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siterace',
            name='raceid',
            field=models.BigIntegerField(),
        ),
    ]