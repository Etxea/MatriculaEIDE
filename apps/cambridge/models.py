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
    (1, _('PB')),
    (2, _('CB')),
    (3, _('FS PB')),
    (4, _('FS CB')),
)


class Level(models.Model):
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	def __unicode__(self):
		return "%s-%se"%(self.name,self.price)
	

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
		return "%s %s %s"%(self.level.name,self.get_exam_type_display(),self.exam_date.strftime('%d-%m-%Y'))
	def __unicode__(self):
		return "%s %s %s"%(self.level.name,self.get_exam_type_display(),self.exam_date.strftime('%d-%m-%Y'))
	
#Asbtract model to inherit from him
class Registration(models.Model):
	exam = models.ForeignKey(Exam,limit_choices_to = {'registration_end_date__gte': datetime.date.today})
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
    La matrícula se hará efectiva una vez se haya recibido el pago. El pago puede realizarse de 2 formas: con tarjeta bancaria a través de una plataforma online o por transferencia bancaria.
</div>

<div class="well">
    <p><b>A. ONLINE  CON TARJETA BANCARIA</b>, a través de una <b>pasarela de pago segura</b> de la CECA 
    (Confederación Española de Cajas de Ahorro), que garantiza <b>total seguridad. </b></p>
    <p>Una vez efectuado el pago, recibirá un mail de confirmación. Si no recibe dicha comunicación en el plazo de 2 días hábiles, póngase en contacto con nosotros a través del mail o teléfono indicados abajo.</p>
    <a href="http://matricula-eide.es/%s">REALIZAR EL PAGO ONLINE CON TARJETA BANCARIA</a>    
</div>

<div class="well">
    <p><b>B. A través de TRANSFERENCIA BANCARIA O INGRESO.</b></p>
<ul>
    <li>Cuenta Bancaria (Kutxabank – BBK): <b>2095 0553 50 9108403919</b></li>
    <li>Concepto: %s-%s %s %s</li>
    <li>Importe: <b>%s</b>€</li>
</ul>
<p>Cuando realice el ingreso es recomendable adjuntar una copia del justificante de transferencia por mail, 
fax o comunicarnos que ha hecho la transferencia por teléfono. Tenga en cuenta que las transferencias pueden 
demorarse hasta 3 días y sólo se confirmará la matrícula cuando recibamos el importe en nuestra cuenta bancaria. 
En caso de que el plazo de matrícula sea muy ajustado, es recomendable optar por ingreso bancario, pago 
con tarjeta o pago en metálico en EIDE. Una vez recibido el pago, recibirá un mail de confirmación. Si no 
recibe dicha comunicación en el plazo de 4 días hábiles, póngase en contacto con nosotros a través del mail 
o teléfono indicados abajo. </p>
</div>

<div class="well">
    <h1>DATOS DE CONTACTO</h1>
    <ul>
        <li>Mail: <a href="mailto:/eide@eide.es">eide@eide.es</a></li>
        <li>Tel: 94 493 70 05</li>
        <li>Fax: 94 461 57 23</li>
        <li>Dirección: Genaro Oraá 6 - 48980 Santurtzi</li>
    </ul>
</div>"""%(self.exam,self.generate_payment_url(),self.exam.level,self.exam.exam_date,self.name,self.surname,self.exam.level.price)
		
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg.attach_alternative(html_content, "text/html")
		##msg.content_subtype = "html"
		msg.send()
		 
		### Para los admins
		subject = "Hay una nueva matricula (sin pagar) para cambridge %s"%self.exam
		message_body = u"""Se ha dado de alta una nueva matricula para el examen %s. 
Los datos son del alumno son: 
	Nombre: %s
	Apellidos: %s
	Telefono: %s
	e-mail: %s
"""%(self.exam,self.name,self.surname,self.telephone,self.email)
		mail_admins(subject, message_body)
	def send_paiment_confirmation_email(self):
		subject = "Se ha confirmado el pago de la matricula para el examen %s"%self.exam
		html_content=u"""<html><body>
		<h2>CONFIRMACIÓN DE MATRÍCULA</h2>
<p>Se ha matriculado para el examen <b> %s </b> en la fecha <b> %s </b>. En unos días, se le enviará el COE (Confirmation of Entry) 
con las fechas y horas del examen escrito y oral a la dirección de e-mail que ha proporcionado el candidato en la 
hoja de matrícula. Si dos semanas antes de la fecha del examen el candidato no ha recibido el COE, es su responsabilidad 
el ponerse en contacto con EIDE y solicitar el COE. EIDE no se responsabiliza del extravío o no recepción del mismo y no 
asume ninguna responsabilidad por cualquier problema derivado del desconocimiento de la fecha, horario y lugar del examen 
y se reserva el derecho de no admitir a candidatos que lleguen tarde.</p>

