from django.conf.urls import url
from . import views


app_name = 'configmanager'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecslist'),
    url(r'^ecs/(?P<pk>[0-9]+)/change/$', views.ECSChangeView.as_view(), name='ecschange'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/save/$', views.ecs_save, name='ecssave'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/enable/$', views.ecs_enable, name='ecsenable'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/disable/$', views.ecs_disable, name='ecsdisable'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/delete/$', views.ecs_delete, name='ecsdelete'),
    url(r'^ecs/add/$', views.ECSAddView.as_view(), name='ecsadd'),
    url(r'^ecs/addmethod/$', views.ecs_add, name='ecsaddmethod'),
]
