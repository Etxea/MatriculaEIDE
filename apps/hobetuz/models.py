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
from django.contrib.localflavor import generic
from django.contrib.localflavor.es.forms import *
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse

from random import choice
from string import letters
import datetime

from django.conf import settings

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, mail_admins
else:
    from django.core.mail import send_mail, mail_admins

from django.utils.translation import gettext_lazy as _
# Create your models here.

SEXO = (
    (1, _('Male')),
    (2, _('Female')),
)

TITULACION = (
    (1, _('Sin titulación')),
    (2, _('Graduado Escolar o ESO')),
    (3, _('Bachillerato, COU o similar')),
    (4, _('Grado, Licenciatura o Diplomatura')),
    (5, _('Certificado de Profesionalidad en Turismo y Hostelería de Nivel 1')),
    (6, _('Certificado de Profesionalidad en Turismo y Hostelería de Nivel 2 o 3')),
    (7, _('Ciclo Grado Medio, FPI, Certificado de Profesionalidad de Nivel 2 en otra especialidad')),
    (8, _('Ciclo de Grado Superior, FPII; Certificado de Profesionalidad de Nivel 3 en otra especialidad')),
 
)

NIVELES_IDIOMAS = (
    (1, _('Cero')),
    (2, _('Inicial')),
    (3, _('Intermedio')),
    (4, _('Avanzado')),
)

class Curso(models.Model):
	name = models.CharField(max_length=50)
	matricula_abierta = models.BooleanField(_('Matricula Abierta'),default=datetime.date.today)
	def __unicode__(self):
		return "Curso de %s"%(self.name)
	