<p>Es responsabilidad del candidato llegar al lugar del examen con 15 minutos de antelación. Los candidatos deben traer un 
DNI o pasaporte que atestigüe su identidad en cada examen (escrito y oral).</p>

<p>Le recordamos las condiciones generales que ha aceptado del examen para el que acaba de matricularse.</p>
		
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>1.NORMATIVA
		GENERAL</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Para
		llevar a cabo una sesión de examen debe haber al menos un mínimo de
		4 candidatos por nivel.</FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">La
		tasa de inscripción es válida sólo para la convocatoria en la que
		se ha inscrito&nbsp; y no es transferible a otro examen o a
		convocatorias posteriores. Dichas tasas <B>NO</B> se devuelven al
		candidato en caso de que éste no se presente a parte o a ninguno de
		los exámenes. </FONT></FONT>
		</P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><SPAN STYLE="background: #ffff00">Se
		enviará el </SPAN></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B><SPAN STYLE="background: #ffff00">COE
		(</SPAN></B></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><I><B><SPAN STYLE="background: #ffff00">Confirmation
		of Entry</SPAN></B></I></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B><SPAN STYLE="background: #ffff00">)</SPAN></B></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><SPAN STYLE="background: #ffff00">
		con la </SPAN></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B><SPAN STYLE="background: #ffff00">fecha
		y hora del examen escrito y oral </SPAN></B></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><SPAN STYLE="background: #ffff00">a
		la dirección de e-mail que ha proporcionado el candidato en la hoja
		de matrícula. Si dos semanas antes de la fecha del examen el
		candidato no ha recibido el COE, es </SPAN></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B><SPAN STYLE="background: #ffff00">su
		responsabilidad</SPAN></B></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><SPAN STYLE="background: #ffff00">
		el ponerse en contacto con </SPAN></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><I><B><SPAN STYLE="background: #ffff00">EIDE</SPAN></B></I></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><SPAN STYLE="background: #ffff00">
		y solicitar el COE.</SPAN></FONT></FONT> <FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><I><B>EIDE</B></I></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">
		no se responsabiliza del extravío o no recepción del mismo y no
		asume ninguna responsabilidad por cualquier problema derivado del
		desconocimiento de la fecha, horario y lugar del examen y se reserva
		el derecho de no admitir a candidatos que lleguen tarde.</FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Es
		responsabilidad del candidato llegar al lugar del examen con <B>15
		minutos de antelación</B>. Los candidatos deben traer un <B>DNI o
		pasaporte</B> que atestigüe su identidad en cada examen (escrito y
		oral).</FONT></FONT></P>
		<P ALIGN=JUSTIFY>&nbsp;</P>
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>2.
		CANCELACIONES</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Solo
		se admitirán cancelaciones de matrículas hasta la fecha tope de
		matrícula indicada en el reverso. El candidato recibirá la
		devolución de la tasa de examen descontándose la cantidad de 35 €
		en concepto de gastos de administración. Pasada esta fecha sólo se
		admitirán cancelaciones por causas médicas en cuyo caso el
		candidato deberá rellenar un formulario solicitando dicha
		cancelación y adjuntar un CERTIFICADO MÉDICO OFICIAL. En este caso
		también se procederá a realizar una devolución de la tasa de
		examen menos 35 € por gastos administrativos. No se admitirán
		certificados médicos pasados 15 días de la fecha del examen
		escrito. No se admitirá ningún&nbsp; cambio o cancelación por
		otros motivos que no sean médicos después del último día de
		matrícula.</FONT></FONT></P>
		<P ALIGN=JUSTIFY>&nbsp;</P>
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>3.
		CANDIDATOS CON NECESIDADES ESPECIALES</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">En
		caso de que un candidato padezca alguna deficiencia/minusvalía
		(déficit auditivo, problemas de habla, etc.) y ésta le impida
		realizar los exámenes en igualdad de condiciones que el resto de
		candidatos, le informamos que deberá presentar un certificado médico
		oficial de su discapacidad/minusvalía <U><B>en el momento de
		matricularse</B></U>. Ese certificado será enviado a la Universidad
		de Cambridge ESOL Examinations para que decida las condiciones en las
		que ese candidato debe realizar los exámenes. <I><B>EIDE </B></I>no
		podrá realizar ninguna gestión para la modificación de los
		exámenes de los candidatos que no informen de su discapacidad con la
		suficiente antelación (es decir, durante la matriculación).</FONT></FONT></P>
		<P ALIGN=JUSTIFY>&nbsp;</P>
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>4.
		REVISIÓN DE RESULTADOS</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Si
		algún candidato no está conforme con su resultado, podrá solicitar
		una revisión. La revisión de resultados se debe solicitar en la
		Secretaría de <I><B>EIDE</B></I> siendo necesario seguir el
		procedimiento establecido por la Universidad de Cambridge.</FONT></FONT></P>
		<P ALIGN=JUSTIFY STYLE="margin-left: 0.64cm"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B>1.</B></FONT></FONT><SPAN STYLE="font-variant: normal"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B>&nbsp;&nbsp;&nbsp;&nbsp;
		</B></FONT></FONT></SPAN><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B>Primera
		revisión:</B></FONT></FONT> <FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Revisión
		clerical de la suma de los puntos: </FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B>25,00
		€</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">2.</FONT></FONT><SPAN STYLE="font-variant: normal"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">&nbsp;&nbsp;&nbsp;&nbsp;
		</FONT></FONT></SPAN><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B>Segunda
		revisión:</B></FONT></FONT> <FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Corrección
		de los exámenes escritos exceptuando el examen oral: </FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><B>110,00
		€.</B></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">
		Este importe deberá abonarse en </FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt"><I><B>EIDE</B></I></FONT></FONT><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">
		en el momento de hacer la solicitud de la revisión del examen. (Para
		solicitar esta revisión es imprescindible haber solicitado primero
		la revisión de la suma de los puntos). Una vez que el candidato
		reciba el resultado de la primera revisión podrá solicitar la
		segunda.</FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Los
		candidatos no podrán revisar sus exámenes físicamente ya que éstos
		permanecen bajo propiedad intelectual de la Universidad de Cambridge<I>.
		Cambridge ESOL Examinations </I>&nbsp;<B>NO</B> facilita ningún
		informe detallado de cada una de las partes en las que consiste el
		examen y nunca dará más información en la competencia de un
		candidato de la que aparece en el “Statement of Results”.</FONT></FONT></P>
		<P ALIGN=JUSTIFY>&nbsp;</P>
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>5.
		LOS CERTIFICADOS</B></FONT></FONT></P>
		<P><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Los
		certificados podrán retirarse de la Secretaría de EIDE
		aproximadamente 2 meses después de la fecha del examen.</FONT></FONT></P>
		<P ALIGN=JUSTIFY>&nbsp;</P>
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>6.
		PROTECCIÓN DE DATOS</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">En
		cumplimiento con los establecido en la Ley Orgánica 15/99 de
		Protección de Datos de Carácter Personal, los datos de carácter
		personal que nos facilite serán utilizados en la forma y con las
		limitaciones y derechos que recoge la Ley y pasarán a formar parte
		de un fichero propiedad de <I><B>EIDE</B></I>. Estos datos son
		necesarios para la gestión de los exámenes de inglés por parte de
		University <I>of Cambridge ESOL Examinations</I> y son transferidos a
		la Universidad de Cambridge con el único fin de la prestación de
		dicho servicio. Al facilitarnos sus datos personales consiente el
		tratamiento informatizado o no de los mismos por <I><B>EIDE</B></I>
		para los fines anteriormente citados. </FONT></FONT>
		</P>
		<P ALIGN=JUSTIFY>&nbsp;</P>
		<P ALIGN=CENTER STYLE="background: #c0c0c0"><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 11pt"><B>7.
		AUTORIZACIÓN FOTO</B></FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Todos
		aquellos candidatos matriculados en los exámenes PET, FCE, CAE y CPE
		serán fotografiados el día del examen oral o del examen escrito,
		para aumentar la seguridad del examen y permitir a instituciones como
		universidades, organizaciones profesionales y autoridades de
		inmigración confirmar los resultados de los candidatos de forma
		fácil y segura. Ninguna persona u organización podrá acceder a la
		fotografía de ningún candidato sin su autorización.</FONT></FONT></P>
		<P ALIGN=JUSTIFY><FONT FACE="Arial, sans-serif"><FONT SIZE=2 STYLE="font-size: 9pt">Junto
		con la matrícula del examen, los candidatos deberán firmar una
		autorización, indicando su nombre y fecha. Si el candidato es menor
		de edad, la autorización deberá ser firmada por su madre, padre o
		tutor.</FONT></FONT></P>
		<P><FONT COLOR="#1f497d">&nbsp;</FONT></P>
		<P STYLE="margin-bottom: 0cm"><BR>
		</P>
		</body></html>
		"""%(self.exam,self.exam.exam_date)
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
		return "%s"%(self.exam)
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
		super(Registration, self).save(*args, **kwargs)
		
	
	
	def generate_payment_url(self):
		return '/pagos/cambridge/%s/'%(self.id)
