# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from time import time
from datetime import datetime
from re import split
from django.core.files import File
import os, json

# Create your views here.

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import ECS, Site, Configfile, Siterace, Release, ConfigmanagerHistoricalconfigfile, Apply, Deployitem, SLB, SLBsite, SLBhealthstatus, DeployECS
from .forms import ApplyForm, DeployitemFormSet, SLBForm, SLBsiteFormSet
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.forms import inlineformset_factory
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from .acs_ecs_monitor import query_ecs_api
from .acs_ecs_info import query_ecs_info
from .acs_slb_info import query_slb_info
from .acs_slb_health import query_slb_health
from .acs_slb_backendserver_remove import remove_backendserver
from .acs_slb_backendserver_add import add_backendserver
from .acs_all_ecs_info import query_all_ecs


app_name = 'configmanager'


@login_required(login_url='/login/')
def index(request):
    return render_to_response('configmanager/index.html')


@login_required(login_url='/login/')
def nav_top(request):
    return render_to_response('configmanager/nav_top.html')


@login_required(login_url='/login/')
def welcome(request):
    print request.user.username
    context = {}
    return render(request, 'configmanager/welcome.html', context)


@login_required(login_url='/login/')
def deploymanager(request):
    return render_to_response('configmanager/deploymanager.html')


@login_required(login_url='/login/')
def systemmanager(request):
    return render_to_response('configmanager/systemmanager.html')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSListView(generic.ListView):
    template_name = 'configmanager/ecs_list.html'
    context_object_name = 'ECS_list'
    def get_queryset(self):
        return ECS.objects.order_by('name')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSChangeView(generic.DetailView):
    model = ECS
    template_name = 'configmanager/ecs_change.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ECSAddView(generic.ListView):
    model = ECS
    template_name = 'configmanager/ecs_add.html'


