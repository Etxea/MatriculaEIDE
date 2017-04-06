# -*- coding: utf-8 -*-
from django.forms import ModelForm, DateField
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.es.forms import *
from django.utils.translation import gettext_lazy as _

from models import *

class ReservationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    #postal_code = ESPostalCodeField(label=_("Código Postal"))
    birth_date = DateField(label="Fecha Nac. (DD/MM/AAAA)", input_formats=['%d/%m/%Y'])
    class Meta:
        model = Reservation
        exclude = ('password',)

        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD/MM/YYYY", "pickTime": False}),
        }