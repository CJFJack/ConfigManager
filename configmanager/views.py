# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.core.files import File
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login

# Create your views here.

from time import time
from .models import ECS, Site, Configfile, Siterace, Release, ConfigmanagerHistoricalconfigfile, Apply, Deployitem, SLB, \
    SLBhealthstatus, DeployECS, RDS_Usage_Record, Alarm_History
from .forms import ApplyForm, DeployitemFormSet, SLBForm, SLBsiteFormSet, LoginForm
from configmanager.acs_api.acs_ecs_monitor import query_ecs_api
from acs_api.acs_ecs_info import query_ecs_info
from configmanager.acs_api.acs_slb_info import query_slb_info
from configmanager.acs_api.acs_slb_health import query_slb_health
from configmanager.acs_api.acs_slb_backendserver_remove import remove_backendserver
from configmanager.acs_api.acs_slb_backendserver_add import add_backendserver
from configmanager.acs_api.acs_all_ecs_info import query_all_ecs
import os, json, time, datetime

app_name = 'configmanager'


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, "configmanager/login.html", {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next', '/') or '/')
            else:
                return render(request, "configmanager/login.html", {'messages': u'用户名或密码错误！', 'login_form': login_form})
        else:
            return render(request, "configmanager/login.html", {'login_form': login_form})


@login_required(login_url='/login/')
def index(request):
    context = {}

    # 默认rds-line图横坐标间隔
    context['rds_range_default'] = u'1小时'
    # 选择rds-line图横坐标间隔
    if request.method == 'POST':
        range = request.POST['select_range']
        if range == u'1小时':
            select_count = 12
        if range == u'6小时':
            select_count = 72
        if range == u'12小时':
            select_count = 144
        if range == u'1天':
            select_count = 288
        if range == u'3天':
            select_count = 864
        if range == u'7天':
            select_count = 2016
        if range == u'14天':
            select_count = 4032
        context['rds_range_default'] = range

    return render(request, "configmanager/index.html", context)


@login_required(login_url='/login/')
def index_rds_cpu_pie(request):
    # 获取最近一次rds资源
    last_rds_resource = RDS_Usage_Record.objects.order_by('-add_time')[:1]
    # 获取最近一次rds资源cpu使用率
    try:
        last_rds_cpu = [q.cpu_usage for q in last_rds_resource][0]
    except Exception, e:
        print e

    return HttpResponse(json.dumps({'success': True, 'last_rds_cpu': last_rds_cpu}), content_type="application/json")


@login_required(login_url='/login/')
def index_rds_io_pie(request):
    # 获取最近一次rds资源
    last_rds_resource = RDS_Usage_Record.objects.order_by('-add_time')[:1]
    # 获取最近一次rds资源IO使用率
    try:
        last_rds_io = [q.io_usage for q in last_rds_resource][0]
    except Exception, e:
        print e

    return HttpResponse(json.dumps({'success': True, 'last_rds_io': last_rds_io}), content_type="application/json")


@login_required(login_url='/login/')
def index_rds_disk_pie(request):
    # 获取最近一次rds资源
    last_rds_resource = RDS_Usage_Record.objects.order_by('-add_time')[:1]
    # 获取最近一次rds资源IO使用率
    try:
        last_rds_disk = [q.disk_usage for q in last_rds_resource][0]
    except Exception, e:
        print e

    return HttpResponse(json.dumps({'success': True, 'last_rds_disk': last_rds_disk}), content_type="application/json")


@login_required(login_url='/login/')
def index_rds_line(request):
    # 默认横坐标间隔
    select_count = 12
    range = request.POST['select_range']
    if range == u'1小时':
        select_count = 12
    if range == u'6小时':
        select_count = 72
    if range == u'12小时':
        select_count = 144
    if range == u'1天':
        select_count = 288
    if range == u'3天':
        select_count = 864
    if range == u'7天':
        select_count = 2016
    if range == u'14天':
        select_count = 4032

    # 获取最近12次rds资源, 默认5分钟为间隔
    recently_rds_resource = RDS_Usage_Record.objects.order_by('-add_time')[:select_count]
    # 获取最近12次add_time的list
    add_time_list = [q.add_time.strftime('%Y-%m-%d %H:%M') for q in recently_rds_resource]
    add_time_list.sort()
    add_time = add_time_list
    # 获取最近12次rds的CPU使用率list
    recently_rds_cpu = [q.cpu_usage for q in recently_rds_resource]
    recently_rds_cpu.reverse()
    # 获取最近12次rds的I/O使用率list
    recently_rds_io = [q.io_usage for q in recently_rds_resource]
    recently_rds_io.reverse()
    # 获取最近12次rds的disk使用率list
    recently_rds_disk = [q.disk_usage for q in recently_rds_resource]
    recently_rds_disk.reverse()

    return HttpResponse(json.dumps({'success': True, 'add_time': add_time,
                                    'recently_rds_cpu': recently_rds_cpu, 'recently_rds_io': recently_rds_io,
                                    'recently_rds_disk': recently_rds_disk}), content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_product_type_pie(request):
    # 按alarm产品类型统计（默认为最近30天）
    now = datetime.datetime.now()
    ever = now - datetime.timedelta(days=30)
    alarm = Alarm_History.objects.filter(alarm_time__gt=ever).values('namespace').annotate(Count("id"))
    product_type_list = []
    for i in alarm:
        product_type_list.append(str(i['namespace']))
    product_type_alarm_list = []
    for i in alarm:
        product_type_dict = {}
        product_type_dict[str('value')] = i['id__count']
        product_type_dict[str('name')] = str(i['namespace'])
        product_type_alarm_list.append(product_type_dict)
    return HttpResponse(json.dumps({'success': True, 'product_type_list': product_type_list,
                                    'product_type_alarm_list': product_type_alarm_list}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_metric_type_pie(request):
    # 按alarm监控项类型统计（默认为最近30天）
    now = datetime.datetime.now()
    ever = now - datetime.timedelta(days=30)
    alarm = Alarm_History.objects.filter(alarm_time__gt=ever).values('metric_name').annotate(Count("id"))
    metric_type_list = []
    for i in alarm:
        metric_type_list.append(str(i['metric_name']))
    metric_type_alarm_list = []
    for i in alarm:
        metric_type_dict = {}
        metric_type_dict[str('value')] = i['id__count']
        metric_type_dict[str('name')] = str(i['metric_name'])
        metric_type_alarm_list.append(metric_type_dict)
    return HttpResponse(json.dumps({'success': True, 'metric_type_list': metric_type_list,
                                    'metric_type_alarm_list': metric_type_alarm_list}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_instance_pie(request):
    # 按alarm实例比例统计（默认为最近30天）
    now = datetime.datetime.now()
    ever = now - datetime.timedelta(days=30)
    alarm = Alarm_History.objects.filter(alarm_time__gt=ever).values('instance_name').annotate(Count("id"))
    instance_list = []
    for i in alarm:
        instance_list.append(i['instance_name'])
    instance_alarm_list = []
    for i in alarm:
        instance_dict = {}
        instance_dict['value'] = i['id__count']
        instance_dict['name'] = i['instance_name']
        instance_alarm_list.append(instance_dict)
    return HttpResponse(json.dumps({'success': True, 'instance_list': instance_list,
                                    'instance_alarm_list': instance_alarm_list}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_line(request):
    start = str(datetime.datetime.now())[:4] + '-01-01'
    end = str(datetime.datetime.now())[:4] + '-12-31'
    alarm = Alarm_History.objects.filter(alarm_time__gt=start).filter(alarm_time__lt=end). \
        extra(select={'month': 'month(alarm_time)'}).values('month').annotate(number=Count('id'))
    alarm_num_x = []
    alarm_num_y = []
    this_year = str(datetime.datetime.now())[:4]
    for m in xrange(1, 13):
        this_date = this_year + '-' + str(m)
        alarm_num_x.append(this_date)
    for m in xrange(1, 13):
        try:
            dict_index = [int(a['month']) for a in alarm].index(m)
        except Exception, e:
            alarm_num_y.append(0)
            print e
        else:
            alarm_num_y.append([a for a in alarm][dict_index]['number'])

    return HttpResponse(json.dumps({'success': True, 'alarm_num_x': alarm_num_x, 'alarm_num_y': alarm_num_y}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_ecs_cpu_pie(request):
    ecs_cpu_average = ECS.objects.aggregate(Avg('recently_cpu'))
    ecs_cpu_average = ecs_cpu_average['recently_cpu__avg']
    ecs_cpu_average = '%.2f' % ecs_cpu_average
    return HttpResponse(json.dumps({'success': True, 'ecs_cpu_average': ecs_cpu_average}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_ecs_memory_pie(request):
    ecs_memory_average = ECS.objects.aggregate(Avg('recently_memory'))
    ecs_memory_average = ecs_memory_average['recently_memory__avg']
    ecs_memory_average = '%.2f' % ecs_memory_average
    return HttpResponse(json.dumps({'success': True, 'ecs_memory_average': ecs_memory_average}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_ecs_disk_pie(request):
    ecs_disk_average = ECS.objects.aggregate(Avg('recently_diskusage'))
    ecs_disk_average = ecs_disk_average['recently_diskusage__avg']
    ecs_disk_average = '%.2f' % ecs_disk_average
    return HttpResponse(json.dumps({'success': True, 'ecs_disk_average': ecs_disk_average}),
                        content_type="application/json")


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSListView(generic.ListView):
    model = ECS
    template_name = 'configmanager/ecs_list.html'
    context_object_name = 'ECS_list'
    paginator_class = SafePaginator
    paginate_by = 10

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            ECS_list = ECS.objects.filter(
                Q(name__icontains=q) |
                Q(IP__icontains=q) |
                Q(instanceid__icontains=q)).order_by('name')
        else:
            ECS_list = ECS.objects.order_by('name')
        return ECS_list

    def get_context_data(self, **kwargs):
        context = super(ECSListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSChangeView(generic.DetailView):
    model = ECS
    template_name = 'configmanager/ecs_change.html'


@login_required(login_url='/login/')
def ecs_save(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.instanceid = request.POST['instanceid']
    ecs.status = request.POST['status']
    ecs.modified_user = request.user.username
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def ecs_enable(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.status = 'Y'
    ecs.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def ecs_disable(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.status = 'N'
    ecs.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def ecs_delete(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.delete()
    messages.success(request, '成功！删除ECS ' + ecs.name)
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def ecs_add(request):
    if request.POST.has_key('ecs-add'):
        instanceid = request.POST['instanceid']
        ecs = ECS(instanceid=instanceid)
        ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def update_ecs_monitor(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    instanceid = ecs.instanceid.encode('utf-8')
    try:
        recently_cpu = query_ecs_api(instanceid=instanceid, metric="cpu_total")
        recently_mem = query_ecs_api(instanceid=instanceid, metric="memory_usedutilization")
        recently_diskusage = query_ecs_api(instanceid=instanceid, metric="diskusage_utilization")
    except:
        pass
    else:
        ecs.recently_memory = recently_mem['Average']
        ecs.recently_cpu = recently_cpu['Average']
        ecs.recently_diskusage = recently_diskusage['Average']
        ecs.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def update_allecs_monitor(request):
    for ecs in ECS.objects.all():
        update_ecs_monitor(request, ecs.id)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def update_ecs_info(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    instanceid = ecs.instanceid.encode('utf-8')
    try:
        result = query_ecs_info(instanceids=[instanceid])
    except:
        pass
    else:
        ecs.instancestatus = result['Status']
        ecs.IP = result['InnerIpAddress']
        ecs.publicipaddress = result['PublicIpAddress']
        ecs.regionId = result['RegionId']
        ecs.osname = result['OSName']
        ecs.expiredtime = result['ExpiredTime']
        ecs.memory = result['Memory'] / 1024
        ecs.ostype = result['OSType']
        ecs.networktype = result['NetworkType']
        ecs.name = result['InstanceName']
        ecs.cpu = result['Cpu']
        ecs.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def sync_all_ecs_info(request):
    ecs_aliyun = query_all_ecs(RegionId='cn-hangzhou')
    ecs_local = []
    '''获取本地所有ecs实例id的list'''
    for ecs in ECS.objects.all():
        ecs_local.append(ecs.instanceid)
    '''增加本地没有的ecs'''
    for ecsinstanceid in ecs_aliyun:
        if ecsinstanceid not in ecs_local:
            ecs = ECS(instanceid=ecsinstanceid)
            ecs.save()
    '''删除阿里云没有的本地ecs'''
    for ecsinstanceid in ecs_local:
        if ecsinstanceid not in ecs_aliyun:
            ecs = get_object_or_404(ECS, instanceid=ecsinstanceid)
            ecs.delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def update_allecs_info(request):
    for ecs in ECS.objects.all():
        update_ecs_info(request, ecs.id)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteListView(generic.ListView):
    template_name = 'configmanager/site_list.html'
    context_object_name = 'Site_list'
    paginator_class = SafePaginator
    paginate_by = 10

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            Site_list = Site.objects.filter(Q(fullname__icontains=q) |
                                            Q(shortname__icontains=q) |
                                            Q(port__icontains=q)).order_by('fullname')
        else:
            Site_list = Site.objects.order_by('fullname')
        return Site_list

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        context['configfile'] = Site.configfile_set
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteChangeView(generic.DetailView):
    model = Site
    template_name = 'configmanager/site_change.html'

    def get_context_data(self, **kwargs):
        context = super(SiteChangeView, self).get_context_data(**kwargs)
        configfiles = Site.configfile_set
        ECSs = ECS.objects.all()
        Sites = Site.objects.all()
        Siteraces = Siterace.objects.all()
        context['configfiles'] = configfiles
        context['ECSs'] = ECSs
        context['Sites'] = Sites
        context['Siteraces'] = Siteraces
        return context


@login_required(login_url='/login/')
def add_relation_ecs(request, site):
    for key in request.POST:
        value_list = request.POST.getlist(key)
        for v in value_list:
            try:
                e = ECS.objects.get(name=v)
            except:
                pass
            else:
                site.ECSlists.add(e)


@login_required(login_url='/login/')
def site_save(request, site_id):
    if request.POST.has_key('site-save'):
        s = get_object_or_404(Site, pk=site_id)
        s.fullname = request.POST['fullname']
        s.shortname = request.POST['shortname']
        s.configdirname = request.POST['configdirname']
        s.port = request.POST['port']
        s.testpage = request.POST['testpage']
        s.status = request.POST['status']
        s.devcharge = request.POST['devcharge']
        s.deployattention = request.POST['deployattention']
        s.modified_user = request.user.username

        '''修改所属站点族'''
        try:
            s.siterace_id = request.POST['select_race']
        except:
            s.siterace_id = '99999'
        s.save()

        '''新增或删除关联配置文件'''
        post_filenames = request.POST['configfiles']
        post_filenames_list = post_filenames.split(';')
        s.update_configfiles(post_filenames_list=post_filenames_list)

        ''''增加所属ECS'''
        add_relation_ecs(request=request, site=s)

        '''减少所属ECS'''
        for key in request.POST:
            if key == 'select_ecs[]':
                value_list = request.POST.getlist(key)
        for es in s.ECSlists.all():
            if es.name not in value_list:
                s.ECSlists.remove(es)

        messages.success(request, "成功！修改站点 <a href=\'/site/" + str(site_id) + "/change/\'>" + s.fullname + "</a>")
        return HttpResponseRedirect(reverse('configmanager:sitelist'))

    if request.POST.has_key('site-goback'):
        return HttpResponseRedirect(reverse('configmanager:sitelist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteAddView(generic.ListView):
    model = Site
    template_name = 'configmanager/site_add.html'

    def get_context_data(self, **kwargs):
        context = super(SiteAddView, self).get_context_data(**kwargs)
        ECSs = ECS.objects.all()
        Siteraces = Siterace.objects.all()
        context['ECSs'] = ECSs
        context['Siteraces'] = Siteraces
        return context


@login_required(login_url='/login/')
def site_add(request):
    if request.POST.has_key('site-add') or request.POST.has_key('site-add-continue-add'):
        '''保存站点基础信息'''
        fullname = request.POST['fullname']
        shortname = request.POST['shortname']
        configdirname = request.POST['configdirname']
        if request.POST['port']:
            port = request.POST['port']
        else:
            port = 0
        testpage = request.POST['testpage']
        status = request.POST['status']
        devcharge = request.POST['devcharge']
        deployattention = request.POST['deployattention']
        try:
            siterace_id = request.POST['optionsRadios']
        except:
            siterace_id = '99999'
        modified_user = request.user.username
        site = Site(fullname=fullname, shortname=shortname, configdirname=configdirname, port=port, testpage=testpage,
                    status=status, devcharge=devcharge, deployattention=deployattention, modified_user=modified_user,
                    siterace_id=siterace_id)
        site.save()
        '''添加关联ECS'''
        add_relation_ecs(request, site)

        '''新增或删除关联配置文件'''
        post_filenames_list = []
        post_filenames = request.POST['configfiles']
        post_filenames_list = post_filenames.split(';')
        site.update_configfiles(post_filenames_list=post_filenames_list)
        if request.POST.has_key('site-add-continue-add'):
            ECSs = ECS.objects.all()
            Siteraces = Siterace.objects.all()
            return render(request, 'configmanager/site_add.html', {'ECSs': ECSs, 'Siteraces': Siteraces})
        if request.POST.has_key('site-add'):
            messages.success(request, "成功！添加站点 " + fullname)
            return HttpResponseRedirect(reverse('configmanager:sitelist'))
    else:
        return HttpResponseRedirect(reverse('configmanager:sitelist'))


@login_required(login_url='/login/')
def site_delete(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    site.delete()
    return HttpResponseRedirect(reverse('configmanager:sitelist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RaceListView(generic.ListView):
    template_name = 'configmanager/race_list.html'
    context_object_name = 'Race_list'
    paginate_by = 5

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            Race_list = Siterace.objects.filter(Q(alias__icontains=q)).order_by('raceid')
        else:
            Race_list = Siterace.objects.order_by('raceid')
        return Race_list

    def get_context_data(self, **kwargs):
        context = super(RaceListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RaceEditView(generic.DetailView):
    model = Siterace
    template_name = 'configmanager/race_edit.html'

    def get_context_data(self, **kwargs):
        context = super(RaceEditView, self).get_context_data(**kwargs)
        site_list = Site.objects.all()
        context['site_list'] = site_list
        return context


@login_required(login_url='/login/')
def race_add(request):
    randomraceid = int(round(time.time() * 1000))
    print randomraceid
    siterace = Siterace(raceid=randomraceid)
    siterace.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def race_delete(request, race_id):
    siterace = Siterace(id=race_id)
    siterace.delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def race_site_relation(request, race_id):
    if request.POST.has_key('save'):
        race = Siterace.objects.get(pk=race_id)
        for site in race.site_set.all():
            site.siterace_id = 99999
            site.save()
        race.alias = request.POST['alias']
        race.save()
        for key in request.POST:
            try:
                site = Site.objects.get(fullname=key)
            except:
                pass
            else:
                site.siterace_id = race_id
                site.save()
        messages.success(request, "成功！修改 <a href=\'/race/" + str(race_id) + "/change/\'>" + race.alias + "</a>")
    return HttpResponseRedirect(reverse('configmanager:racelist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigListView(generic.ListView):
    model = Site
    template_name = 'configmanager/config_list.html'
    paginate_by = 5

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            Site_list = Site.objects.filter(Q(fullname__icontains=q) |
                                            Q(shortname__icontains=q) |
                                            Q(port__icontains=q)).filter(status='Y').order_by('fullname')
        else:
            Site_list = Site.objects.filter(status='Y').order_by('fullname')
        return Site_list

    def get_context_data(self, **kwargs):
        context = super(ConfigListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UndeployConfigListView(generic.ListView):
    model = Site
    template_name = 'configmanager/config_list.html'
    context_object_name = 'site_list'
    paginate_by = 5

    def get_queryset(self):
        L = []
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            for site in Site.objects.filter(Q(fullname__icontains=q) |
                                            Q(shortname__icontains=q) |
                                            Q(port__icontains=q)).order_by('fullname'):
                if site.have_undeploy_config_or_not():
                    L.append(site)
        else:
            for site in Site.objects.all():
                if site.have_undeploy_config_or_not():
                    L.append(site)
        return L

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigChangeView(generic.DetailView):
    model = Configfile
    template_name = 'configmanager/config_change.html'


@login_required(login_url='/login/')
def config_save(request, configfile_id):
    if request.POST.has_key('config-save'):
        '''保存配置函数'''

        def relation_config_save(request, configfileid):
            '''保存基本配置信息'''
            c = get_object_or_404(Configfile, pk=configfileid)
            c.content = request.POST['configcontent']
            c.modified_user = request.user.username
            c.save()
            siteid = c.site.id
            '''更新release状态为待发布u"N"'''
            for ecs in c.site.ECSlists.all():
                ecsid = ecs.id
                r = Release.objects.filter(site_id=siteid).filter(ECS_id=ecsid)
                if not r:
                    r = Release(site_id=siteid, ECS_id=ecsid)
                    r.save()
                else:
                    r = Release.objects.get(site_id=siteid, ECS_id=ecsid)
                    r.status = 'N'
                    r.save()

        '''保存配置内容'''
        c = get_object_or_404(Configfile, pk=configfile_id)
        for key in request.POST:
            try:
                s = Site.objects.get(fullname=key)
            except:
                pass
            else:
                for p_c in s.configfile_set.all():
                    if p_c.filename == c.filename:
                        relation_config_save(request, configfileid=p_c.id)
        return HttpResponseRedirect(reverse('configmanager:configlist'))

    if request.POST.has_key('config-goback'):
        return HttpResponseRedirect(reverse('configmanager:configlist'))


@login_required(login_url='/login/')
def config_deploy(request, release_id):
    '''更新Release表信息'''
    r = Release.objects.get(pk=release_id)
    r.status = 'Y'
    r.modified_user = request.user.username
    r.save()
    '''获取发布配置文件存放目录'''
    deploy_dir_path = settings.DEPLOY_DIR_PATH
    '''生成配置文件'''
    ecs = r.ECS.name
    config_path = os.path.join(deploy_dir_path, r.site.fullname, ecs, 'releaseconfig')
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    for c in r.site.configfile_set.all():
        file_name = os.path.join(config_path, c.filename)
        with open(file_name, 'w') as f:
            myfile = File(f)
            myfile.write(str(c.content))
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def apply_config_deploy(request, deployecs_id, release_id):
    d = get_object_or_404(DeployECS, pk=deployecs_id)
    d.ECSdeploystatus = 'Y'
    d.save()
    r = get_object_or_404(Release, pk=release_id)
    if r.status == 'Y':
        pass
    else:
        config_deploy(request, release_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def config_history(request, configfile_id):
    confighistory_list = ConfigmanagerHistoricalconfigfile.objects.filter(id=configfile_id).order_by('-modified_time')
    template_name = 'configmanager/config_history.html'
    return render(request, template_name, {'confighistory_list': confighistory_list})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigHistoryDetailView(generic.DetailView):
    model = ConfigmanagerHistoricalconfigfile
    template_name = 'configmanager/config_history_detail.html'
    context_object_name = 'confighistorydetail'


@login_required(login_url='/login/')
def config_rollback(request, confighistorydetail_id):
    ch = ConfigmanagerHistoricalconfigfile.objects.get(pk=confighistorydetail_id)
    configfileid = ch.id
    if request.POST.has_key('config-rollback'):
        # 回滚配置文件
        rollbackcontent = ch.content
        c = Configfile.objects.get(pk=configfileid)
        c.content = rollbackcontent
        c.save()
        # 更新配置发布状态为未发布
        for r in c.site.release_set.all():
            r.status = 'N'
            r.save()
        # 返回页面提示信息
        messages.success(request, "成功！回滚站点 " + ch.get_site_fullname() + " 配置文件 " + ch.filename + " 修改编号："
                         + confighistorydetail_id)
        return HttpResponseRedirect(reverse('configmanager:configlist'))
    if request.POST.has_key('config-goback'):
        return HttpResponseRedirect(reverse('configmanager:confighistory', args=(configfileid,)))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplyListView(generic.ListView):
    model = Apply
    template_name = 'configmanager/Apply_list.html'
    paginate_by = 10

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        print q
        if (q != ''):
            apply_list = Apply.objects.filter(Q(applyproject__icontains=q)).order_by('-apply_time')
        else:
            apply_list = Apply.objects.order_by('-apply_time')
        return apply_list

    def get_context_data(self, **kwargs):
        context = super(ApplyListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UndeployApplyListView(generic.ListView):
    template_name = 'configmanager/apply_list.html'
    context_object_name = 'apply_list'
    paginate_by = 10

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            apply_list = Apply.objects.filter(Q(applyproject__icontains=q)).filter(status='WD').order_by(
                '-wishdeploy_time').order_by('-apply_time')
        else:
            apply_list = Apply.objects.filter(status='WD').order_by('-wishdeploy_time').order_by('-apply_time')
        return apply_list

    def get_context_data(self, **kwargs):
        context = super(UndeployApplyListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplyChangeView(UpdateView):
    model = Apply
    form_class = ApplyForm
    template_name = 'configmanager/apply_change.html'

    def get_context_data(self, **kwargs):
        context = super(ApplyChangeView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['apply_form'] = ApplyForm(self.request.POST, instance=self.object)
            context['deployitem_form'] = DeployitemFormSet(self.request.POST)
        else:
            context['apply_form'] = ApplyForm(instance=self.object)
            context['deployitem_form'] = DeployitemFormSet(instance=self.object)
        return context


@login_required(login_url='/login/')
def apply_save(request, obj):
    try:
        if request.POST['wishdeploy_time']:
            obj.wishdeploy_time = request.POST['wishdeploy_time']
        obj.confamendexplain = request.POST['confamendexplain']
        obj.remarkexplain = request.POST['remarkexplain']
    except:
        pass
    else:
        obj.save()
    if request.method == 'POST':
        formset = DeployitemFormSet(request.POST, request.FILES, instance=obj)
        if formset.is_valid():
            formset.save()


@login_required(login_url='/login/')
def apply_status_change(request, apply_id):
    a = get_object_or_404(Apply, pk=apply_id)
    if a.status == 'WC':
        if request.POST.has_key('apply-save'):
            apply_save(request, a)
            a.applyoperatelog_set.create(type='保存', OperatorName=request.user.username, OperationTime=timezone.now())
        if request.POST.has_key('apply-commit'):
            a.status = 'DA'
            apply_save(request, a)
            a.applyoperatelog_set.create(type='保存并提交', OperatorName=request.user.username, OperationTime=timezone.now())
        if request.POST.has_key('apply-cancel'):
            a.status = 'C'
            a.save()
            a.applyoperatelog_set.create(type='取消', OperatorName=request.user.username, OperationTime=timezone.now())
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'DA':
        if request.POST.has_key('dev-approval'):
            a.status = 'TA'
            a.save()
            a.applyoperatelog_set.create(type='研发经理审核通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        if request.POST.has_key('dev-unapproval'):
            a.status = 'WC'
            a.save()
            a.applyoperatelog_set.create(type='研发经理审核不通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'TA':
        if request.POST.has_key('test-approval'):
            a.status = 'EA'
            a.save()
            a.applyoperatelog_set.create(type='测试经理审核通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        if request.POST.has_key('test-unapproval'):
            a.status = 'WC'
            a.save()
            a.applyoperatelog_set.create(type='测试经理审核不通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'EA':
        if request.POST.has_key('EA-approval'):
            a.status = 'OA'
            a.save()
            a.applyoperatelog_set.create(type='运维工程师审核通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        if request.POST.has_key('EA-unapproval'):
            a.status = 'WC'
            a.save()
            a.applyoperatelog_set.create(type='运维工程师审核不通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'OA':
        if request.POST.has_key('OA-approval'):
            a.status = 'TDA'
            a.save()
            a.applyoperatelog_set.create(type='运维经理审核通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        if request.POST.has_key('OA-unapproval'):
            a.status = 'WC'
            a.save()
            a.applyoperatelog_set.create(type='运维经理审核不通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'TDA':
        if request.POST.has_key('TDA-approval'):
            a.status = 'WD'
            a.save()
            a.applyoperatelog_set.create(type='技术总监审核通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        if request.POST.has_key('TDA-unapproval'):
            a.status = 'WC'
            a.save()
            a.applyoperatelog_set.create(type='技术总监审核不通过', OperatorName=request.user.username,
                                         OperationTime=timezone.now())
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'WD':
        if request.POST.has_key('deploy-finish'):
            a.status = 'D'
            a.deploy_user = request.user.username
            a.deploy_time = datetime.now()
            a.save()
            a.applyoperatelog_set.create(type='已发布', OperatorName=request.user.username, OperationTime=timezone.now())
        if request.POST.has_key('goto-deploy'):
            return HttpResponseRedirect(reverse('configmanager:deploysitelist', args=(a.id,)))
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    return HttpResponseRedirect(reverse('configmanager:applylist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplyAdd(CreateView):
    model = Apply
    fields = ('applyproject', 'wishdeploy_time', 'confamendexplain', 'remarkexplain')
    template_name = 'configmanager/apply_create.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        deployitem_form = DeployitemFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, deployitem_form=deployitem_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        apply_form = self.get_form(form_class)
        deployitem_form = DeployitemFormSet(self.request.POST)
        if (apply_form.is_valid() or deployitem_form.is_valid()):
            messages.success(request, "成功！创建发布申请单")
            return self.form_valid(apply_form, deployitem_form)
        else:
            return self.form_invalid(apply_form, deployitem_form)

    def form_valid(self, apply_form, deployitem_form):
        apply_form.instance.apply_user = self.request.user
        self.object = apply_form.save()
        deployitem_form.instance = self.object
        for form in deployitem_form:
            try:
                site_id = form.cleaned_data['deploysite'].id
            except:
                pass
            else:
                for ecs in form.cleaned_data['deploysite'].ECSlists.all():
                    ecs_id = ecs.id
                    d = DeployECS(applyproject_id=apply_form.instance.id, ECS_id=ecs_id, site_id=site_id)
                    d.save()
                deployitem_form.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))

    def form_invalid(self, apply_form, deployitem_form):
        return self.render_to_response(
            self.get_context_data(apply_form=apply_form, deployitem_form=deployitem_form))


@login_required(login_url='/login/')
def apply_delete(request, apply_id):
    a = get_object_or_404(Apply, pk=apply_id)
    a.delete()
    messages.success(request, '成功！删除发布申请单')
    return HttpResponseRedirect(reverse('configmanager:applylist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeploySiteView(generic.DetailView):
    model = Apply
    template_name = 'configmanager/deploy_sitelist.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SLBListView(generic.ListView):
    template_name = 'configmanager/slb_list.html'
    context_object_name = 'slb_list'
    paginate_by = 10

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            slb_list = SLB.objects.filter(Q(name__icontains=q) |
                                          Q(instanceid__icontains=q) |
                                          Q(ip__icontains=q)).order_by('name')
        else:
            slb_list = SLB.objects.order_by('name')
        return slb_list

    def get_context_data(self, **kwargs):
        context = super(SLBListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


@login_required(login_url='/login/')
def all_slb_info_update(request):
    slb_list = []
    try:
        result = query_slb_info(regionid='cn-hangzhou')
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                            content_type="application/json")
    else:
        if 'Message' in result:
            return HttpResponse(json.dumps({'success': False, 'message': result['Message']}),
                                content_type="application/json")
        else:
            for slb in result:
                '''新增或更新现有SLB'''
                if not SLB.objects.filter(instanceid=slb['LoadBalancerId']):
                    s = SLB(instanceid=slb['LoadBalancerId'], name=slb['LoadBalancerName'],
                            status=slb['LoadBalancerStatus'], ip=slb['Address'], addresstype=slb['AddressType'],
                            createdate=slb['CreateTime'], networktype=slb['NetworkType'])
                    s.save()
                else:
                    s = SLB.objects.get(instanceid=slb['LoadBalancerId'])
                    s.instanceid = slb['LoadBalancerId']
                    s.name = slb['LoadBalancerName']
                    s.status = slb['LoadBalancerStatus']
                    s.ip = slb['Address']
                    s.addresstype = slb['AddressType']
                    s.createdate = slb['CreateTime']
                    s.networktype = slb['NetworkType']
                    s.save()
                slb_list.append(slb['LoadBalancerId'])
            for current_slb in SLB.objects.all():
                '''删除阿里云没有的SLB'''
                if current_slb.instanceid not in slb_list:
                    current_slb.delete()
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SLBDetailView(UpdateView):
    model = SLB
    form_class = SLBForm
    template_name = 'configmanager/slb_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SLBDetailView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['slb_form'] = SLBForm(self.request.POST, instance=self.object)
            context['slbsite_form'] = SLBsiteFormSet(self.request.POST)
        else:
            context['slb_form'] = SLBForm(instance=self.object)
            context['slbsite_form'] = SLBsiteFormSet(instance=self.object)
        return context


@login_required(login_url='/login/')
def slb_rela_site(request, slb_id):
    slb = get_object_or_404(SLB, pk=slb_id)
    if request.method == 'POST':
        if request.POST.has_key('slb-rela-site'):
            formset = SLBsiteFormSet(request.POST, request.FILES, instance=slb)
            if formset.is_valid():
                formset.save()
        return HttpResponseRedirect(reverse('configmanager:slblist'))


@login_required(login_url='/login/')
def slb_health_update(request, slb_id):
    try:
        '''判断SLB实例是否存在'''
        slb = get_object_or_404(SLB, pk=slb_id)
    except:
        return render_to_response(request.META['HTTP_REFERER'], {'success': False})
    else:
        try:
            '''判断调用阿里云接口是否成功'''
            result = query_slb_health(LoadBalancerId=slb.instanceid)
        except:
            return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                                content_type="application/json")
        else:
            if 'Message' in result:
                '''判断调用阿里云是否返回报错信息'''
                return HttpResponse(json.dumps({'success': False, 'message': result['Message']}),
                                    content_type="application/json")
            else:
                '''无报错则开始处理返回数据'''
                for sh in SLBhealthstatus.objects.filter(SLB_id=slb.id):
                    '''先将该SLB下所属ECS状态更新为已移除'''
                    sh.SLBstatus = 'removed'
                    sh.save()
                for r in result:
                    try:
                        '''判断数据库中是否存在ECS，没有则需要先到ECS页面同步ECS信息'''
                        ecs = get_object_or_404(ECS, instanceid=r['ServerId'])
                    except:
                        return HttpResponse(json.dumps({'success': False, 'message': 'ECS不存在，请到ECS页面进行同步后再刷新SLB信息'}),
                                            content_type="application/json")
                    else:
                        '''判断数据库中该SLB是否有对应的后端服务器记录，没有则增加，有则更新'''
                        if not SLBhealthstatus.objects.filter(SLB_id=slb.id, ECS_id=ecs.id):
                            sh = SLBhealthstatus(SLB_id=slb.id, ECS_id=ecs.id, SLBstatus='added',
                                                 healthstatus=r['ServerHealthStatus'])
                            sh.save()
                        else:
                            sh = SLBhealthstatus.objects.get(SLB_id=slb.id, ECS_id=ecs.id)
                            sh.SLB_id = slb.id
                            sh.ECS_id = ecs.id
                            sh.SLBstatus = 'added'
                            sh.healthstatus = r['ServerHealthStatus']
                            sh.save()
                return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def more_slb_health_update(request, site_id):
    try:
        s = get_object_or_404(Site, pk=site_id)
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '没有此站点，请重新刷新页面'}), content_type="application/json")
    else:
        slb_id_list = s.get_slb_id_list()
        if 0 not in slb_id_list:
            for slbid in slb_id_list:
                slb_health_update(request, slb_id=slbid)
        else:
            return HttpResponse(json.dumps({'success': False, 'message': '该站点没有关联SLB，请到SLB管理页面进行关联'}),
                                content_type="application/json")
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def all_slb_health_update(request):
    for slb in SLB.objects.all():
        slb_health_update(request, slb_id=slb.id)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def remove_backend_server(request, slb_id, server_id):
    slb = get_object_or_404(SLB, pk=slb_id)
    slbinstanceId = slb.instanceid
    ecs = ECS.objects.get(pk=server_id)
    backendservers = []
    backendservers.append(ecs.instanceid)
    backendservers = json.dumps(backendservers)
    try:
        r = remove_backendserver(LoadBalancerId=slbinstanceId, BackendServers=backendservers)
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                            content_type="application/json")
    else:
        if 'Message' in r:
            return HttpResponse(json.dumps({'success': False, 'message': r['Message']}),
                                content_type="application/json")
        else:
            slb_health_update(request, slb.id)
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def site_remove_backend_server(request, site_id, server_id):
    try:
        s = get_object_or_404(Site, pk=site_id)
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '该站点不存在，请重新刷新页面'}),
                            content_type="application/json")
    else:
        for slb in s.slbsite_set.all():
            remove_backend_server(request, slb_id=slb.SLB.id, server_id=server_id)
        slb_health_update(request, slb_id=slb.SLB.id)
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def add_backend_server(request, slb_id, server_id):
    slb = get_object_or_404(SLB, pk=slb_id)
    slbinstanceId = slb.instanceid
    ecs = ECS.objects.get(pk=server_id)
    serverdict = {}
    serverlist = []
    serverdict['ServerId'] = str(ecs.instanceid)
    serverdict['Weight'] = str(100)
    serverlist.append(serverdict)
    backendservers = json.dumps(serverlist)
    try:
        result = add_backendserver(LoadBalancerId=slbinstanceId, BackendServers=backendservers)
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '网络超时，调用阿里云接口失败'}),
                            content_type="application/json")
    else:
        if 'Message' in result:
            return HttpResponse(json.dumps({'success': False, 'message': result['Message']}),
                                content_type="application/json")
        else:
            slb_health_update(request, slb.id)
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def site_add_backend_server(request, site_id, server_id):
    try:
        s = get_object_or_404(Site, pk=site_id)
    except:
        return HttpResponse(json.dumps({'success': False, 'message': '该站点不存在，请重新刷新页面'}),
                            content_type="application/json")
    else:
        for slb in s.slbsite_set.all():
            add_backend_server(request, slb_id=slb.SLB.id, server_id=server_id)
        slb_health_update(request, slb_id=slb.SLB.id)
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required(login_url='/login/')
def slb_part_refresh(request, slb_id):
    slb = SLB.objects.get(pk=slb_id)
    template = 'configmanager/slbpart_health_template.html'
    return render(request, template, {"slb": slb})


@login_required(login_url='/login/')
def slb_whole_refresh(request, pagenumber):
    slb_list = SLB.objects.order_by('name')
    template = 'configmanager/slbwhole_health_template.html'
    paginator = Paginator(slb_list, 10)
    try:
        slb_list = paginator.page(pagenumber)
    except PageNotAnInteger:
        slb_list = paginator.page(1)
    except EmptyPage:
        slb_list = paginator.page(paginator.num_pages)
    return render(request, template, {'slb_list': slb_list, 'pagenumber': pagenumber})


@login_required(login_url='/login/')
def config_slb_part_refresh(request, site_id):
    site = Site.objects.get(pk=site_id)
    template = 'configmanager/config_slb_template.html'
    return render(request, template, {"site": site})


@login_required(login_url='/login/')
def config_ecs_part_refresh(request, site_id):
    site = Site.objects.get(pk=site_id)
    template = 'configmanager/config_ecs_template.html'
    return render(request, template, {"site": site})


@login_required(login_url='/login/')
def apply_part_refresh(request, site_id):
    site = Deployitem.objects.get(pk=site_id)
    template = 'configmanager/deploysite_template.html'
    return render(request, template, {"site": site})


@login_required(login_url='/login/')
def ecs_part_refresh(request, ecs_id, pagenumber):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    template = 'configmanager/ecslist_part_template.html'
    return render(request, template, {"ecs": ecs, 'pagenumber': pagenumber})


@login_required(login_url='/login/')
def ecs_whole_refresh(request, pagenumber):
    ECS_list = ECS.objects.order_by('name')
    template = 'configmanager/ecslist_whole_template.html'
    paginator = Paginator(ECS_list, 10)
    try:
        ECS_list = paginator.page(pagenumber)
    except PageNotAnInteger:
        ECS_list = paginator.page(1)
    except EmptyPage:
        ECS_list = paginator.page(paginator.num_pages)
    return render(request, template, {'ECS_list': ECS_list, 'pagenumber': pagenumber})


@login_required(login_url='/login/')
def site_whole_refresh(request, pagenumber):
    Site_list = Site.objects.order_by('fullname')
    template = 'configmanager/sitelist_whole_template.html'
    paginator = Paginator(Site_list, 10)
    try:
        Site_list = paginator.page(pagenumber)
    except PageNotAnInteger:
        Site_list = paginator.page(1)
        return render(request, template, {'Site_list': Site_list, 'pagenumber': pagenumber})
    except EmptyPage:
        return HttpResponse(json.dumps({'empty': True, 'pagenumber': paginator.num_pages}),
                            content_type="application/json")
    else:
        return render(request, template, {'success': True, 'Site_list': Site_list, 'pagenumber': pagenumber})


@login_required(login_url='/login/')
def race_wholerefresh(request, pagenumber, type):
    Race_list = Siterace.objects.order_by('raceid')
    template = 'configmanager/racelist_whole_template.html'
    paginator = Paginator(Race_list, 5)
    if type == 'delete':
        try:
            Race_list = paginator.page(pagenumber)
        except PageNotAnInteger:
            Race_list = paginator.page(1)
            return render(request, template, {'Race_list': Race_list, 'pagenumber': pagenumber})
        except EmptyPage:
            print paginator.num_pages
            return HttpResponse(json.dumps({'empty': True, 'pagenumber': paginator.num_pages}),
                                content_type="application/json")
        else:
            return render(request, template, {'Race_list': Race_list, 'pagenumber': pagenumber})
    else:
        return HttpResponse(json.dumps({'add': True, 'pagenumber': pagenumber}), content_type="application/json")


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AlarmHistoryListView(generic.ListView):
    model = Alarm_History
    template_name = 'configmanager/alarm_list.html'
    context_object_name = 'alarm_list'
    paginator_class = SafePaginator
    paginate_by = 10

    def get_queryset(self):
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if (q != ''):
            alarm_list = Alarm_History.objects.filter(Q(instance_name__icontains=q)).order_by('-alarm_time')
        else:
            alarm_list = Alarm_History.objects.order_by('-alarm_time')
        return alarm_list

    def get_context_data(self, **kwargs):
        context = super(AlarmHistoryListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        context['q'] = q
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)
