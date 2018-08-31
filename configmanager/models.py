# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.html import format_html

# Create your models here.


class ECS(models.Model):
    ENABLE = 'Y'
    DISABLE = 'N'
    status_CHOICES = (
        (ENABLE, 'enable'),
        (DISABLE, 'disable'),
    )
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'ECS名称')
    instanceid = models.CharField(max_length=30, verbose_name=u'实例ID')
    IP = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, verbose_name=u'IP地址')
    status = models.CharField(
        max_length=1,
        choices=status_CHOICES,
        default=ENABLE,
    )
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    recently_cpu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'最近CPU使用率')
    recently_memory = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'最近内存使用率')
    recently_diskusage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'最近磁盘使用率')
    regionId = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'所在区域')
    expiredtime = models.DateTimeField(null=True, blank=True, verbose_name=u'过期时间')
    memory = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'内存大小')
    ostype = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'操作系统类型')
    instancestatus = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'实例状态')
    networktype = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'网络类型')
    cpu = models.CharField(max_length=5, null=True, blank=True, verbose_name=u'CPU核数')
    publicipaddress = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, verbose_name=u'公网IP')
    osname = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'操作系统名称')

    class Meta:
        verbose_name = u'ECS信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Siterace(models.Model):
    raceid = models.BigIntegerField()
    alias = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return str(self.alias)


class Site(models.Model):
    ENABLE = 'Y'
    DISABLE = 'N'
    status_CHOICES = (
        (ENABLE, 'enable'),
        (DISABLE, 'disable'),
    )
    fullname = models.CharField(max_length=50)
    shortname = models.CharField(max_length=30)
    configdirname = models.CharField(max_length=50)
    ECSlists = models.ManyToManyField(ECS)
    port = models.PositiveSmallIntegerField(null=True, blank=True)
    testpage = models.CharField(max_length=30, null=True)
    devcharge = models.CharField(max_length=10, null=True, blank=True)
    deployattention = models.TextField(null=True, blank=True)
    modified_time = models.DateTimeField(auto_now=True)
    modified_user = models.CharField(max_length=20, default='admin')
    status = models.CharField(
        max_length=1,
        choices=status_CHOICES,
        default=ENABLE,
    )
    siterace = models.ForeignKey(Siterace, on_delete=models.CASCADE, null=True, blank=True)
    
    def get_ECSlists_list(self):
        list = []
        for e in self.ECSlists.all():
            list.append(e.name)
        return list

    def exist_or_not_in_siterace(self):
        try:
            race_id = self.siterace.id
        except:
            return False
        else:
            return True
    
    def get_raceid(self):
        '''
        返回站点对应的raceid，若无则返回False
        '''
        try:
            race_id = self.siterace.id
        except:
            return 0
        else:
            return race_id

    def get_relation_sites(self):
        '''
        返回所有关联站点fullname属性的list，若无关联站点，则返回False
        '''
        race_id = self.get_raceid()
        if race_id == 0:
            return False
        else:
            L = []
            siterace = Siterace.objects.get(pk=race_id)
            for sr in siterace.site_set.all():
                if sr.id != self.id:
                    L.append(sr.fullname)
        if L:
            return L
        else:
            return False
    
    def get_configfiles(self):
        '''
        返回配置文件filename的list，以分号分隔
        '''
        return ';'.join([c.filename for c in self.configfile_set.all()])
    
    def get_configfiles_id(self):
        '''
        返回配置文件filename的list，以逗号分隔
        '''
        L = []
        for c in self.configfile_set.all():
            L.append(c.id)
        return L

    def update_configfiles(self, post_filenames_list):
        '''
        新增或删除关联的配置文件
        '''
        relation_filenames_list = []
        for c in self.configfile_set.all():
            relation_filenames_list.append(c.filename)
        '''新增'''
        for pfl in post_filenames_list:
            if pfl not in relation_filenames_list:
                self.configfile_set.create(filename=pfl)
        '''删除'''
        for rfl in relation_filenames_list:
            if rfl not in post_filenames_list:
                c = self.configfile_set.get(filename=rfl)
                c.delete()
     
    def have_undeploy_config_or_not(self):
        '''
        得到存在未生效配置的站点对象列表
        '''
        result = False
        for r in self.release_set.all():
            if r.status == 'N':
                return True
                break
            else:
                continue
        return result

    def get_one_slb(self):
        '''
        得到其中一个关联的slb对象
        '''
        for slb in self.slbsite_set.all():
            return slb.SLB

    def get_slb_id_list(self):
        '''
        得到其中一个关联的slb的list对象
        '''
        slb_id_list = []
        if self.slbsite_set.all():
            for slb in self.slbsite_set.all():
                if slb:
                    slb_id_list.append(slb.SLB.id)
            return slb_id_list
        else:
            return [0,]

    def __unicode__(self):
        return self.fullname


class Configfile(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True)
    filename = models.CharField(max_length=30)
    content = models.TextField(null=True, blank=True)
    modified_user = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __unicode__(self):
        return self.filename


