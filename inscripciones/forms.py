# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from models import *
from django.forms.models import inlineformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.localflavor.es.forms import *
from django.contrib.admin import widgets                                       
from django.utils.translation import gettext_lazy as _

class RegistrationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono (*)"))
    class Meta:
        model = Registration
        exclude = ('paid','accept_conditions')
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']

class RegistrationEditForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    class Meta:
        model = Registration
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']