#Asbtract model to inherit from him
class Registration(models.Model):
	curso = models.ForeignKey(Curso,verbose_name="Primera Opción (*)",limit_choices_to = {'matricula_abierta': True})
	curso2 = models.ForeignKey(Curso,verbose_name="Segunda Opción",limit_choices_to = {'matricula_abierta': True},blank=True,related_name="registration2_set",null=True)
	curso3 = models.ForeignKey(Curso,verbose_name="Tercera Opción",limit_choices_to = {'matricula_abierta': True},blank=True,related_name="registration3_set",null=True)
	curso4 = models.ForeignKey(Curso,verbose_name="Cuarta Opción",limit_choices_to = {'matricula_abierta': True},blank=True,related_name="registration4_set",null=True)
	curso5 = models.ForeignKey(Curso,verbose_name="Quinta Opción",limit_choices_to = {'matricula_abierta': True},blank=True,related_name="registration5_set",null=True)

	password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
	name = models.CharField(_('Nombre (*)'),max_length=50)
	surname = models.CharField(_('Apellido(s) (*)'),max_length=100)
	#~ address = models.CharField(_('Address'),max_length=100)
	#~ location = models.CharField(_('Location'),max_length=100)
	#~ postal_code = models.DecimalField(_('Postal Code'),max_digits=6, decimal_places=0)
	#~ sex = models.DecimalField(_('Sex'),max_digits=1, decimal_places=0,choices=SEXO)
	#~ birth_date = models.DateField(_('Birth Date'),help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
	#dni = models.CharField(max_length=9,blank=True,help_text=_('Introduce el DNI completo con la letra sin espacios ni guiones'))
	telephone = models.CharField('Tel. Fijo (*)',max_length=12)
	telephone2 = models.CharField('Tel. Móvil (*)',max_length=12)
	email = models.EmailField('Email (*)')
	
	titulacion = models.DecimalField(_('Titulación (*)'),max_digits=1, decimal_places=0,choices=TITULACION)
	
	desempleado = models.BooleanField(_('Desempleado'), help_text=_('haga click en el check si se encuentra en situación de desempleo'))
	fecha_desempleo = models.DateField(default=datetime.date.today, blank=True, null=True)
	
	empresa_nombre = models.CharField(_('Nombre de la empresa'),max_length=100, blank=True)
	empresa_puesto = models.CharField(_('Puesto en la empresa'),max_length=100, blank=True)
	empresa_actividad = models.CharField(_('Actividad de la empresa'),max_length=200, blank=True)
	
	registration_date = models.DateField(default=datetime.date.today, auto_now_add=True)
	
	nivel_ingles = models.DecimalField(_('Nivel Ingles'),help_text="En caso de que halla escogido este diioma indique su nivel",max_digits=1, decimal_places=0,choices=NIVELES_IDIOMAS,blank=True,null=True)
	nivel_frances = models.DecimalField(_('Nivel Frances'),help_text="En caso de que halla escogido este diioma indique su nivel",max_digits=1, decimal_places=0,choices=NIVELES_IDIOMAS,blank=True,null=True)
	nivel_aleman = models.DecimalField(_('Nivel Aleman'),help_text="En caso de que halla escogido este diioma indique su nivel",max_digits=1, decimal_places=0,choices=NIVELES_IDIOMAS,blank=True,null=True)
	nivel_chino = models.DecimalField(_('Nivel Chino'),help_text="En caso de que halla escogido este diioma indique su nivel",max_digits=1, decimal_places=0,choices=NIVELES_IDIOMAS,blank=True,null=True)
	
	accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
	
	
	def send_confirmation_email(self):
		##Para el alumno
		subject = "Has solicitado un curso de HOBETUZ en EIDE"
		
		html_content = u"""
<html>
<body>
<div class="well">
    Acaba de realizar una solicitud de curso para: <br />
    %s <br>
    %s <br>
    %s <br>
    %s <br>
    %s <br>
</div>
<div class="well">
<p>En caso de que convoquemos un curso de los que solicita y cumpla los requisitos, no pondremos en contacto con usted para realizar un proceso de selección.</p>
</div>
</body>
</html>
"""%(self.curso,self.curso2,self.curso3,self.curso4,self.curso5)
		
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg.attach_alternative(html_content, "text/html")
		##msg.content_subtype = "html"
		msg.send()
		 
		### Para los admins
		subject = "[Hobetuz]Hay una nueva solicitud para Hobetuz"
		message_body = u"""
Se ha dado de alta una nueva solictud de hobetuz. 
Los datos son del solicitante son: 
Nombre: %s
Apellidos: %s
Telefono Fijo: %s
Telefono Móvil: %s
e-mail: %s

Curso1: %s
Curso2: %s
Curso3: %s
Curso4: %s
Curso5: %s

Para mas detalle visitar:
https://matricula-eide.es/%s

"""%(self.name,self.surname,self.telephone,self.telephone2,self.email,self.curso,self.curso2,self.curso3,self.curso4,self.curso5,self.get_detail_url())
		message_html = u"""
<html>
<body>		
Se ha dado de alta una nueva solictud de hobetuz. 
Los datos son del solicitante son: 
<table>
<tr>
	<td>Nombre:</td><td> %s</td>
</tr>
<tr>
	</d>Apellidos:</td><td> %s</td>
</tr>
<tr>
	<td>Telefono Fijo:</td><td> %s</td>
</tr>
<tr>
	<td>Telefono Móvil:</td><td> %s</td>
</tr>
<tr>
	<td>e-mail:</td><td> %s</td>
</tr>
</table>
Para mas detalle visitar:
<a href="https://matricula-eide.es/%s">Detalles</a>
</body>	
"""%(self.name,self.surname,self.telephone,self.telephone2,self.email,self.get_detail_url())
		
		mail_admins(subject, message_body,False,None,message_html)
		
	def __unicode__(self):
		return "%s-%s"%(self.id,self.email)
	def get_detail_url(self):
		return reverse('hobetuz_view',args=[self.id])
	def registration_name(self):
		#return "%s - %s, %s"%(self.exam,self.surname,self.name)
		#~ return "%s"%(self.exam)
		return self.__unicode__()
	#Antes de guardar ahaceos algunas cosas, como generar password y enviar un mail
	def save(self, *args, **kwargs):
		##We generate a random password
		if self.id is None:
			#We set de password, not used roght now
			self.password = ''.join([choice(letters) for i in xrange(6)])
			#We send a confirmation mail to te registrant and a advise mail to the admins
			self.send_confirmation_email()
		super(Registration, self).save(*args, **kwargs)
		
