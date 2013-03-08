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
	dni = ESIdentityCardNumberField()
	postal_code = ESPostalCodeField(label=_("Código Postal"))
	class Meta:
		model = Registration
		exclude = ('paid')
		fields = ['exam','minor','tutor_name','tutor_surname','name','surname','address','location','postal_code','sex','birth_date','dni','telephone','email','eide_alumn','centre_name']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.fields['birth_date'].widget.format = '%d-%m-%Y'

		# at the same time, set the input format on the date field like you want it:
		self.fields['birth_date'].input_formats = ['%d-%m-%Y']	

class RegistrationEditForm(ModelForm):
	telephone = ESPhoneNumberField(label=_("Teléfono"))
	dni = ESIdentityCardNumberField()
	postal_code = ESPostalCodeField(label=_("Código Postal"))
	class Meta:
		model = Registration
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.fields['birth_date'].widget.format = '%d-%m-%Y'

		# at the same time, set the input format on the date field like you want it:
		self.fields['birth_date'].input_formats = ['%d-%m-%Y']

class ComputerBasedRegistrationForm(ModelForm):
	telephone = ESPhoneNumberField()
	dni = ESIdentityCardNumberField()
	postal_code = ESPostalCodeField()
#	def __init__(self, *args, **kw):
#        super(ModelForm, self).__init__(*args, **kw)
#		self.fields.keyOrder = ['exam','minor','tutor_name','tutor_surname']
	class Meta:
		model = ComputerBasedRegistration
		
		exclude = ('paid')
		fields = ['exam','minor','tutor_name','tutor_surname','name','surname','address','location','postal_code','sex','birth_date','dni','telephone','email','eide_alumn','centre_name']
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.fields['birth_date'].widget.format = '%d-%m-%Y'

		# at the same time, set the input format on the date field like you want it:
		self.fields['birth_date'].input_formats = ['%d-%m-%Y']	
