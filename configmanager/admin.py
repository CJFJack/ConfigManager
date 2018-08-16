# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import Site, ECS, Configfile, Apply, Deployitem, Siterace, Person, Group, Membership
from datetime import datetime
from django.core.files import File
import os


class ECSAdmin(admin.ModelAdmin):
    fieldsets = [
        ('server_info',      {'fields': ['name']}),
        (None,               {'fields': ['instanceid']}),
        (None,               {'fields': ['IP']}),
        (None,               {'fields': ['status']}),
    ]

    list_display = ('name', 'instanceid', 'IP', 'status', 'modified_time')
    list_filter = ['status', 'name']
    search_fields = ['name', 'IP']


class ConfigfileInline(admin.TabularInline):
    model = Configfile
    extra = 0
    readonly_fields = ['site',]
    fieldsets = [
        (None, {'fields': ['filename', 'content']}),
    ]
    list_display = ('site', 'filename', 'modified_user', 'modified_time')
    #search_fields = ['']

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        config_path = os.path.join('/releaseconfig', obj.filename)
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        file_name = os.path.join(config_path, obj.filename)
        with open(file_name, 'w') as f:
            myfile = File(f)
            myfile.write(obj.content)
        super(ConfigfileInline, self).save_model(request, obj, form, change)

 
class SiteAdmin(admin.ModelAdmin):

    def get_ECSlists(self, obj):
        return ', '.join([e.name for e in obj.ECSlists.all()])
    get_ECSlists.short_description = 'ECSs'

    def get_configfiles(self, obj):
        return ', '.join([c.filename for c in obj.configfile_set.all()])
    get_configfiles.short_description = 'Configfiles'

    def make_sites_disable(self, request, queryset):
        rows_updated = queryset.update(status='N')
        if rows_updated == 1:
            message_bit = "1 site was"
        else:
            message_bit = "%s sites were" % rows_updated
        self.message_user(request, "%s successfully marked as disable." % message_bit)
    make_sites_disable.short_description = "Disable selected sites"

    def make_sites_enable(self, request, queryset):
        rows_updated = queryset.update(status='Y')
        if rows_updated == 1:
            message_bit = "1 site was"
        else:
            message_bit = "%s sites were" % rows_updated
        self.message_user(request, "%s successfully marked as enable." % message_bit)
    make_sites_enable.short_description = "Enabke selected site"
 
    fieldsets = [
        ('site_info', {'fields': ['fullname', 'shortname', 'configdirname', 'ECSlists', 'port', 'testpage', 'status', 'deployattention', 'devcharge']}),
    ]
    filter_horizontal = ('ECSlists',)
    inlines = [ConfigfileInline] 

    list_display = ('fullname', 'shortname', 'configdirname', 'get_ECSlists', 'get_configfiles', 'status', 'modified_user', 'modified_time')
    list_filter = ['status', 'port']
    search_fields = ['fullname', 'port']
    actions = [make_sites_disable, make_sites_enable]

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(SiteAdmin, self).save_model(request, obj, form, change)


class DeployitemInline(admin.TabularInline):
    model = Deployitem
    extra = 0
    def get_readonly_fields(self, request, obj=Apply):
        if obj and obj.status == 'WC':
            self.readonly_fields =  []
            return self.readonly_fields
        if obj and obj.status != 'WC' and obj.status != 'WD':
            self.readonly_fields = ['deployorderby', 'jenkinsversion', 'deploysite', 'type']
            return self.readonly_fields
        if obj and obj.status == 'WD':
            self.readonly_fields = ['deployorderby', 'jenkinsversion', 'deploysite', 'type']
            return self.readonly_fields
        else:
            self.readonly_fields = []
            return self.readonly_fields

    def get_ECSlists(self, obj):
        return obj.deploy_site.ECSlists
        
    fieldsets = [
        (None, {'fields': ['deployorderby', 'jenkinsversion', 'type', 'deploysite']}),
    ]


class ApplyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        user_group = request.user.groups.all()[0].name
        if request.user.username == 'admin':
            self.readonly_fields = []
            return self.readonly_fields
        '''创建时'''
        if not obj:
            self.readonly_fields = ['status', 'apply_status']
            return self.readonly_fields
        '''已取消、已发布'''
        if obj and (obj.status == 'D' or obj.status == 'C'):
            self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''待提交'''
        if obj and obj.status == 'WC':
            if user_group == '研发经理' or user_group == '测试工程师' or user_group == '研发工程师':
                self.readonly_fields = ['status',]
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''研发经理审批中'''
        if obj and obj.status == 'DA':
            if user_group == '研发经理': 
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status']
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''测试经理审批中'''
        if obj and obj.status == 'TA':
            if user_group == '测试经理': 
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status']
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''运维工程师审批中'''
        if obj and obj.status == 'EA':
            if user_group == '运维工程师': 
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status']
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''运维经理审批中'''
        if obj and obj.status == 'OA':
            if user_group == '运维经理': 
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status']
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''技术总监审批中'''
        if obj and obj.status == 'TDA':
            if user_group == '技术总监': 
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status']
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields
        '''待发布'''
        if obj and obj.status == 'WD':
            if user_group == '运维工程师': 
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status']
            else:
                self.readonly_fields = ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']
            return self.readonly_fields

    fieldsets = [
        (None, {'fields': ['applyproject', 'confamendexplain', 'remarkexplain', 'status', 'apply_status']}),
    ]
    inlines = [DeployitemInline]
    list_display = ('applyproject', 'status', 'apply_user', 'apply_time', 'deploy_user', 'deploy_time')
    list_filter = ('status',)
    search_fields = ('applyproject',)
    date_hierarchy = 'apply_time'

    def save_model(self, request, obj, form, change):
        '''记录发布申请人'''
        if obj.apply_user is None:
            obj.apply_user = request.user.username
        '''状态待提交，审核通过'''
        if obj.status == 'WC' and obj.apply_status == 'Y':
            obj.status = 'DA'
            obj.apply_status = ''
        '''状态待提交，审核不通过'''
        if obj.status == 'WC' and obj.apply_status == 'N':
            obj.status = 'C'
        '''状态研发经理审批中，审核不通过'''
        if obj.status == 'DA' and obj.apply_status == 'N':
            obj.status = 'WC'
            obj.apply_status = ''
        '''状态研发经理审批中，审核通过'''
        if obj.status == 'DA' and obj.apply_status == 'Y':
            obj.status = 'TA'
            obj.apply_status = ''
        '''状态测试经理审批中，审核不通过'''
        if obj.status == 'TA' and obj.apply_status == 'N':
            obj.status = 'WC'
            obj.apply_status = ''
        '''状态测试经理审批中，审核通过'''
        if obj.status == 'TA' and obj.apply_status == 'Y':
            obj.status = 'EA'
            obj.apply_status = ''
        '''状态运维工程师审批中，审核不通过'''
        if obj.status == 'EA' and obj.apply_status == 'N':
            obj.status = 'WC'
            obj.apply_status = ''
        '''状态运维工程师审批中，审核通过'''
        if obj.status == 'EA' and obj.apply_status == 'Y':
            obj.status = 'OA'
            obj.apply_status = ''
        '''状态运维经理审批中，审核不通过'''
        if obj.status == 'OA' and obj.apply_status == 'N':
            obj.status = 'WC'
            obj.apply_status = ''
        '''状态运维经理审批中，审核通过'''
        if obj.status == 'OA' and obj.apply_status == 'Y':
            obj.status = 'TDA'
            obj.apply_status = ''
        '''状态技术总监审批中，审核不通过'''
        if obj.status == 'TDA' and obj.apply_status == 'N':
            obj.status = 'WC'
            obj.apply_status = ''
        '''状态技术总监审批中，审核通过'''
        if obj.status == 'TDA' and obj.apply_status == 'Y':
            obj.status = 'WD'
            obj.apply_status = ''
        '''状态待发布，审核不通过'''
        if obj.status == 'WD' and obj.apply_status == 'N':
            obj.apply_status = ''
        '''状态待发布，审核通过，记录发布人、发布时间'''
        if obj.status == 'WD' and obj.apply_status == 'Y':
            obj.status = 'D'
            obj.apply_status = 'Y'
            obj.deploy_user = request.user.username
            obj.deploy_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        super(ApplyAdmin, self).save_model(request, obj, form, change)
    
    list_per_page = 10


class DeployitemAdmin(admin.ModelAdmin):
    def get_ECSlists(self, obj):
        return ', '.join([e.name for e in obj.deploysite.ECSlists.all()])
    get_ECSlists.short_description = 'ECSs'

    list_display = ['applyproject', 'deployorderby', 'jenkinsversion', 'type', 'deploysite', 'get_ECSlists']
    list_filter = ['applyproject',]
    search_fields = ['applyproject',]
    


class MembershipInline(admin.TabularInline):
    model = Group.members.through
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ('members',)


admin.site.site_title = '运维管理平台'

admin.site.register(ECS, ECSAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(Deployitem, DeployitemAdmin)
admin.site.register(Configfile,SimpleHistoryAdmin)
admin.site.register(Siterace)

