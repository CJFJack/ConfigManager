# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-16 09:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0045_auto_20180716_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slbhealthstatus',
            name='SLBsite',
        ),
        migrations.AddField(
            model_name='slbhealthstatus',
            name='SLB',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configmanager.SLB'),
        ),
        migrations.AlterField(
            model_name='slbhealthstatus',
            name='SLBstatus',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='slbhealthstatus',
            name='healthstatus',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
