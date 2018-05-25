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

    APPROVAL = 'Y'
    NOAPPROVAL = 'N'
    apply_status_CHOICES = (
        (APPROVAL, '审批通过'),
        (NOAPPROVAL, '审批不通过'),
    )

    def apply_user_default(self, request, obj, form, change):
        return request.user.username

    applyproject = models.CharField("申请编号", max_length=50)
    status = models.CharField(
        "状态",
        max_length=3,
        choices=status_CHOICES,
        default=WAITFORCOMMIT,
    ) 
    apply_user = models.CharField("申请人", max_length=20,null=True, blank=True)
    apply_time = models.DateTimeField("申请时间", auto_now_add=True)
    deploy_user = models.CharField("发布人", max_length=20, null=True, blank=True)
    deploy_time = models.DateTimeField("发布时间", null=True, blank=True)
    confamendexplain = models.TextField("配置修改说明", null=True, blank=True)
    remarkexplain = models.TextField("备注事项", null=True, blank=True)
    apply_status = models.CharField(
        max_length=1,
        choices=apply_status_CHOICES,
        null=True,
        blank=True,
        verbose_name="审核状态"
    )

    def __unicode__(self):
        return self.applyproject


class Deployitem(models.Model):
    TRUNK = 'T'
    BRANCH = 'B'
    type_CHOICES = (
        (TRUNK, '主干'),
        (BRANCH, '分支'),
    )
    DEPLOYED = 'Y'
    WAITFORDEPLOY = 'N'
    deploy_status_CHOICES = (
        (DEPLOYED, '已发布'),
        (WAITFORDEPLOY, '待发布'),
    )
    
    applyproject = models.ForeignKey(Apply, on_delete=models.CASCADE)
    deployorderby = models.PositiveSmallIntegerField("发布顺序", null=True,blank=True)
    jenkinsversion = models.PositiveSmallIntegerField("jenkins版本号", null=True,blank=True)
    type = models.CharField(
        "代码类型",
        max_length=1,
        choices=type_CHOICES,
        default=TRUNK,
    ) 
    deploysite = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, verbose_name="发布站点",) 
    deploy_status = models.CharField(
        "发布状态",
        max_length=1,
        choices=deploy_status_CHOICES,
        default=WAITFORDEPLOY,                                                                                                                    
    )
    
    def __unicode__(self):
        return self.deploy_status
