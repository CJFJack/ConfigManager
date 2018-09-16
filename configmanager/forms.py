# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, DateField, Form, CharField
from .models import Apply, Deployitem, SLB, SLBsite
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets
from captcha.fields import CaptchaField


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


class LoginForm(Form):
    username = CharField(required=True, max_length=20)
    password = CharField(required=True, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误！'})