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
from django.template.loader import render_to_string

from random import choice
from string import letters
import datetime
import sys

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
    (1, _('PB')),
    (2, _('CB')),
    (3, _('FS PB')),
    (4, _('FS CB')),
)


class Level(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __unicode__(self):
        try:
            return "[%s] %s-%s"%(self.schoollevel.school,self.name.split(" ")[0],self.price)
	
        except:
            return "%s-%s"%(self.name,self.price)
    

class Exam(models.Model):
    exam_type =  models.DecimalField(_('Tipo Examen'),max_digits=1, decimal_places=0,choices=EXAM_TYPE)
    level = models.ForeignKey(Level)
    exam_date =  models.DateField(default=datetime.date.today)
    registration_end_date =  models.DateField(_('Fecha fin de la matriculación'),default=datetime.date.today)
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
    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return "%s %s %s"%(self.level,self.get_exam_type_display(),self.exam_date.strftime('%d-%m-%Y'))

class School(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    description = models.CharField(_('Description'),max_length=100,default="")
    password = models.CharField(_('Password'),max_length=50)
    def __unicode__(self):
        return self.name
    def exam_count(self):
        return self.schoolexam_set.all().count()
    def registration_count(self):
        total=0
        for e in self.schoolexam_set.all():
            total = total + e.registration_set.all().count()
        return total

class Venue(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    description = models.CharField(_('Description'),max_length=100,default="")
    password = models.CharField(_('Password'),max_length=50)
    def __unicode__(self):
        return self.name
    def exam_count(self):
        return self.venueexam_set.all().count()
    def registration_count(self):
        total=0
        for e in self.venueexam_set.all():
            total = total + e.registration_set.all().count()
        return total

class SchoolLevel(Level):
    school = models.ForeignKey(School)

class SchoolExam(Exam):
    school = models.ForeignKey(School)
    def __unicode__(self):
        return "%s %s"%(self.level.__unicode__(),self.exam_date.strftime('%d-%m-%Y'))

class VenueExam(Exam):
    venue = models.ForeignKey(Venue)
    def __unicode__(self):
        return "[%s] %s %s"%(self.venue,self.level.__unicode__(),self.exam_date.strftime('%d-%m-%Y'))


class Registration(models.Model):
    exam = models.ForeignKey(Exam,limit_choices_to = {'registration_end_date__gt': datetime.date.today})
    password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
    name = models.CharField(_('Name'),max_length=50)
    surname = models.CharField(_('Surname'),max_length=100)
    address = models.CharField(_('Address'),max_length=100)
    location = models.CharField(_('Location'),max_length=100)
    postal_code = models.DecimalField(_('Postal Code'),max_digits=6, decimal_places=0)
    sex = models.DecimalField(_('Sex'),max_digits=1, decimal_places=0,choices=SEXO)
    birth_date = models.DateField(_('Birth Date'),help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    #dni = models.CharField(max_length=9,blank=True,help_text=_('Introduce el DNI completo con la letra sin espacios ni guiones'))
    telephone = models.CharField(_('Telephone'),max_length=12)
    email = models.EmailField()
    eide_alumn = models.BooleanField(_('EIDE Alumn'), help_text=_('Check this if you are an alumn of EIDE. If not please fill in your centre name'))
    centre_name = models.CharField(_('Centre Name'),max_length=100, blank=True) 
    registration_date = models.DateField(default=datetime.date.today, auto_now_add=True)
    paid = models.BooleanField(_('Paid'),default=False)
    accept_conditions = models.BooleanField(_('Accept the conditions'), help_text=_('You must accept the conditions to register'),default=True,blank=True)
    accept_photo_conditions = models.BooleanField(_('Aceptar las conficiones de la foto.'), help_text=_('Debes aceptar las condiciones de la la toma de foto para poder matricularte.'),default=True,blank=True)
    minor = models.BooleanField(_('El candidato es menor de edad y yo soy su padre/madre o tutor legal.'),default=False,blank=True)
    tutor_name = models.CharField(_('Nombre de padre/madre o tutor.'),max_length=50,blank=True)
    tutor_surname = models.CharField(_('Apellido(s) del padre/madre o tutor.'),max_length=100,blank=True)

    def send_confirmation_email(self):
        ##Para el alumno
        subject = "Te has matriculado para un examen Cambridge en EIDE"
        
        html_content = u"""
        


<div class="well">
    Acaba de realizar una solicitud de matrícula para: <br />
    %s 
</div>
<div class="well">
    <h1>Pago de la matrícula</h1>
    La matrícula se hará efectiva una vez se haya recibido el pago. Puede hacer el pago en la siguiente dirección: <a href="http://matricula-eide.es/%s">http://matricula-eide.es/%s</a>
</div>"""%(self.exam,self.generate_payment_url(),self.generate_payment_url())
        
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        #msg.send()
         
        ### Para los admins
        subject = "Hay una nueva matricula (sin pagar) para cambridge %s"%self.exam
        message_body = u"""Se ha dado de alta una nueva matricula para el examen %s. 
Los datos son del alumno son: 
    Nombre: %s
    Apellidos: %s
    Telefono: %s
    e-mail: %s
"""%(self.exam,self.name,self.surname,self.telephone,self.email)
        #mail_admins(subject, message_body)
    def send_paiment_confirmation_email(self):
        subject = "Se ha confirmado el pago de la matricula para el examen %s"%self.exam
        html_content=u"""<html><body>
        <h2>CONFIRMACIÓN DE MATRÍCULA</h2>
<p>Se ha matriculado para el examen <b> %s </b> en la fecha <b> %s </b>. Tras el cierre del periodo de matriculación se le enviará el COE (Confirmation of Entry) 
con las fechas y horas del examen escrito y oral a la dirección de e-mail que ha proporcionado el candidato en la 
hoja de matrícula. Si dos semanas antes de la fecha del examen el candidato no ha recibido el COE, es su responsabilidad 
el ponerse en contacto con EIDE y solicitar el COE. EIDE no se responsabiliza del extravío o no recepción del mismo y no 
asume ninguna responsabilidad por cualquier problema derivado del desconocimiento de la fecha, horario y lugar del examen 
y se reserva el derecho de no admitir a candidatos que lleguen tarde.</p>

<p>Es responsabilidad del candidato llegar al lugar del examen con 15 minutos de antelación. Los candidatos deben traer un 
DNI o pasaporte que atestigüe su identidad en cada examen (escrito y oral).</p>
        """%(self.exam,self.exam.exam_date)
	#html_content= html_content+render_to_string('cambridge/legal.html')
        html_content= html_content+u"""</body></html>"""
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        msg.send()
        
        subject = "[cambridge] Se ha confirmado el pago de una matrcicula"
        message_body = u"""Se acaba de confirmar el pago de un matricula para examen %s. \n 
Los datos son:\n
ID de la mátricula: %s \n 
Nombre: %s \n Apellidos: %s \n
Puedes ver más detalles e imprimirla en la siguente url http://matricula-eide.es/cambridge/edit/%s/
"""%(self.exam,self.id,self.name,self.surname,self.id)
        mail_admins(subject, message_body)
    def set_as_paid(self):
        self.paid = True
        self.save()
        self.send_paiment_confirmation_email()
        
    def __unicode__(self):
        return "%s-%s"%(self.id,self.exam)
    def registration_name(self):
        #return "%s - %s, %s"%(self.exam,self.surname,self.name)
	try:
	    return "%s"%(self.exam.level.schoollevel.__unicode__())
	except:
            return "%s"%(self.exam)
    def save(self, *args, **kwargs):
        ##We generate a random password
        if self.id is not None:
            if self.paid:
                self.send_paiment_confirmation_email()      
        else:
            #We set th password, not used right now
            self.password = ''.join([choice(letters) for i in xrange(6)])
            #COmprobamos si es un schoolexam
            try:
                if isinstance(self.exam.schoolexam,SchoolExam):
                    self.minor=True
                    self.eide_alumn=False
                    self.centre_name=self.exam.schoolexam.school.name
            except:
                pass
            #We send a confirmation mail to te registrant and a advise mail to the admins
            self.send_confirmation_email()
        super(Registration, self).save(*args, **kwargs)
        
    
    
    def generate_payment_url(self):
        return '/pagos/cambridge/%s/'%(self.id)
