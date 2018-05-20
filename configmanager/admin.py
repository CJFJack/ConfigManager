# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import Site, ECS, Configfile


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
 
    fieldsets = [
        ('site_info', {'fields': ['fullname', 'shortname', 'configdirname', 'ECSlists', 'configfiles', 'port', 'testpage', 'status', 'deployattention', 'devcharge']}),
    ]
    filter_horizontal = ('ECSlists', 'configfiles')

    list_display = ('fullname',  'deployattention', 'get_ECSlists', 'get_configfiles', 'status', 'modified_user', 'modified_time')
    list_filter = ['status', 'port']
    search_fields = ['fullname']

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(SiteAdmin, self).save_model(request, obj, form, change)


@admin.register(Configfile)
class ConfigfileAdmin(SimpleHistoryAdmin):
    fieldsets = [
        (None, {'fields': ['sitecluster', 'filename', 'content']}),
    ]
    list_display=('sitecluster', 'filename', 'modified_user', 'modified_time')
    search_fields = ['sitecluster']
    
    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(ConfigfileAdmin, self).save_model(request, obj, form, change)

admin.site.register(ECS, ECSAdmin)
admin.site.register(Site, SiteAdmin)
