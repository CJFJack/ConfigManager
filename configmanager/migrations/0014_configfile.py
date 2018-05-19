# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 02:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0013_auto_20180518_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conf_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configmanager.Site')),
            ],
        ),
    ]
