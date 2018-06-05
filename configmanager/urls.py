from django.conf.urls import url
from . import views

app_name = 'configmanager'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ecs$', views.ECSListView.as_view(), name='ecslist'),
    url(r'^ecs/(?P<pk>[0-9]+)/change$', views.ECSChangeView.as_view(), name='ecschange'),
    url(r'^ecs/(?P<ecs_id>[0-9]+)/save/$', views.save, name='save'),
    url(r'^search-form$', views.search_form),
    url(r'^search$', views.search),
    url(r'^search-post$', views.search_form),
]
