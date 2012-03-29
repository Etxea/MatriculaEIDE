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
from datetime import datetime

from django.conf import settings

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, mail_admins
else:
    from django.core.mail import send_mail, mail_admins

# Create your models here.

SEXO = (
    (1, 'Male'),
    (2, 'Female'),
)

EXAM_TYPE = (
    (1, 'Normal'),
    (2, 'Computer Based'),
)


class Level(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	def __unicode__(self):
		return "%s-%se"%(self.name,self.price)
	
class BaseExam(models.Model):
	level = models.ForeignKey(Level)
	exam_date =  models.DateField()
	registration_date =  models.DateField()
	registration_open = models.BooleanField()
#	exam_type = models.DecimalField(max_digits=1, decimal_places=0,choices=EXAM_TYPE)
	class Meta:
		abstract = True

class Exam(BaseExam):
	def __unicode__(self):
		return "Exam %s %s"%(self.exam_date,self.level)
	
class SchoolExam(BaseExam):
	def __unicode__(self):
		return "School Exam %s %s"%(self.exam_date,self.level)


class ComputerBasedExam(BaseExam):
	def __unicode__(self):
		return "Computer Exam %s %s"%(self.exam_date,self.level)
	

#Asbtract model to inherit from him
class BaseRegistration(models.Model):
	password = models.CharField(max_length=6,blank=True,editable=False)
	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	postal_code = models.DecimalField(max_digits=6, decimal_places=0)
	sex = models.DecimalField(max_digits=1, decimal_places=0,choices=SEXO)
	birth_date = models.DateField()
	dni = models.CharField(max_length=9)
	telephone = models.CharField(max_length=12)
	email = models.EmailField(blank=True)
	eide_alumn = models.BooleanField()
	centre_name = models.CharField(max_length=100, blank=True)
	
	registration_date = models.DateField(auto_now_add=True)
	paid = models.BooleanField(default=False)
	accept_conditions = models.BooleanField()
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
	exam = models.ForeignKey(Exam,limit_choices_to = {'registration_date__gte': datetime.now, 'registration_open': True})


class SchoolRegistration(BaseRegistration):
	exam = models.ForeignKey(SchoolExam,limit_choices_to = {'registration_date__gte': datetime.now, 'registration_open': True})
	
class ComputerBasedRegistration(BaseRegistration):
	exam = models.ForeignKey(ComputerBasedExam,limit_choices_to = {'registration_date__gte': datetime.now, 'registration_open': True})
	
