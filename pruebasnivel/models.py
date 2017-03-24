# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.conf import settings

from random import choice
from string import letters
#Para el envio del mail de confirmacion    password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, mail_admins
else:
    from django.core.mail import send_mail, mail_admins


SEXO = (
    (1, _('Male')),
    (2, _('Female')),
)
ENGLISH_LEVEL = (
    (1, _('A1')),
    (2, _('A2')),
    (3, _('B1')),
    (4, _('B2.1')),
    (5, _('B2.2')),
    (6, _('C1.1')),
    (7, _('C1.2')),
    (8, _('C2'))
)
VENUES = (
    (1, "Genaro Ora"),
    (2, "Kabiezes")
)
class Registration(models.Model):
    password = models.CharField(_('Password'), max_length=6, blank=True, editable=False)
    name = models.CharField(_('Nombre (*)'), max_length=50)
    surname = models.CharField(_('Apellido(s) (*)'), max_length=100)
    #~ address = models.CharField(_('Address'),max_length=100)
    #~ location = models.CharField(_('Location'),max_length=100)
    birth_date = models.DateField(_('Birth Date'), help_text=_('Formato: AAAA-MM-DD(año-mes-día)'))
    telephone = models.CharField('Tel. Fijo (*)', max_length=12)
    email = models.EmailField('Email (*)')
    registration_date = models.DateField(default=datetime.date.today)
    create_date = models.DateField(auto_now_add=True)
    accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
    venue = models.DecimalField(_('Venue'),max_digits=1, decimal_places=0,choices=VENUES)