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

from random import choice
from string import letters
from datetime import datetime
# Create your models here.

SEXO = (
    (1, 'Hombre'),
    (2, 'Mujer'),
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
	def __unicode__(self):
		return "%s-%s"%(self.exam_date,self.level)
	class Meta:
		abstract = True

class Exam(BaseExam):
	pass
	
class SchoolExam(BaseExam):
	pass

class ComputerBasedExam(BaseExam):
	pass

#Asbtract model to inherit from him
class BaseRegistration(models.Model):
	password = models.CharField(max_length=6,blank=True,editable=False)
	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	postal_code = models.DecimalField(max_digits=6, decimal_places=0)
	sex = models.DecimalField(max_digits=1, decimal_places=0,choices=SEXO)
	born_date = models.DateField()
	dni = models.CharField(max_length=9)
	telephone = models.CharField(max_length=12)
	email = models.EmailField(blank=True)
	eide_alumn = models.BooleanField()
	centre_name = models.CharField(max_length=100, blank=True)
	
	registration_date = models.DateField(auto_now_add=True)
	accept_conditions = models.BooleanField()
	def get_absolute_url(self):
		return "view/%s"%self.id
	def __unicode__(self):
		return "%s-%s"%(self.registration_date,self.dni)
	def save(self, *args, **kwargs):
		#We generate a random password
		self.password = ''.join([choice(letters) for i in xrange(6)])
		super(Registration, self).save(*args, **kwargs)
	class Meta:
		abstract = True

class Registration(BaseRegistration):
	exam = models.ForeignKey(Exam,limit_choices_to = {'registration_date__gte': datetime.now, 'registration_open': True})


class SchoolRegistration(BaseRegistration):
	exam = models.ForeignKey(SchoolExam,limit_choices_to = {'registration_date__gte': datetime.now, 'registration_open': True})
	
class ComputerBasedRegistration(BaseRegistration):
	exam = models.ForeignKey(ComputerBasedExam,limit_choices_to = {'registration_date__gte': datetime.now, 'registration_open': True})
	
