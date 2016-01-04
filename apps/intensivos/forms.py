# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  


from django import forms
from django.forms import ModelForm
from models import *
from django.forms.models import inlineformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.localflavor.es.forms import *
from django.contrib.admin import widgets                                       
from django.utils.translation import gettext_lazy as _

class RegistrationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #~ horarios = forms.ModelMultipleChoiceField(required=True,widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = Registration
        exclude = ('paid','accept_conditions')
        #~ widgets = {
            #~ 'horarios': forms.widgets.CheckboxSelectMultiple(),
        #~ }
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']
        self.fields['horarios'].widget.attrs['size']='6'  
    def save(self, commit=True):
        instancia = super(RegistrationForm, self).save(commit=False)
	instancia.save(commit=False)
        print self.cleaned_data
	for horario in self.cleaned_data['horarios']:
            print "Añadiendo",horario
            instancia.horarios.add(horario)
            print "Añadido",horario
        if commit:
            print "vamos a guardar"
            instancia.save()
            print "guardado"
        return instancia

class RegistrationEditForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    class Meta:
        model = Registration
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']
