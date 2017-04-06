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
    (1, _('Elementary (A2)')),
    (2, _('Pre-Intermediate (B1.1)')),
    (3, _('Intermediate (B1.2)')),
    (4, _('Upper-Intermediate (B2.1)')),
    (5, _('First Certificate (B2.2)')),
    (6, _('Pre-Advanded (C1.1)')),
    (7, _('Advanced (C1.2)')),
    (8, _('Proficiency (C2)')),
)

NIVELES_INTESIVO = (
    (1, _('Elementary (A2)')),
    (2, _('Pre-Intermediate (B1.1)')),
    (3, _('Intermediate (B1.2)')),
    (4, _('Upper-Intermediate (B2.1)')),
    (5, _('First Certificate (B2.2)')),
    (6, _('Pre-Advanded (C1.1)')),
    (7, _('Advanced (C1.2)')),
    (8, _('Proficiency (C2)')),
)

NIVELES_IDIOMAS = (
    (1, _('A1')),
    (2, _('A2')),
    (3, _('B1')),
    (4, _('B2.1')),
    (5, _('B2.2')),
    (6, _('C1.1')),
    (7, _('C1.2')),
    (8, _('C2'))
)

class Intensivo(models.Model):
    name = models.CharField(_('Name'),max_length=50)
#    nivel = models.DecimalField('Nivel del curso',max_digits=1, decimal_places=0,choices=NIVELES_INTESIVO)
    dias = models.CharField(_('Dias'),max_length=50)
    horario = models.CharField(_('Horario'),max_length=50)
    inicio = models.DateField(_('Start'),help_text=_('Formato: AAAA-MM-DD(año-mes-día)'))
    fin = models.DateField(_('End'),help_text=_('Formato: AAAA-MM-DD(año-mes-día)'))
    horas = models.DecimalField('Horas',max_digits=3, decimal_places=0)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    def reservas(self):
        return len(self.registration_set.all())
    def __unicode__(self):
        return "%s"%(self.name)

class Horario(models.Model):
    name = models.CharField(_('Horario (*)'),max_length=50,primary_key=True)
    def __unicode__(self):
        return self.name

class Registration(models.Model):
    password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
    name = models.CharField(_('Nombre (*)'),max_length=50)
    surname = models.CharField(_('Apellido(s) (*)'),max_length=100)
    address = models.CharField(_('Address'),max_length=100)
    location = models.CharField(_('Location'),max_length=100)
    birth_date = models.DateField(_('Birth Date'),help_text=_('Formato: AAAA-MM-DD(año-mes-día)'))
    telephone = models.CharField('Tel. Fijo (*)',max_length=12)
    email = models.EmailField('Email (*)')
    registration_date = models.DateField(auto_now_add=True)
    nivel_ingles = models.DecimalField(_('Nivel Ingles Actual'),help_text="",max_digits=1, decimal_places=0,choices=NIVELES_IDIOMAS,blank=True,null=True)
    curso = models.DecimalField('Nivel del curso',max_digits=1, decimal_places=0,choices=CURSO)
    intensivos = models.ManyToManyField(Intensivo,help_text="Recuerde que debe elegir todos los horarios a los que le sea posible asistir. Para seleccionar varios horarios use la tecla CTRL y haga click con el ratón en todas las opciones")
    accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
    paid = models.BooleanField(_('Paid'),default=False)
    def get_absolute_url(self):
        return '/intensivos/edit/%d/'%self.id
    def send_confirmation_email(self):
        ##Para el alumno
        subject = "Has solicitado un curso Intensivo en EIDE"
        
        html_content = u"""
<html>
<head>
        <link rel="stylesheet" href="https://matricula-eide.es/site_media/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://matricula-eide.es/site_media/static/css/extra.css">
</head>
<body>
<div class="well">
    Muchas gracias por la solicitud del curso: %s <br>
    <p>Pronto nos pondremos en contacto desde EIDE para darle más información.</p>
    <p>Gracias.</p>
</div>
<div class="well">
<p></p>
</div>
</body>
</html>
"""%(self.get_curso_display())
        
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        msg.send()
        
        ##Para el secretaria        
        subject = "[EIDE] Matricula curso intensivo"
        payload = {'registration': self}
        
        html_content = render_to_string('intensivos/detalle.html', payload)
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, ["moebius1984@gmail.com","secretaria@eide.es"])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        msg.send()

        ### Para los admins
        subject = u"[INTENSIVOS]Hay una nueva matrícula"
        message_body = u"""
Se ha dado de alta una nueva solictud de intensivo. 
Los datos son del solicitante son: 
Nombre: %s
Apellidos: %s
Telefono : %s
e-mail: %s

Curso: %s

Para mas detalle visitar:
https://matricula-eide.es/intensivos/list/

"""%(self.name,self.surname,self.telephone,self.email,self.get_curso_display)
        message_html = u"""
<html>
<body>      
Se ha dado de alta una nueva solictud de intensivo: 
Los datos son del solicitante son: 
<table>
<tr>
    <td>Nombre:</td><td> %s</td>
</tr>
<tr>
    </d>Apellidos:</td><td> %s</td>
</tr>
<tr>
    <td>Teléfono:</td><td> %s</td>
</tr>

<tr>
    <td>e-mail:</td><td> %s</td>
</tr>
<tr>
    <td>Curso</td><td>%s</td>
</tr>
</table>
Para mas detalle visitar:
<a href="https://matricula-eide.es/intesivos/list/">Lista</a>
</body> 
"""%(self.name,self.surname,self.telephone,self.email,self.get_curso_display)
        
        mail_admins(subject, message_body,False,None,message_html)
        
    def __unicode__(self):
        return u"%s-%s"%(self.id,self.email)
    def registration_name(self):
        return self.__unicode__()
   
        
