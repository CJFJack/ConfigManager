# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords

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
    history = HistoricalRecords()

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

   
class Apply(models.Model):
    WAITFORCOMMIT = 'WC'
    WAITFORDEPLOY = 'WD'
    CANCELED = 'C'
    DEPLOYED = 'D'
    DEVMANAGERAPPROVAL = 'DA'
    OPERMANAGERAPPROVAL = 'OA'
    ENGINEERAPPROVAL = 'EA'
    TESTMANAGERAPPROVAL = 'TA'
    TECHNICALDIRECTORYAPPROVAL = 'TDA'
    status_CHOICES = (
        (WAITFORCOMMIT, '待提交'),
        (WAITFORDEPLOY, '待发布'),
        (CANCELED, '已取消'),
        (DEPLOYED, '已发布'),
        (DEVMANAGERAPPROVAL, '研发经理审批中'),
        (OPERMANAGERAPPROVAL, '运维经理审批中'),
        (ENGINEERAPPROVAL, '运维工程师审批中'),
        (TESTMANAGERAPPROVAL, '测试经理审批中'),
        (TECHNICALDIRECTORYAPPROVAL, '技术总监审批中'),
    )

    applyproject = models.CharField(max_length=50)
    status = models.CharField(
        max_length=3,
        choices=status_CHOICES,
        default=WAITFORCOMMIT,
    ) 
    apply_user = models.CharField(max_length=20)
    apply_time = models.DateTimeField(auto_now_add=True)
    deploy_user = models.CharField(max_length=20, null=True, blank=True)
    deploy_time = models.DateTimeField(null=True, blank=True)
    confamendexplain = models.TextField(null=True, blank=True)
    remarkexplain = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.applyproject


class deployitem(models.Model):
    TRUNK = 'T'
    BRANCH = 'B'
    type_CHOICES = (
        (TRUNK, '主干'),
        (BRANCH, '分支'),
    )
    DEPLOYED = 'Y'
    WAITFORDEPLOY = 'N'
    status_CHOICES = (
        (DEPLOYED, 'Y'),
        (WAITFORDEPLOY, 'N'),
    )

    applyproject = models.ForeignKey(Apply, on_delete=models.CASCADE)
    deployorderby = models.PositiveSmallIntegerField(null=True,blank=True)
    jenkinsversion = models.PositiveSmallIntegerField(null=True,blank=True)
    type = models.CharField(
        max_length=1,
        choices=type_CHOICES,
        default=TRUNK,
    ) 
    deploysite = models.ManyToManyField(Site, blank=True)
    status = models.CharField(
        max_length=1,
        choices=status_CHOICES,
        default=WAITFORDEPLOY,                                                                                                                    
    )
    
    def __unicode__(self):
        return self.jenkinsversion
    



