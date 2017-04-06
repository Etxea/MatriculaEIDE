# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime 
from django.conf import settings
#Para la autogneración de passwd
from random import choice
from string import letters
#Para el envio del mail de confirmacion
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

CURSO = (
    (1, _('Inglés nivel A2')),
    (2, _('Inglés nivel B2')),
    (3, _('Inglés nivel C1')),
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

class Registration(models.Model):
    course = models.DecimalField('¿En que curso estás interesado?',max_digits=1, decimal_places=0,choices=CURSO)
    password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
    name = models.CharField(_('Nombre (*)'),max_length=50)
    surname = models.CharField(_('Apellido(s) (*)'),max_length=100)
    #~ address = models.CharField(_('Address'),max_length=100)
    #~ location = models.CharField(_('Location'),max_length=100)
    birth_date = models.DateField(_('Birth Date'),help_text=_('Formato: AAAA-MM-DD(año-mes-día)'))
    telephone = models.CharField('Tel. Fijo (*)',max_length=12)
    email = models.EmailField('Email (*)')
    registration_date = models.DateField(default=datetime.date.today, auto_now_add=True)
    accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
    paid = models.BooleanField(_('Paid'),default=False)
    estudios_superiores = models.BooleanField('¿Tienes titulación de ESO o Superior?')
    english_level = models.DecimalField('¿Cuál es tu nivel de Inglés?',max_digits=1, decimal_places=0,choices=ENGLISH_LEVEL)
    english_qualification = models.CharField('¿Tienes titulación oficial de Inglés?¿Cual?',max_length=25)
    def get_absolute_url(self):
        return '/inscripciones/edit/%d/'%self.id
    def __unicode__(self):
        return u"%s-%s"%(self.id,self.email)
    def registration_name(self):
        return self.__unicode__()
    def send_confirmation_email(self):
        ##Para el alumno
        subject = "Has solicitado un curso en EIDE"        
        html_content = u"""
<html>
<head>
        <link rel="stylesheet" href="https://matricula-eide.es/site_media/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://matricula-eide.es/site_media/static/css/extra.css">
</head>
<body>
<div class="well">
    <p>Buenas</p>
    Acaba de realizar una solicitud de curso para: <br />
    %s <br>
    <p>Pronto nos pondremos en contacto desde EIDE para formalizar la inscripción.</p>
    <p>Gracias.</p>
</div>
<div class="well">
<p></p>
</div>
</body>
</html>
"""%(self.get_course_display())
        
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        msg.send()
        
        ##Para el secretaria        
        subject = "[EIDE] Matricula curso"
        payload = {'registration': self}
        
        html_content = render_to_string('inscripciones/registration_detail.html', payload)
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, ["moebius1984@gmail.com","secretaria@eide.es"])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        msg.send()

    
        
#~ def Curso(models.model):
    #~ name = models.CharField(_('Nombre (*)'),max_length=50)
    #~ description = models.CharField(_('Descripción (*)'),max_length=500)
    #~ price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #~ def __unicode__:
        #~ return self.name
