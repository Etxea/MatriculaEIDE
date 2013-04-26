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
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.localflavor import generic
from django.contrib.localflavor.es.forms import *
from django.core.mail import EmailMultiAlternatives

from django_countries import CountryField

from random import choice
from string import letters
import datetime

from django.conf import settings

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, mail_admins
else:
    from django.core.mail import send_mail, mail_admins

SEXO = (
    (1, _('Male')),
    (2, _('Female')),
)

class Accomodation(models.Model):
    price_per_week = models.DecimalField(_('Price'),max_digits=4, decimal_places=0, default=0)
    name = models.CharField(_('Name'),max_length=50)

class Transfer(models.Model):
    price = models.DecimalField(_('Price'),max_digits=4, decimal_places=0, default=0)
    name = models.CharField(_('Name'),max_length=50)

class Course(models.Model):
    price = models.DecimalField(_('Price'),max_digits=4, decimal_places=0, default=0)
    name = models.CharField(_('Name'),max_length=50)


class Registration(models.Model):
    firstname = models.CharField(_('First Name'),max_length=120)
    lastname = models.CharField(_('Last Name'),max_length=120)
    sex = models.DecimalField(_('Sex'),max_digits=1, decimal_places=0,choices=SEXO)
    email = models.EmailField()
    birth_date = models.DateField(_('Date of Birth'),help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    nationality = CountryField(_('Nationality'))
    country = CountryField(_('Coutry of Residence (if different from nationality)'))
    address = models.CharField(_('Address'),max_length=100)
    city = models.CharField(_('City'),max_length=100)
   

    visa = models.BooleanField(_("Will you need student's VISA?"))
    
    course = models.ForeignKey(Course)
    start_date = models.DateField(_('Birth Date'),help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    weeks = models.DecimalField(_('Number of weeks'),max_digits=3, decimal_places=0)
    private_hours_week = models.DecimalField(_('Number of private hours per week (only private courses or intensive +5, +10, +20)'),max_digits=3, decimal_places=0)
    
    
    accomodation = models.ForeignKey(Accomodation)
    arrival_date = models.DateField(_('Arrival Date'),help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    accomodation_weeks = models.DecimalField(_('Number of weeks'),max_digits=3, decimal_places=0)
    
    transfer = models.ForeignKey(Transfer)
    
    
    
    telephone = models.CharField(_('Telephone'),max_length=12)
    
    registration_date = models.DateField(default=datetime.date.today, auto_now_add=True)
    paid = models.BooleanField(_('Paid'),default=False)
    price = models.DecimalField(_('Total Price'),max_digits=4, decimal_places=0, default=0)
    accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'))

    def send_confirmation_email(self):
        ##Para el alumno
        subject = "Te has matriculado para un examen Cambridge en EIDE"
        message_body = """"""
        ### Para los admins
        subject = "Hay una nueva matricula (sin pagar) para cambridge "
        message_body = """"""
        mail_admins(subject, message_body)
    def send_paiment_confirmation_email(self):
        subject = "Se ha confirmado el pago de la matricula para el examen"
        html_content=""""""
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        msg.send()
        
        subject = "Se ha confirmado el pago"
        message_body = """"""
        mail_admins(subject, message_body)
    def set_as_paid(self):
        self.paid = True
        self.save()
        self.send_paiment_confirmation_email()
        
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)
    def generate_payment_url(self):
        return '/pagos/espanol/%s/'%(self.id)

    def save(self, *args, **kwargs):
        if self.id is not None:
            if self.paid:
                self.send_paiment_confirmation_email()		
        else:
            #We send a confirmation mail to te registrant and a advise mail to the admins
            self.send_confirmation_email()
        super(Registration, self).save(*args, **kwargs)
        

