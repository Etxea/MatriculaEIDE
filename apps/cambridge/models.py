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

EXAM_TYPE = (
    (1, _('Paper Based')),
    (2, _('Computer Based')),
)


class Level(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	def __unicode__(self):
		return "%s-%se"%(self.name,self.price)
	
class BaseExam(models.Model):
	level = models.ForeignKey(Level)
	exam_date =  models.DateField(default=datetime.date.today)
	registration_start_date =  models.DateField(default=datetime.date.today)
	
	class Meta:
		abstract = True

class Exam(BaseExam):
	def registrations(self):
		try:
			return self.registration_set.count()
		except:
			return 0
	
	def paid_registrations(self):
		try:
			return self.registration_set.filter(paid=True).count()
		except:
			return 0
	
	def __unicode__(self):
		return "%s %s %s"%(_('Exam'),self.exam_date,self.level)
	
class SchoolExam(BaseExam):
	def __unicode__(self):
		return "School Exam %s %s"%(self.exam_date,self.level)


class ComputerBasedExam(BaseExam):
	def registrations(self):
		try:
			return self.computerbasedregistration_set.count()
		except:
			return 0
	
	def paid_registrations(self):
		try:
			return self.computerbasedregistration_set.filter(paid=True).count()
		except:
			return 0
	
	def __unicode__(self):
		return "%s %s %s"%(_('Computer Based Exam'),self.exam_date,self.level)
	

#Asbtract model to inherit from him
class BaseRegistration(models.Model):
	password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
	name = models.CharField(_('Name'),max_length=50)
	surname = models.CharField(_('Surname'),max_length=100)
	address = models.CharField(_('Address'),max_length=100)
	location = models.CharField(_('Location'),max_length=100)
	postal_code = models.DecimalField(_('Postal Code'),max_digits=6, decimal_places=0)
	sex = models.DecimalField(_('Sex'),max_digits=1, decimal_places=0,choices=SEXO)
	birth_date = models.DateField(_('Birth Date'))
	dni = models.CharField(max_length=9)
	telephone = models.CharField(_('Telephone'),max_length=12)
	email = models.EmailField()
	eide_alumn = models.BooleanField(_('EIDE Alumn'), help_text=_('Check this if you are an alumn of EIDE. If not please fill in your centre name'))
	centre_name = models.CharField(_('Centre Name'),max_length=100, blank=True)
	
	registration_date = models.DateField(default=datetime.date.today, auto_now_add=True)
	paid = models.BooleanField(_('Paid'),default=False)
	accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'))

	def send_confirmation_email(self):
		subject = "De momento solo un mail de prueba"
		message_body = "Se ha registrado para el examen %s de cambridge blablabla y lalalal y lelele"%self.exam
		send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		subject = "Hay una nueva matricula para cambridge"
		message_body = """Se ha dado de alta una nueva matricula para el examen %s. Entre 
			en http://matrocilas.eide.es/cambridge/ para revisarla si quiere"""%self.exam
		mail_admins(subject, message_body)
	def send_paiment_confirmation_email(self):
		subject = "Confirmación de la recepción del pago para el examen %s"%self.exam
		message_body = "Se ha registrado para el examen %s de cambridge blablabla y lalalal y lelele"%self.exam
		send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		subject = "Hay una nueva matricula para cambridge"
		message_body = """Se ha dado de alta una nueva matricula para el examen %s. Entre 
			en http://matrocilas.eide.es/cambridge/ para revisarla si quiere"""%self.exam
		mail_admins(subject, message_body)
	def __unicode__(self):
		return "%s-%s"%(self.registration_date,self.dni)
	def save(self, *args, **kwargs):
		##We generate a random password
		if self.id is not None:
			if self.paid:
				self.send_paiment_confirmation_email()
		
		else:
			#We set de password, not used roght now
			self.password = ''.join([choice(letters) for i in xrange(6)])
			#We send a confirmation mail to te registrant and a advise mail to the admins
			self.send_confirmation_email()
		super(BaseRegistration, self).save(*args, **kwargs)
		
	class Meta:
		abstract = True

class Registration(BaseRegistration):
	#asignames los examenes del tipo adecuado y solo mostramos los que están en fecha
	exam = models.ForeignKey(Exam,\
		limit_choices_to = {'registration_start_date__lte': datetime.date.today,\
		'exam_date__gte': datetime.date.today})


class SchoolRegistration(BaseRegistration):
	#asignames los examenes del tipo adecuado y solo mostramos los que están en fecha
	exam = models.ForeignKey(SchoolExam,\
		limit_choices_to = {'registration_start_date__lte': datetime.date.today,\
		'exam_date__gte': datetime.date.today})
	
class ComputerBasedRegistration(BaseRegistration):
	#asignames los examenes del tipo adecuado y solo mostramos los que están en fecha
	exam = models.ForeignKey(ComputerBasedExam,\
		limit_choices_to = {'registration_start_date__lte': datetime.date.today, \
		'exam_date__gte': datetime.date.today})
	
