# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import Deployitem
from django.core.exceptions import NON_FIELD_ERRORS


class DeployitemForm(ModelForm):
    class Meta:
        model = Deployitem
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
