# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-14 06:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0012_auto_20180612_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siterace',
            name='siteid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configmanager.Site'),
        ),
    ]
