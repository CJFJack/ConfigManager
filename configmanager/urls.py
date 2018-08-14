# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


app_name = 'configmanager'

urlpatterns = [
    # 主体页面
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    # ECS页面
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecslist'),
    url(r'^ecs/(?P<pk>[0-9]+)/change/$', views.ECSChangeView.as_view(), name='ecschange'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/save/$', views.ecs_save, name='ecssave'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/enable/$', views.ecs_enable, name='ecsenable'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/disable/$', views.ecs_disable, name='ecsdisable'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/delete/$', views.ecs_delete, name='ecsdelete'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/updatemonitor/$', views.update_ecs_monitor, name='updatemonitor'),
    url(r'^ecs/updateallmonitor/$', views.update_allecs_monitor, name='updateallmonitor'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/updateinfo/$', views.update_ecs_info, name='updateinfo'),
    url(r'^ecs/updateallinfo/$', views.update_allecs_info, name='updateallinfo'),
    url(r'^ecs/syncallecsinfo/$', views.sync_all_ecs_info, name='syncallecsinfo'),
    url(r'^ecs/addmethod/$', views.ecs_add, name='ecsaddmethod'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/partrefresh/$', views.ecs_part_refresh, name='ecspartrefresh'),
    url(r'^ecs/wholerefresh/$', views.ecs_whole_refresh, name='ecswholerefresh'),
    # Site页面
    url(r'^site/$', views.SiteListView.as_view(), name='sitelist'),
    url(r'^site/(?P<pk>[0-9]+)/change/$', views.SiteChangeView.as_view(), name='sitechange'),
    url(r'^site/(?P<site_id>[0-9]+)/save/$', views.site_save, name='sitesave'),
    url(r'^site/add/$', views.SiteAddView.as_view(), name='siteadd'),
    url(r'^site/addmethod/$', views.site_add, name='siteaddmethod'),
    url(r'^site/(?P<site_id>[0-9]+)/delete/$', views.site_delete, name='sitedelete'),
    url(r'^site/wholerefresh/$', views.site_whole_refresh, name='sitewholerefresh'),
    # 站点族页面
    url(r'^race/$', views.RaceListView.as_view(), name='racelist'),
    url(r'^race/add/$', views.race_add, name='raceadd'),
    url(r'^race/(?P<race_id>[0-9]+)/delete/$', views.race_delete, name='racedelete'),
    url(r'^race/(?P<pk>[0-9]+)/change/$', views.RaceEditView.as_view(), name='raceedit'),
    url(r'^race/(?P<race_id>[0-9]+)/siterelations/$', views.race_site_relation, name='racesiterelation'),
    url(r'^race/wholerefresh/$', views.race_wholerefresh, name='racewholerefresh'),
    # Config页面
    url(r'^config/$', views.ConfigListView.as_view(), name='configlist'),
    url(r'^undeployconfig/$', views.UndeployConfigListView.as_view(), name='undeployconfiglist'),
    url(r'^config/(?P<pk>[0-9]+)/change/$', views.ConfigChangeView.as_view(), name='configchange'),
    url(r'^config/(?P<configfile_id>[0-9]+)/save/$', views.config_save, name='configsave'),
    url(r'^config/(?P<release_id>[0-9]+)/deploy/$', views.config_deploy, name='configdeploy'),
    url(r'^config/(?P<configfile_id>[0-9]+)/history/$', views.config_history, name='confighistory'),
    url(r'^config/(?P<pk>[0-9]+)/historydetail/$', views.ConfigHistoryDetailView.as_view(), name='confighistorydetail'),
    url(r'^config/(?P<confighistorydetail_id>[0-9]+)/rollback/$', views.config_rollback, name='configrollback'),
    url(r'^config/(?P<deployecs_id>[0-9]+)/deploy/(?P<release_id>[0-9]+)/$', views.apply_config_deploy, name='applyconfigdeploy'),
    url(r'^config/(?P<site_id>[0-9]+)/slbpartrefresh/$', views.config_slb_part_refresh, name='configslbrefresh'),
    url(r'^config/(?P<site_id>[0-9]+)/ecspartrefresh/$', views.config_ecs_part_refresh, name='configecsrefresh'),
    # Apply页面
    url(r'^apply/$', views.ApplyListView.as_view(), name='applylist'),
    url(r'^undeployapply/$', views.UndeployApplyListView.as_view(), name='undeployapplylist'),
    url(r'^apply/add$', views.ApplyAdd.as_view(), name='applyadd'),
    url(r'^apply/(?P<pk>[0-9]+)/change/$', views.ApplyChangeView.as_view(), name='applychange'),
    url(r'^apply/(?P<apply_id>[0-9]+)/statuschange/$', views.apply_status_change, name='applystatuschange'),
    url(r'^apply/(?P<apply_id>[0-9]+)/delete/$', views.apply_delete, name='applydelete'),
    url(r'^apply/(?P<pk>[0-9]+)/deploysitelist/$', views.DeploySiteView.as_view(), name='deploysitelist'),
    url(r'^apply/(?P<site_id>[0-9]+)/partrefresh/$', views.apply_part_refresh, name='applypartrefresh'),
    # SLB页面
    url(r'^slb/$', views.SLBListView.as_view(), name='slblist'),
    url(r'^slb/allinfoupdate/$', views.all_slb_info_update, name='allslbinfoupdate'),
    url(r'^slb/(?P<pk>[0-9]+)/detail/$', views.SLBDetailView.as_view(), name='slbdetail'),
    url(r'^slb/(?P<slb_id>[0-9]+)/slbrelasite/$', views.slb_rela_site, name='slbrelasite'),
    url(r'^slb/(?P<slb_id>[0-9]+)/slbhealthupdate/$', views.slb_health_update, name='slbhealthupdate'),
    url(r'^slb/(?P<site_id>[0-9]+)/moreslbhealthupdate/$', views.more_slb_health_update, name='moreslbhealthupdate'),
    url(r'^slb/allslbhealthupdate/$', views.all_slb_health_update, name='allslbhealthupdate'),
    url(r'^slb/(?P<slb_id>[0-9]+)/removebackendserver/(?P<server_id>[0-9]+)/$', views.remove_backend_server, name='removebackendserver'),
    url(r'^slb/(?P<slb_id>[0-9]+)/addbackendserver/(?P<server_id>[0-9]+)/$', views.add_backend_server, name='addbackendserver'),
    url(r'^slb/(?P<site_id>[0-9]+)/siteremovebackendserver/(?P<server_id>[0-9]+)/$', views.site_remove_backend_server, name='siteremovebackendserver'),
    url(r'^slb/(?P<site_id>[0-9]+)/siteaddbackendserver/(?P<server_id>[0-9]+)/$', views.site_add_backend_server, name='siteaddbackendserver'),
    url(r'^slb/(?P<slb_id>[0-9]+)/partrefresh/$', views.slb_part_refresh, name='slbpartrefresh'),
    url(r'^slb/wholerefresh/$', views.slb_whole_refresh, name='slbwholerefresh'),
]
