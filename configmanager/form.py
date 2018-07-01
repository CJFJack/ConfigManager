# -*- coding: utf-8 -*-
from django.forms import ModelForm
from myapp.models import Deployitem


class DeployitemForm(ModelForm)
    class Meta:
        model = Deployitem
        fields = ['applyproject', 'deployorderby', 'jenkinsversion', 'type', 'deploysite', 'deploy_status']
