# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import Apply, Deployitem
from django.forms.models import inlineformset_factory


class ApplyForm(ModelForm):
    class Meta:
        model = Apply
        fields = '__all__'
        localized_fields = ('apply_time',)


DeployitemFormSet = inlineformset_factory(Apply, Deployitem, fields=('deployorderby', 'jenkinsversion', 'deploysite', 'type', 'deploy_status'), extra=1) 
