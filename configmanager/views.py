# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import ECS, Site
from django.http import HttpResponse
from django.views import generic

app_name = 'configmanager'

def index(request):
    return render_to_response('configmanager/index.html')

 
class ECSListView(generic.ListView):
    template_name = 'configmanager/ecs_list.html'
    context_object_name = 'ECS_list'
    def get_queryset(self):
        return ECS.objects.order_by('name')


class ECSChangeView(generic.DetailView):
    model = ECS
    template_name = 'configmanager/ecs_change.html'


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



# 表单
def search_form(request):
    return render_to_response('configmanager/search_form.html')
 
# 接收请求数据
def search(request):  
    request.encoding='utf-8'
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q']
        return HttpResponse(message)
    elif request.POST:
        ctx ={}
        ctx['rlt'] = request.POST['q']
        return render(request, "configmanager/post.html", ctx)
    else:
        message = '你提交了空表单'
        return HttpResponse(message)
