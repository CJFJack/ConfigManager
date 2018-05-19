# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ECS(models.Model):
    ENABLE = 'Y'
    DISABLE = 'N'
    status_CHOICES = (
        (ENABLE, 'enable'),
        (DISABLE, 'disable'),
    )
    name = models.CharField(max_length=30)
    instanceid = models.CharField(max_length=30)
    IP = models.CharField(max_length=20)
    status = models.CharField(
        max_length=1,
        choices=status_CHOICES,
        default=ENABLE,
    )
    modified_user = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Configfile(models.Model):
    sitecluster = models.CharField(max_length=30)
    filename = models.CharField(max_length=30)
    content = models.TextField(null=True, blank=True)
    modified_user = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.sitecluster


class Site(models.Model):
    ENABLE = 'Y'
    DISABLE = 'N'
    status_CHOICES = (
        (ENABLE, 'enable'),
        (DISABLE, 'disable'),
    )
    fullname = models.CharField(max_length=30)
    shortname = models.CharField(max_length=30)
    configdirname = models.CharField(max_length=50)
    ECSlists = models.ManyToManyField(ECS)
    configfiles = models.ManyToManyField(Configfile, blank=True)
    port = models.PositiveSmallIntegerField(null=True)
    testpage = models.CharField(max_length=30, null=True)
    devcharge = models.CharField(max_length=10, null=True)
    deployattention = models.TextField(null=True, blank=True)
    modified_time = models.DateTimeField(auto_now=True)
    modified_user = models.CharField(max_length=20, default='admin')
    status = models.CharField(
        max_length=1,
        choices=status_CHOICES,
        default=ENABLE,
    )
    
    def __unicode__(self):
        return self.fullname

   
