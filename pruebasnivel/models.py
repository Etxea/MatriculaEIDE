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

HOURS = (
    (1,"10-11"),
    (2,"11-12"),
    (3,"16-17"),
    (4,"17-18"),
    (5,"18-19"),
    (5,"19-20"),
)

WEEKDAYS = (
    (1,_("Monday")),
    (2,_("Tuesday")),
    (3,_("Wednesday")),
    (4,_("Thursday")),
    (5,_("Friday")),
)


AVAILABILITY = (
    (1, (
        (1,True),
        (2,True),
        (3,False),
        (4,True),
        (5,True),
        )
    ),
    (2, (
        (1,False),
        (2,False),
        (3,False),
        (4,True),
        (5,False),
        )
    ),
)

class Availability(models.Model):
    venue = models.DecimalField(_('Venue'), max_digits=1, decimal_places=0, choices=VENUES)
    hour = models.DecimalField(_('Hour'), max_digits=1, decimal_places=0, choices=HOURS)
    weekday = models.DecimalField(_('Week Day'), max_digits=1, decimal_places=0, choices=WEEKDAYS)

class Reservation(models.Model):
    password = models.CharField(_('Password'), max_length=6, blank=True, editable=False)
    venue = models.DecimalField(_('Venue'), max_digits=1, decimal_places=0, choices=VENUES)
    name = models.CharField(_('Nombre (*)'), max_length=50)
    surname = models.CharField(_('Apellido(s) (*)'), max_length=100)
    #~ address = models.CharField(_('Address'),max_length=100)
    #~ location = models.CharField(_('Location'),max_length=100)
    birth_date = models.DateField(_('Birth Date'), help_text=_('Formato: DD/MM/AAAA'))
    telephone = models.CharField('Tel. Fijo (*)', max_length=12)
    email = models.EmailField('Email (*)')
    registration_date = models.DateField(default=datetime.date.today)
    create_date = models.DateField(auto_now_add=True)
    accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
    def send_confirmation_email(self):
        ##Para el alumno
        subject = "Has realizado una reserva de prueba de nivel en EIDE"
        html_content = u"""

        <div class="well">
            Acaba de realizar una reserva de nivel en el centro %s de EIDE el día %s<br />

        </div>
        """ % (self.get_venue_display(), self.registration_date)

        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email], html_message=message_body)

        ### Para los admins
        subject = "Hay una nueva reserva de prueba de nivel para cambridge %s"%self.get_venue_display()
        message_body = u"""Se ha dado de alta una reserva para el centro %s el día %s.
            Los datos son del alumno son:
            Nombre: %s
            Apellidos: %s
            Telefono: %s
            e-mail: %s """%(self.get_venue_display(),self.registration_date,self.name,self.surname,self.telephone,self.email)
        mail_admins(subject, message_body)
