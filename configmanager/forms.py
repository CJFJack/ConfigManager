# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, DateField
from .models import Apply, Deployitem
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets


class ApplyForm(ModelForm):
    wishdeploy_time = DateField(widget=widgets.AdminDateWidget(), label=u'期望发布日期')
    class Meta:
        model = Apply
        fields = '__all__'
        widgets = {
            'confamendexplain': Textarea(attrs={'cols': 80, 'rows': 20}),
            'remarkexplain': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


DeployitemFormSet = inlineformset_factory(Apply, Deployitem, fields=('deployorderby', 'jenkinsversion', 'deploysite', 'type', 'deploy_status'), extra=2, can_delete=True) 
