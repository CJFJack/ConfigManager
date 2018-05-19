# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Site, ECS, Configfile

#class ConfigfileInline(admin.TabularInline):
#    model = Configfile
#    extra = 0

class ECSAdmin(admin.ModelAdmin):
    fieldsets = [
        ('server_info',      {'fields': ['name']}),
        (None,               {'fields': ['instanceid']}),
        (None,               {'fields': ['IP']}),
        (None,               {'fields': ['status']}),
    ]

    list_display = ('name', 'instanceid', 'IP', 'status', 'modified_user', 'modified_time') 
    list_filter = ['name']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(ECSAdmin, self).save_model(request, obj, form, change)


class SiteAdmin(admin.ModelAdmin):

    def get_ECSlists(self, obj):
        return ', '.join([e.name for e in obj.ECSlists.all()])
    get_ECSlists.short_description = 'ECSs'
 
    fieldsets = [
        ('site_info', {'fields': ['fullname', 'shortname', 'configdirname', 'ECSlists', 'configfiles', 'port', 'testpage', 'status', 'deployattention', 'devcharge']}),
    ]
    #inlines = [ConfigfileInline]
    filter_horizontal = ('ECSlists', 'configfiles')

    list_display = ('fullname', 'get_ECSlists', 'deployattention', 'status', 'modified_time')
    list_filter = ['status', 'port']
    search_fields = ['fullname']

    def save_model(self, request, obj, form, change):
        obj.modified_user = request.user.username
        super(SiteAdmin, self).save_model(request, obj, form, change)


class ConfigfileAdmin(admin.ModelAdmin):
    list_display=('sitecluster', 'filename', 'modified_time')

admin.site.register(ECS, ECSAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Configfile, ConfigfileAdmin)
