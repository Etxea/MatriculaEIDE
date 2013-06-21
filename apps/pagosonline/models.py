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
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import hashlib
import datetime
#from django.utils.text import slugify
from django.template.defaultfilters import slugify
from cambridge.models import Registration



class Pago(models.Model):
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.CharField(_('Descripción de quien es el pago.'),max_length=250,blank=True)
    fecha_creacion = models.DateField(default=datetime.date.today, auto_now_add=True)
    fecha_pago = models.DateField(null=True,blank=True)
    def get_absolute_url(self):
        return "/pagos/pago/%i/" % self.id
    def set_as_paid(self):
        self.fecha_pago = datetime.date.today
        self.send_paiment_confirmation_email()
    def send_paiment_confirmation_email(self):
		subject = "Se ha confirmado su pago  ONLINE en EIDE"
		html_content=u"""<html><body>
		<h2>CONFIRMACIÓN DE PAGO ONLINE</h2>
<p>Se ha confirmado su pago de <b> %s </b> € con la descripcion %s creado en la fecha <b> %s </b> y confirmado en la fecha <b> %s </b> .</p>
		"""%(self.importe,self.descripcion,self.fecha_creacion,self.fecha_pago)
		message_body = html_content
		##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
		msg.attach_alternative(html_content, "text/html")
		##msg.content_subtype = "html"
		msg.send()
		
		subject = "[PAgosONline] Se ha confirmado un pago manual"
		message_body = u"""Se acaba de confirmarun pago por %s. \n 
"""%(self.importe)
		mail_admins(subject, message_body)


class payament_info:
    """El objecto donde guardamos la infor para pasarla a la vista"""
    #Estas variables las leemos de la conf
    action_url=""
    MerchantID = ""
    AcquirerBIN = ""
    TerminalID = ""
    url_ok = ""
    url_nok = ""    
    clave = ""
    #Estas no cambian entre instalaciones
    cifrado="SHA1"
    tipo_moneda="978"
    exponente="2"
    pago_soportado="SSL"
    #Estas las generamos
    amount = ""
    order_id = ""
    firma = ""
    
    def __init__(self, reference, order_id):
        if reference=="cambridge":
            r = Registration.objects.get(id=order_id)
            #La cantidad la multiplicamos por 100 para tener los 2 decimales en un numero entero
            self.amount = int(float(r.exam.level.price)*100)
            self.amount_text = "%s"%(float(r.exam.level.price))
            #generamos el order_i con la referencia, subreferencia y el ID del la matricula para luego saber cual es
            self.order_id = "%s-%s-%s"%(reference,order_id,slugify(r.registration_name()))
        elif reference == "manual":
            p = Pago.objects.get(id=order_id)
            self.amount = int(float(p.importe)*100)
            self.amount_text = "%s €"%p.importe
            self.order_id = "manual-%s"%order_id
        #Leemos de los settings
        self.MerchantID = settings.PAYMENT_INFO["MerchantID"]
        self.AcquirerBIN=settings.PAYMENT_INFO["AcquirerBIN"]
        self.TerminalID=settings.PAYMENT_INFO["TerminalID"]
        self.clave=settings.PAYMENT_INFO["clave"]
        self.action_url=settings.PAYMENT_INFO["action_url"]
        self.url_ok=settings.PAYMENT_INFO["url_ok"]
        self.url_nok=settings.PAYMENT_INFO["url_nok"]
        #calculamos el SHA1 de la operación
        texto = self.clave + self.MerchantID + self.AcquirerBIN + self.TerminalID + \
            self.order_id + str(self.amount) + self.tipo_moneda + self.exponente + \
            self.cifrado + self.url_ok + self.url_nok;        
        clave_sha1 = hashlib.sha1()
        clave_sha1.update(str(texto))
        self.firma = clave_sha1.hexdigest()

