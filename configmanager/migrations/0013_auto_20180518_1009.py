# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 02:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configmanager', '0012_auto_20180517_2248'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='name',
            new_name='fullname',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='short',
            new_name='shortname',
        ),
    ]
