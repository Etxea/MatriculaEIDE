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
import hashlib
#from django.utils.text import slugify
from django.template.defaultfilters import slugify
from cambridge.models import Registration
# Create your models here.
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