class Release(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    ECS = models.ForeignKey(ECS, on_delete=models.CASCADE)
    HAVEDEPLOY = 'Y'
    WAITDEPLOY = 'N'
    status_CHOICES = (
        (HAVEDEPLOY, '已发布'),
        (WAITDEPLOY, '待发布'),
    )
    status = models.CharField(
        "配置状态",
        max_length=1,
        choices=status_CHOICES,
        default=WAITDEPLOY,
    )
    modified_user = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.status

  
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
    apply_user = models.CharField("申请人", max_length=20, null=True, blank=True)
    apply_time = models.DateTimeField("申请时间", auto_now_add=True)
    deploy_user = models.CharField("发布人", max_length=20, null=True, blank=True)
    deploy_time = models.DateTimeField("实际发布时间", null=True, blank=True)
    confamendexplain = models.TextField("配置修改说明", null=True, blank=True)
    remarkexplain = models.TextField("备注事项", null=True, blank=True)
    apply_status = models.CharField(
        max_length=1,
        choices=apply_status_CHOICES,
        null=True,
        blank=True,
        verbose_name="审核状态"
    )
    wishdeploy_time = models.DateField("期望发布日期", null=True, blank=True)

    def __unicode__(self):
        return self.applyproject


class ApplyOperateLog(models.Model):
    applyproject = models.ForeignKey(Apply, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    OperatorName = models.CharField(max_length=30)
    OperationTime = models.DateTimeField()


class Deployitem(models.Model):
    TRUNK = 'T'
    BRANCH = 'B'
    type_CHOICES = (
        (TRUNK, '主干'),
        (BRANCH, '分支'),
    )
    # DEPLOYED = 'Y'
    # WAITFORDEPLOY = 'N'
    # deploy_status_CHOICES = (
    #     (DEPLOYED, '已发布'),
    #     (WAITFORDEPLOY, '待发布'),
    # )
    
    applyproject = models.ForeignKey(Apply, on_delete=models.CASCADE)
    deployorderby = models.PositiveSmallIntegerField("发布顺序", null=True,blank=True)
    jenkinsversion = models.PositiveSmallIntegerField("jenkins版本号", null=True,blank=True)
    type = models.CharField(
        "代码类型",
        max_length=1,
        choices=type_CHOICES,
        default=TRUNK,
    ) 
    deploysite = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, verbose_name="发布站点") 
    # deploy_status = models.CharField(
    #     "发布状态",
    #     max_length=1,
    #     choices=deploy_status_CHOICES,
    #     default=WAITFORDEPLOY,
    # )
    
    def __unicode__(self):
        return self.deploysite
    

class DeployECS(models.Model):
    applyproject = models.ForeignKey(Apply, on_delete=models.CASCADE)
    ECS = models.ForeignKey(ECS, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    ECSdeploystatus = models.CharField(max_length=1, default='N')
    
    def __unicode__(self):
        return self.ECS.name


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class AuthUser(models.Model):
    did = models.IntegerField(blank=True, null=True) 


class ConfigmanagerHistoricalconfigfile(models.Model):
    id = models.IntegerField()
    filename = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)
    modified_user = models.CharField(max_length=20)
    modified_time = models.DateTimeField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    site_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configmanager_historicalconfigfile'
    
    def get_site_fullname(self):
        s= Site.objects.get(pk=self.site_id)
        return s.fullname
    
    def __unicode__(self):
        return self.filename


class SLB(models.Model):
    instanceid = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    ip = models.GenericIPAddressField(protocol='IPv4')
    networktype = models.CharField(max_length=10, null=True, blank=True)
    addresstype = models.CharField(max_length=10)
    createdate = models.DateTimeField()
    
    def __unicode__(self):
        return self.name
   

class SLBsite(models.Model):
    SLB = models.ForeignKey(SLB, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.site.fullname


class SLBhealthstatus(models.Model):
    SLB = models.ForeignKey(SLB, on_delete=models.CASCADE)
    ECS = models.ForeignKey(ECS, on_delete=models.CASCADE)
    SLBstatus = models.CharField(max_length=10, null=True, blank=True)
    healthstatus = models.CharField(max_length=10, null=True, blank=True)
    
    def __unicode__(self):
        return self.healthstatus


class RDS(models.Model):
    instance_id = models.CharField(max_length=100, verbose_name=u'实例ID')
    instance_alias = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'实例别名')
    network_type = models.CharField(max_length=20, verbose_name=u'网络类型')
    engine = models.CharField(max_length=30, verbose_name=u'引擎类型')
    engine_version = models.CharField(max_length=50, verbose_name=u'引擎版本')
    status = models.CharField(max_length=30, verbose_name=u'状态')
    expire_time = models.DateTimeField(verbose_name=u'过期时间')

    class Meta:
        verbose_name = u'RDS信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.instance_id


class RDS_Usage_Record(models.Model):
    rds = models.ForeignKey(RDS, on_delete=models.CASCADE, verbose_name=u'所属RDS')
    cpu_usage = models.FloatField(null=True, blank=True, verbose_name=u'CPU使用率')
    io_usage = models.FloatField(null=True, blank=True, verbose_name=u'IOPS使用率')
    disk_usage = models.FloatField(null=True, blank=True, verbose_name=u'磁盘使用率')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'RDS资源使用率记录表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.add_time)


class Alarm_History(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'告警规则名称')
    namespace = models.CharField(max_length=30, verbose_name=u'告警产品名称')
    alarm_time = models.DateTimeField(null=True, blank=True, verbose_name=u'告警时间')
    value = models.CharField(max_length=10, verbose_name=u'告警的当前值')
    instance_name = models.CharField(max_length=50, verbose_name=u'告警实例名称')
    metric_name = models.CharField(max_length=50, verbose_name=u'监控项名称')
    dimension = models.CharField(max_length=200, verbose_name=u'告警详情')

    class Meta:
        verbose_name = u'告警历史'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


