# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0017_auto_20180618_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_user', models.CharField(max_length=20)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('ECS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configmanager.ECS')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configmanager.Site')),
            ],
        ),
    ]
