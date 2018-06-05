# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators import csrf
from django.shortcuts import render

# Create your views here.

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
        return ECS.objects.order_by('modified_time')


class ECSChangeView(generic.DetailView):
    model = ECS
    template_name = 'configmanager/ecs_change.html'


def save(request, ecs_id):
    pass




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
