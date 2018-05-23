# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import Site, ECS, Configfile, Apply, Deployitem


class ECSAdmin(admin.ModelAdmin):
    fieldsets = [
        ('server_info',      {'fields': ['name']}),
        (None,               {'fields': ['instanceid']}),
        (None,               {'fields': ['IP']}),
        (None,               {'fields': ['status']}),
    ]

    list_display = ('name', 'instanceid', 'IP', 'status', 'modified_user', 'modified_time') 
    list_filter = ['status', 'name']
    search_fields = ['name', 'IP']

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(ECSAdmin, self).save_model(request, obj, form, change)


class SiteAdmin(admin.ModelAdmin):

    def get_ECSlists(self, obj):
        return ', '.join([e.name for e in obj.ECSlists.all()])
    get_ECSlists.short_description = 'ECSs'

    def get_configfiles(self, obj):
        return ', '.join([c.filename for c in obj.configfiles.all()])
    get_configfiles.short_description = 'configfiles'

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
        ('site_info', {'fields': ['fullname', 'shortname', 'configdirname', 'ECSlists', 'configfiles', 'port', 'testpage', 'status', 'deployattention', 'devcharge']}),
    ]
    filter_horizontal = ('ECSlists', 'configfiles')

    list_display = ('fullname', 'deployattention', 'get_ECSlists', 'get_configfiles', 'status', 'modified_user', 'modified_time')
    list_filter = ['status', 'port']
    search_fields = ['fullname', 'port']
    actions = [make_sites_disable, make_sites_enable]

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(SiteAdmin, self).save_model(request, obj, form, change)


@admin.register(Configfile)
class ConfigfileAdmin(SimpleHistoryAdmin):
    fieldsets = [
        (None, {'fields': ['sitecluster', 'filename', 'content']}),
    ]
    list_display = ('sitecluster', 'filename', 'modified_user', 'modified_time')
    search_fields = ['sitecluster']
    
    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(ConfigfileAdmin, self).save_model(request, obj, form, change)


class DeployitemInline(admin.TabularInline):
    model = Deployitem
    extra = 0
    filter_horizontal = ('deploysite',)


class ApplyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['applyproject', 'confamendexplain', 'remarkexplain', 'apply_status']}),
    ]
    inlines = [DeployitemInline]
    list_display = ('applyproject', 'status', 'apply_user', 'apply_time', 'deploy_user', 'deploy_time')

    def save_model(self, request, obj, form, change):
        if obj.apply_user is None:
            obj.apply_user = request.user.username
            super(ApplyAdmin, self).save_model(request, obj, form, change)


admin.site.register(ECS, ECSAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Apply, ApplyAdmin)
