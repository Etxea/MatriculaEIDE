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
from django.template.loader import render_to_string

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

NIVELES_ESTUDIOS = (
    (0, _('Sin titulación')),
    (1, _('ESO')),
    (2, _('Graduado Escolar')),
    (3, _('Bachillerato, COU o similar')),
    (4, _('FPII o Técnico FP Grado Superior')),
    (5, _('Estudios Universitarios.')),
)

CURSOS = (
	(0, _('Otros')),
    (1, _('Certificado de Profesionalidad de nivel 1 del área de Hostelería y Turismo')),
    (2, _('Certificado de Profesionalidad de nivel 2 del área de Hostelería y Turismo')),
    (3, _('Certificado de Profesionalidad de cualquier área de nivel 3')),
)
TIEMPO_DESEMPLEO = (
    (0, _('Menos de 12 meses.')),
    (1, _('Más de 12 meses.')),
)



class Registration(models.Model):
	password = models.CharField(_('Password'),max_length=6,blank=True,editable=False,default="  ")
	registration_date = models.DateField(default=datetime.date.today, auto_now_add=True,editable=False)
	curso_1 = models.BooleanField('Certificado de Profesionalidad en Dirección y Producción en Cocina')
	curso_2 = models.BooleanField('Certificado de Profesionalidad en Dirección en Restauración')
	name = models.CharField(_('Nombre (*)'),max_length=50)
	surname = models.CharField(_('Apellido(s) (*)'),max_length=100)
	location = models.CharField(_('Localidad (*)'),max_length=100)
	birth_date = models.DateField(_('Fecha Nacimiento (*)'),help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
	telephone_movil = models.CharField('Tel. Móvil (*)',max_length=12)
	telephone_fijo = models.CharField('Tel. Fijo',max_length=12,blank=True)
	email = models.EmailField('Email (*)')
	
	nivel_estudios = models.DecimalField(_('Estudios (*)'),help_text="*La titulación está ordenada de la más baja a la más alta. Debe seleccionar la titulación más alta que tenga. <br> **Titulación obtenida en el extranjero: En caso de estudios realizados en el extranjero, sólo indicar los estudios que están homologados en España. Si no están homologados, indicar la titulación más alta que tenga homologada en España o, si no tiene titulación homologada en España, seleccione la opción 'sin estudios'. ",max_digits=1, decimal_places=0,choices=NIVELES_ESTUDIOS,default=0,blank=True)
	
	curso_previo = models.BooleanField(_('¿Ha realizado alguna vez un Certificado de Profesionalidad o curso de COCINA?'), help_text=_(' ¿Ha realizado alguna vez un Certificado de Profesionalidad o curso de COCINA?'),blank=True)
	curso_previo_tipo = models.DecimalField(_('Tipo curso previo'),help_text="¿De qué tipo?",max_digits=1, decimal_places=0,choices=CURSOS, blank=True,default=0)
	
	experiencia_previa = models.BooleanField(_('Experiencia previa'), help_text=_('Ha realizado algún curso de cocina o tiene experiencia en cocina o restauración'),blank=True)
	experiencia_previa_actividad = models.CharField(_('Especifique'),max_length=200, blank=True)
	
	desempleado = models.BooleanField(_('Desempleado'), help_text=_('Haga click en el check si se encuentra en situación de desempleo'),blank=True)
	
	trabajador_baja_cual = models.BooleanField(_('Trabajador de baja cualificación'), help_text=_('¿Es usted trabajador de baja cualificación? Se considera trabajador de baja cualificación los incluidos en los grupos de cotización 06, 07, 09 o 10. '),blank=True)
	
	trabajo_previo = models.BooleanField(_('Trabajador previo'), help_text=_('¿Ha tenido alguna vez algún contrato de trabajo?'),blank=True)
	tiempo_desempleo = models.DecimalField(_('Tiempo inscrito desempleo. previo'), help_text=_('¿Cuánto tiempo lleva desempleado e inscrito como tal en Lanbide o Servicio de Empleo de su provincia correspondiente de los últimos 18 meses?'),blank=True,max_digits=1, decimal_places=0,choices=TIEMPO_DESEMPLEO,default=0)
	
	accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=False,blank=True)
		
	def send_confirmation_email(self):
		##Para el alumno
		subject = "Has solicitado un curso de COCINA en EIDE"
		
		html_content = u"""
<html>
<body>
<div class="well">
    <p>Acaba de realizar una solicitud para el curso de COCINA en EIDE. Le agradecemos su solicitud.</p>
	<p>En caso de que convoquemos un curso de los que solicita y cumpla los requisitos, no pondremos en contacto con usted para realizar un proceso de selección.</p>
</div>
</body>
</html>
"""
		
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg.attach_alternative(html_content, "text/html")
		##msg.content_subtype = "html"
		msg.send()
		
		##Para el secretaria
		
		subject = "[COCINA] nueva solicitud desde la Web"
		payload = {'registration': self}
		
		html_content = render_to_string('cocina/detalle.html', payload)
		
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, ["moebius1984@gmail.com","secretaria@eide.es"])
		msg.attach_alternative(html_content, "text/html")
		msg.content_subtype = "html"
		msg.send()



		 
		### Para los admins
		subject = "[COCINA] Hay una nueva solicitud"
		message_body = u"""
Se ha dado de alta una nueva solictud de COCINA. 
Los datos son del solicitante son: 
Nombre: %s
Apellidos: %s
Telefono Fijo: %s
Telefono Móvil: %s
e-mail: %s

Desempleado: %s

Para mas detalle visitar:
https://matricula-eide.es/cocina/view/%s/

o para le listado completo

https://matricula-eide.es/cocina/list/

"""%(self.name,self.surname,self.telephone_fijo,self.telephone_movil,self.email,self.desempleado,self.id)
		message_html = u"""
<html>
<body>		
Se ha dado de alta una nueva solictud de COCINA. 
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
<a href="https://matricula-eide.es/cocina/list/">Lista</a>
</body>	
"""%(self.name,self.surname,self.telephone_fijo,self.telephone_movil,self.email)
		
		mail_admins(subject, message_body,False,None,message_html)
		
	def __unicode__(self):
		return u"%s-%s"%(self.id,self.email)
	#def get_detail_url(self):
		#return reverse('COCINA_view',args=[self.id])
		#return "/COCINA/view/%d/"%self.id
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
			#Ajustamos algunas variables que no están definidas
			if self.tiempo_desempleo == "":
				self.tiempo_desempleo=0
			
			if not self.curso_previo:
				self.curso_previo_tipo=0
			#We send a confirmation mail to te registrant and a advise mail to the admins
			#~ print "vamos a guardar",self
		super(Registration, self).save(*args, **kwargs)
		self.send_confirmation_email()
		
