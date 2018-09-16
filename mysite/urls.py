# -*- coding: utf-8 -*-
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
from configmanager.views import LoginView
import logging


logging.basicConfig()

urlpatterns = [
    url(r'^', include('configmanager.urls')),
    url(r'^configmanager/', include('configmanager.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
]

scheduler = BackgroundScheduler()


@scheduler.scheduled_job("interval", seconds=600, id="get_rds_info")
def get_rds_info():
    cron.save_rds_info()
    print 'Update RDS Info'


@scheduler.scheduled_job("interval", seconds=300, id="get_rds_monitor")
def get_rds_monitor():
    cron.get_rds_monitor()
    print 'get_rds_monitor'


@scheduler.scheduled_job("interval", seconds=500, id="get_alram_history")
def get_alram_history():
    cron.get_alram_history_list()
    print 'get_alarm_history'


@scheduler.scheduled_job("interval", seconds=400, id="get_ecs_resource")
def get_ecs_resource():
    cron.get_ecs_resource()
    print 'get_ecs_resource'


scheduler.start()
