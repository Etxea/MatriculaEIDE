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
    (1, _('Elementary/Upper: Mañana (72h)')),
    (2, _('Elementary/Upper: Tarde (72h)')),
    (3, _('FCE/CAE: Mañana (72h)')),
    (4, _('FCE/CAE: Tarde (72h)')),
    (5, _('FCE/CAE: Tarde (54h)')),
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

class Registration(models.Model):
	curso = models.DecimalField('Curso',max_digits=1, decimal_places=0,choices=CURSO)
	password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
	name = models.CharField(_('Nombre (*)'),max_length=50)
	surname = models.CharField(_('Apellido(s) (*)'),max_length=100)
	address = models.CharField(_('Address'),max_length=100)
	location = models.CharField(_('Location'),max_length=100)
	birth_date = models.DateField(_('Birth Date'),help_text=_('Formato: AAAA-MM-DD(año-mes-día)'))
	telephone = models.CharField('Tel. Fijo (*)',max_length=12)
	email = models.EmailField('Email (*)')
	registration_date = models.DateField(default=datetime.date.today, auto_now_add=True)
	nivel_ingles = models.DecimalField(_('Nivel Ingles Actual'),help_text="",max_digits=1, decimal_places=0,choices=NIVELES_IDIOMAS,blank=True,null=True)
	accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
	paid = models.BooleanField(_('Paid'),default=False)
	
	def send_confirmation_email(self):
		##Para el alumno
		subject = "Has solicitado un curso Intensivo en EIDE"
		
		html_content = u"""
<html>
<body>
<div class="well">
    Acaba de realizar una solicitud de curso para: <br />
    %s <br>
</div>
<div class="well">
<p></p>
</div>
</body>
</html>
"""%(self.curso)
		
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg.attach_alternative(html_content, "text/html")
		##msg.content_subtype = "html"
		msg.send()
		
		##Para el secretaria
		
		subject = "[EIDE] Matrícula curso intensivo"
		payload = {'registration': self}
		
		html_content = render_to_string('intensivos/detalle.html', payload)
		
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, ["moebius1984@gmail.com","secretaria@eide.es"])
		msg.attach_alternative(html_content, "text/html")
		##msg.content_subtype = "html"
		msg.send()



		 
		### Para los admins
		subject = "[INTENSIVOS]Hay una nueva matrícula"
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

"""%(self.name,self.surname,self.telephone,self.email,self.curso)
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
	<td>e-mail:</td><td> %s</td>
</tr>
<tr>
	<td>Curso</td><td>%s</td>
</tr>
</table>
Para mas detalle visitar:
<a href="https://matricula-eide.es/intesivos/list/">Lista</a>
</body>	
"""%(self.name,self.surname,self.telephone,self.email,self.curso)
		
		mail_admins(subject, message_body,False,None,message_html)
		
	def __unicode__(self):
		return u"%s-%s"%(self.id,self.email)
	#def get_detail_url(self):
		#return reverse('hobetuz_view',args=[self.id])
		#return "/hobetuz/view/%d/"%self.id
	def registration_name(self):
		#return "%s - %s, %s"%(self.exam,self.surname,self.name)
		#~ return "%s"%(self.exam)
		return self.__unicode__()
	#Antes de guardar hacemos algunas cosas, como generar password y enviar un mail
	def save(self, *args, **kwargs):
		##We generate a random password
		if self.id is None:
			#We set de password, not used right now
			self.password = ''.join([choice(letters) for i in xrange(6)])
			#We send a confirmation mail to te registrant and a advise mail to the admins
			self.send_confirmation_email()
		super(Registration, self).save(*args, **kwargs)
		
