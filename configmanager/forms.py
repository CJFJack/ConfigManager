# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea
from .models import Apply, Deployitem
from django.forms.models import inlineformset_factory


class ApplyForm(ModelForm):
    class Meta:
        model = Apply
        fields = '__all__'
        widgets = {
            'confamendexplain': Textarea(attrs={'cols': 80, 'rows': 20}),
            'remarkexplain': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


DeployitemFormSet = inlineformset_factory(Apply, Deployitem, fields=('deployorderby', 'jenkinsversion', 'deploysite', 'type', 'deploy_status'), extra=1) 
