"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from apscheduler.schedulers.background import BackgroundScheduler
from configmanager import cron
import logging

urlpatterns = [
    url(r'^', include('configmanager.urls')),
    url(r'^configmanager/', include('configmanager.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]


scheduler = BackgroundScheduler()


@scheduler.scheduled_job("interval", seconds=300, id="job")
def my_schedule_task():
    cron.save_rds_info()
    print 'Update RDS Info'
    cron.get_rds_monitor()
    print 'get_rds_monitor'


scheduler.start()
