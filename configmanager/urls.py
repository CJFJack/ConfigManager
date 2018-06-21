from django.conf.urls import url
from . import views


app_name = 'configmanager'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^nav_top/$', views.nav_top, name='nav_top'),
    url(r'^deploymanager/$', views.deploymanager, name='deploymanager'),
    url(r'^systemmanager/$', views.systemmanager, name='systemmanager'),
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecslist'),
    url(r'^ecs/(?P<pk>[0-9]+)/change/$', views.ECSChangeView.as_view(), name='ecschange'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/save/$', views.ecs_save, name='ecssave'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/enable/$', views.ecs_enable, name='ecsenable'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/disable/$', views.ecs_disable, name='ecsdisable'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/delete/$', views.ecs_delete, name='ecsdelete'),
    url(r'^ecs/add/$', views.ECSAddView.as_view(), name='ecsadd'),
    url(r'^ecs/addmethod/$', views.ecs_add, name='ecsaddmethod'),
    url(r'^site/$', views.SiteListView.as_view(), name='sitelist'),
    url(r'^site/(?P<pk>[0-9]+)/change/$', views.SiteChangeView.as_view(), name='sitechange'),
    url(r'^site/(?P<site_id>[0-9]+)/save/$', views.site_save, name='sitesave'),
    url(r'^site/add/$', views.SiteAddView.as_view(), name='siteadd'),
    url(r'^site/addmethod/$', views.site_add, name='siteaddmethod'),
    url(r'^site/(?P<site_id>[0-9]+)/delete/$', views.site_delete, name='sitedelete'),
    url(r'^config/$', views.ConfigListView.as_view(), name='configlist'),
    url(r'^config/(?P<pk>[0-9]+)/change/$', views.ConfigChangeView.as_view(), name='configchange'),
    url(r'^config/(?P<configfile_id>[0-9]+)/save/$', views.config_save, name='configsave'),
    url(r'^config/(?P<release_id>[0-9]+)/deploy/$', views.config_deploy, name='configdeploy'),
]
