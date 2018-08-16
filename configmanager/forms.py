# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, DateField
from .models import Apply, Deployitem, SLB, SLBsite, SLBhealthstatus
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


class SLBForm(ModelForm):
    class Meta:
        model = SLB
        exclude = '__all__'


DeployitemFormSet = inlineformset_factory(Apply, Deployitem, fields=('deployorderby', 'jenkinsversion', 'deploysite', 'type'), extra=1, can_delete=True)
SLBsiteFormSet = inlineformset_factory(SLB, SLBsite, fields=('site',), extra=1, can_delete=True)