@login_required(login_url='/login/')
def ecs_save(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.name = request.POST['name']
    ecs.instanceid = request.POST['instanceid']
    ecs.IP = request.POST['IP']
    ecs.status = request.POST['status']
    ecs.modified_user = request.user.username
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def ecs_enable(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.status = 'Y'
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def ecs_disable(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.status = 'N'
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def ecs_delete(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.delete()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def ecs_add(request):
    name = request.POST['name']                                                                                                       
    instanceid = request.POST['instanceid']                                                                                           
    IP = request.POST['IP']                                                                                                           
    status = request.POST['status']                                                                                                   
    ecs = ECS(name=name, instanceid=instanceid, IP=IP, status=status, modified_user=request.user.username)
    ecs.save()                                                                                                                            
    return HttpResponseRedirect(reverse('configmanager:ecslist'))   


@login_required(login_url='/login/') 
def update_ecs_monitor(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    instanceid = ecs.instanceid.encode('utf-8')    
    try:
        recently_cpu=query_ecs_api(instanceid=instanceid, metric="cpu_total")
        recently_mem=query_ecs_api(instanceid=instanceid, metric="memory_usedutilization")
        recently_diskusage=query_ecs_api(instanceid=instanceid, metric="diskusage_utilization")
    except:
        pass
    else:
        ecs.recently_memory = recently_mem['Average']
        ecs.recently_cpu = recently_cpu['Average']
        ecs.recently_diskusage = recently_diskusage['Average']
        ecs.save()

    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def update_allecs_monitor(request):
    for ecs in ECS.objects.all():
        update_ecs_monitor(request, ecs.id)
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')                                                                                                      
def update_ecs_info(request, ecs_id): 
    ecs = get_object_or_404(ECS, pk=ecs_id)
    instanceid = ecs.instanceid.encode('utf-8')
    try:
        result=query_ecs_info(instanceids=[instanceid])
    except:
        pass
    else:
        print result
        ecs.instancestatus = result['Status']
        ecs.IP = result['InnerIpAddress']
        ecs.publicipaddress = result['PublicIpAddress']
        ecs.regionId = result['RegionId']
        ecs.osname = result['OSName']
        ecs.expiredtime = result['ExpiredTime']
        ecs.memory = result['Memory']/1024
        ecs.ostype = result['OSType']
        ecs.networktype = result['NetworkType']
        ecs.name = result['InstanceName']
        ecs.cpu = result['Cpu']
        ecs.save()

    return HttpResponseRedirect(reverse('configmanager:ecslist'))


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
            ecs = ECS(instanceid=ecsinstanceid)
            ecs.delete()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


@login_required(login_url='/login/')
def update_allecs_info(request):
    for ecs in ECS.objects.all():
        update_ecs_info(request, ecs.id)
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


    
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteListView(generic.ListView):
    template_name = 'configmanager/site_list.html'
    context_object_name = 'Site_list'
    def get_queryset(self):
        return Site.objects.order_by('fullname')

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        context['configfile'] = Site.configfile_set
        return context            


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
def site_change(request, site_id):
    s = get_object_or_404(Site, pk=site_id)
    f = ';'.join([f.filename for f in s.configfile_set.all()]) 
    return render(request, 'configmanager/site_change.html', {'site': s, 'configfiles': f})

@login_required(login_url='/login/')
def add_relation_ecs(request, site):

    for key in request.POST:
        try:
            e = ECS.objects.get(name=key)
        except:
            pass
        else:
            site.ECSlists.add(e)

@login_required(login_url='/login/')
def add_relation_site(request, site):

    if not site.exist_or_not_in_siterace():                                                                                              
        for key in request.POST:                                                                                                      
            try:                                                                                                                      
                relation_s = Site.objects.get(fullname=key)                                                                           
            except:                                                                                                                   
                pass                                                                                                                  
            else:                                                                                                                     
                raceid = relation_s.get_raceid()                                                                                      
                if raceid != 0:                                                                                                       
                    site.siterace_set.create(raceid=raceid)                                                                              
                                                                                                                                      
    if not site.exist_or_not_in_siterace():                                                                                              
        raceid=int(round(time() * 1000))                                                                                              
        site.siterace_set.create(raceid=raceid)                                                                                          
                                                                                                                                      
    L = []                                                                                                                            
    raceid=int(round(time() * 1000))                                                                                                  
    if site.exist_or_not_in_siterace():                                                                                                  
        for key in request.POST:                                                                                                      
            try:                                                                                                                      
                relation_s = Site.objects.get(fullname=key)                                                                           
            except:                                                                                                                   
                pass                                                                                                                  
            else:                                                                                                                     
                if not relation_s.exist_or_not_in_siterace():                                                                         
                    raceid = site.get_raceid()                                                                                           
                    relation_s.siterace_set.create(raceid=raceid)


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
        s.save()
        
        '''新增或删除关联配置文件'''
        post_filenames_list = []
        post_filenames = request.POST['configfiles']
        post_filenames_list = post_filenames.split(';')
        s.update_configfiles(post_filenames_list=post_filenames_list)

        ''''增加所属ECS'''
        add_relation_ecs(request=request, site=s) 

        '''减少所属ECS'''
        for es in s.ECSlists.all():
            if not request.POST.has_key(es.name):
                s.ECSlists.remove(es)

        '''减少关联站点'''
        L = []
        for key in request.POST:
            try:
                relation_s = Site.objects.get(fullname=key)
            except:
                pass
            else:
                L.append(relation_s.fullname)
        if s.get_relation_sites():
            for rs in s.get_relation_sites():
                if rs not in L:
                    rs_obj = Site.objects.get(fullname=rs)
                    rs_obj.siterace_set.all().delete()                        
 
        '''增加关联站点'''
        add_relation_site(request, s)
      
        '''若站点没有任何关联站点族，则将其从站点族中删除'''
        if not s.get_relation_sites():
            s.siterace_set.all().delete()

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
    if request.POST.has_key('site-save'):
        '''保存站点基础信息'''
        fullname = request.POST['fullname']
        shortname = request.POST['shortname']
        configdirname = request.POST['configdirname']
        port = request.POST['port']
        testpage = request.POST['testpage']
        status = request.POST['status']
        devcharge = request.POST['devcharge']
        deployattention = request.POST['deployattention']
        modified_user = request.user.username
        site = Site(fullname=fullname, shortname=shortname, configdirname=configdirname, port=port, testpage=testpage, status=status, devcharge=devcharge, deployattention=deployattention, modified_user=modified_user)
        site.save()
        '''添加关联ECS、所属站点族'''
        add_relation_site(request, site)
        add_relation_ecs(request, site)
        '''新增或删除关联配置文件'''
        post_filenames_list = []
        post_filenames = request.POST['configfiles']
        post_filenames_list = post_filenames.split(';')
        site.update_configfiles(post_filenames_list=post_filenames_list)
    return HttpResponseRedirect(reverse('configmanager:sitelist'))


@login_required(login_url='/login/')
def site_delete(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    site.delete()
    return HttpResponseRedirect(reverse('configmanager:sitelist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigListView(generic.ListView):
    model = Site
    template_name = 'configmanager/config_list.html'
    

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UndeployConfigListView(generic.ListView):
    model = Site
    template_name = 'configmanager/undeploy_config_list.html'


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
    '''生成配置文件'''
    ecs = r.ECS.name
    config_path = os.path.join('/release', r.site.fullname, ecs, 'releaseconfig')
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    for c in r.site.configfile_set.all():
        file_name = os.path.join(config_path, c.filename)
        with open(file_name, 'w') as f:
            myfile = File(f)
            myfile.write(c.content)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


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
    return render_to_response(template_name, {'confighistory_list': confighistory_list})
    

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigHistoryDetailView(generic.DetailView):
    model = ConfigmanagerHistoricalconfigfile
    template_name = 'configmanager/config_history_detail.html'
    context_object_name = 'confighistorydetail'


@login_required(login_url='/login/')
def config_rollback(request, confighistorydetail_id):
    ch = ConfigmanagerHistoricalconfigfile.objects.get(pk=confighistorydetail_id)
    configfileid=ch.id
    if request.POST.has_key('config-rollback'):
        rollbackcontent = ch.content
        c = Configfile.objects.get(pk=configfileid)
        c.content = rollbackcontent
        c.save()
        return HttpResponseRedirect(reverse('configmanager:configlist'))
    if request.POST.has_key('config-goback'):
        return HttpResponseRedirect(reverse('configmanager:confighistory', args=(configfileid,)))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ApplyListView(generic.ListView):
    model = Apply
    template_name = 'configmanager/Apply_list.html'


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
    time_str = request.POST['wishdeploy_time']
    time = datetime.strptime(time_str, '%Y/%m/%d')
    obj.wishdeploy_time = time.strftime('%Y-%m-%d')
    obj.confamendexplain = request.POST['confamendexplain']
    obj.remarkexplain = request.POST['remarkexplain']
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
        if request.POST.has_key('apply-commit'):
            a.status = 'DA'
            apply_save(request, a)
        if request.POST.has_key('apply-cancel'):
            a.status = 'C'
            a.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'DA':
        if request.POST.has_key('dev-approval'):
            a.status = 'TA'
            a.save()
        if request.POST.has_key('dev-unapproval'):
            a.status = 'WC'
            a.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'TA':
        if request.POST.has_key('test-approval'):
            a.status = 'EA'
            a.save()
        if request.POST.has_key('test-unapproval'):
            a.status = 'WC'
            a.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'EA':
        if request.POST.has_key('EA-approval'):
            a.status = 'OA'
            a.save()
        if request.POST.has_key('EA-unapproval'):
            a.status = 'WC'
            a.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'OA':
        if request.POST.has_key('OA-approval'):
            a.status = 'TDA'
            a.save()
        if request.POST.has_key('OA-unapproval'):
            a.status = 'WC'
            a.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'TDA':
        if request.POST.has_key('TDA-approval'):
            a.status = 'WD'
            a.save()
        if request.POST.has_key('TDA-unapproval'):
            a.status = 'WC'
            a.save()
        return HttpResponseRedirect(reverse('configmanager:applylist'))
    if a.status == 'WD':
        if request.POST.has_key('deploy-finish'):
            a.status = 'D'
            a.deploy_user = request.user.username
            a.deploy_time = datetime.now()
            a.save()
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
        if (apply_form.is_valid() and deployitem_form.is_valid()):
            return self.form_valid(apply_form, deployitem_form)
        else:
            return self.form_invalid(apply_form, deployitem_form)

    def form_valid(self, apply_form, deployitem_form):
        apply_form.instance.apply_user = self.request.user
        self.object = apply_form.save()
        deployitem_form.instance = self.object
        for form in deployitem_form:
            site_id = form.cleaned_data['deploysite'].id
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
    return HttpResponseRedirect(reverse('configmanager:applylist'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DeploySiteView(generic.DetailView):
    model = Apply
    template_name = 'configmanager/deploy_sitelist.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SLBListView(generic.ListView):
    template_name = 'configmanager/slb_list.html'
    context_object_name = 'slb_list'
    def get_queryset(self):
        return SLB.objects.order_by('name')


@login_required(login_url='/login/')
def all_slb_info_update(request):
    slb_list = []
    for slb in query_slb_info(regionid='cn-hangzhou'):
        if not SLB.objects.filter(instanceid=slb['LoadBalancerId']):
            s = SLB(instanceid=slb['LoadBalancerId'], name=slb['LoadBalancerName'], status=slb['LoadBalancerStatus'], ip=slb['Address'], addresstype=slb['AddressType'], createdate=slb['CreateTime'], networktype=slb['NetworkType'])
            s.save()
        else:
            s = SLB.objects.get(instanceid=slb['LoadBalancerId'])
            s.instanceid=slb['LoadBalancerId']
            s.name=slb['LoadBalancerName']
            s.status=slb['LoadBalancerStatus']
            s.ip=slb['Address']
            s.addresstype=slb['AddressType']
            s.createdate=slb['CreateTime']
            s.networktype=slb['NetworkType']
            s.save()
        slb_list.append(slb['LoadBalancerId'])    
        print slb_list
    for current_slb in SLB.objects.all():
        if current_slb.instanceid not in slb_list:
            current_slb.delete()
    return HttpResponseRedirect(reverse('configmanager:slblist'))
            
        
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
def slb_health_update(request, slb_id, redirect='yes'):
    try:
        slb = get_object_or_404(SLB, pk=slb_id)
    except:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        result = query_slb_health(LoadBalancerId=slb.instanceid)
        for sh in SLBhealthstatus.objects.filter(SLB_id=slb.id):
            sh.SLBstatus = 'removed'
            sh.save()
        for r in result:
            try:
                ecs = get_object_or_404(ECS, instanceid=r['ServerId'])
            except:
                pass
            else:
                if not SLBhealthstatus.objects.filter(SLB_id=slb.id, ECS_id=ecs.id):
                    sh = SLBhealthstatus(SLB_id=slb.id, ECS_id=ecs.id, SLBstatus='added', healthstatus=r['ServerHealthStatus'])
                    sh.save()
                else:
                    sh = SLBhealthstatus.objects.get(SLB_id=slb.id, ECS_id=ecs.id)
                    sh.SLB_id=slb.id
                    sh.ECS_id=ecs.id
                    sh.SLBstatus='added'
                    sh.healthstatus=r['ServerHealthStatus']
                    sh.save()
    if redirect == 'yes':
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def more_slb_health_update(request, site_id):
    s = get_object_or_404(Site, pk=site_id)
    slb_id_list = s.get_slb_id_list()
    for slbid in slb_id_list:
        slb_health_update(request, slb_id=slbid, redirect='no')
    return HttpResponseRedirect(reverse('configmanager:configlist'))


@login_required(login_url='/login/')
def all_slb_health_update(request):
    for slb in SLB.objects.all():
        slb_health_update(request, slb_id=slb.id, redirect='no')
    return HttpResponseRedirect(reverse('configmanager:slblist'))


@login_required(login_url='/login/')
def remove_backend_server(request, slb_id, server_id, redirect='yes'):
    slb = get_object_or_404(SLB, pk=slb_id)
    slbinstanceId = slb.instanceid
    ecs = ECS.objects.get(pk=server_id)
    backendservers = []
    backendservers.append(ecs.instanceid)
    backendservers = json.dumps(backendservers)
    r = remove_backendserver(LoadBalancerId=slbinstanceId, BackendServers=backendservers)
    print r
    if redirect == 'yes':
        slb_health_update(request, slb_id=slb.id)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def site_remove_backend_server(request, site_id, server_id):
    s = get_object_or_404(Site, pk=site_id)
    for slb in s.slbsite_set.all():
        remove_backend_server(request, slb_id=slb.SLB.id, server_id=server_id, redirect='no')
        slb_health_update(request, slb_id=slb.SLB.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    

@login_required(login_url='/login/')
def add_backend_server(request, slb_id, server_id, redirect='yes'):
    slb = get_object_or_404(SLB, pk=slb_id)
    slbinstanceId = slb.instanceid
    ecs = ECS.objects.get(pk=server_id)
    serverdict = {}
    serverlist = []
    serverdict['ServerId'] = str(ecs.instanceid)
    serverdict['Weight'] = str(100)
    serverlist.append(serverdict)
    backendservers = json.dumps(serverlist)
    result = add_backendserver(LoadBalancerId=slbinstanceId, BackendServers=backendservers)
    print result
    if redirect == 'yes':
        slb_health_update(request, slb_id=slb.id)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def site_add_backend_server(request, site_id, server_id):
    s = get_object_or_404(Site, pk=site_id)
    for slb in s.slbsite_set.all():
        add_backend_server(request, slb_id=slb.SLB.id, server_id=server_id, redirect='no')
        slb_health_update(request, slb_id=slb.SLB.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




