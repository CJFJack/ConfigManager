# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from time import time

# Create your views here.

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import ECS, Site, Configfile, Siterace
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


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


def ecs_save(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.name = request.POST['name']
    ecs.instanceid = request.POST['instanceid']
    ecs.IP = request.POST['IP']
    ecs.status = request.POST['status']
    ecs.modified_user = request.user.username
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


def ecs_enable(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.status = 'Y'
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


def ecs_disable(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.status = 'N'
    ecs.save()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


def ecs_delete(request, ecs_id):
    ecs = get_object_or_404(ECS, pk=ecs_id)
    ecs.delete()
    return HttpResponseRedirect(reverse('configmanager:ecslist'))


def ecs_add(request):
    name = request.POST['name']                                                                                                       
    instanceid = request.POST['instanceid']                                                                                           
    IP = request.POST['IP']                                                                                                           
    status = request.POST['status']                                                                                                   
    ecs = ECS(name=name, instanceid=instanceid, IP=IP, status=status, modified_user=request.user.username)
    ecs.save()                                                                                                                            
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
def site_save(request, site_id):
    if request.POST.has_key('site-save'):
        s = get_object_or_404(Site, pk=site_id)
        s.fullname = request.POST['fullname']
        s.shortname = request.POST['shortname']
        s.configdirname = request.POST['configdirname']
        s.port = request.POST['port']
        s.save()

        ''''增加所属ECS'''
        for key in request.POST:
            try:
                e = ECS.objects.get(name=key)
            except:
                pass
            else:
                s.ECSlists.add(e)

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
        if not s.exist_or_not_in_siterace():
            for key in request.POST:
                try:
                    relation_s = Site.objects.get(fullname=key)
                except:
                    pass
                else:
                    raceid = relation_s.get_raceid()
                    if raceid != 0:
                        s.siterace_set.create(raceid=raceid)

        if not s.exist_or_not_in_siterace():
            raceid=int(round(time() * 1000))
            s.siterace_set.create(raceid=raceid)
                
        L = []
        raceid=int(round(time() * 1000))
        if s.exist_or_not_in_siterace():
            for key in request.POST:
                try:
                    relation_s = Site.objects.get(fullname=key)
                except:
                    pass
                else:
                    if not relation_s.exist_or_not_in_siterace():
                        raceid = s.get_raceid()
                        relation_s.siterace_set.create(raceid=raceid) 
       
        if not s.get_relation_sites():
            s.siterace_set.all().delete()

        return HttpResponseRedirect(reverse('configmanager:sitelist'))

    if request.POST.has_key('site-goback'):
        return HttpResponseRedirect(reverse('configmanager:sitelist'))

