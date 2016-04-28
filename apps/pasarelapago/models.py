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
from django.template.defaultfilters import slugify
from django.core.mail import send_mail, mail_admins

from cambridge.models import Registration
import datetime
import hashlib, json, base64, hmac
from Crypto.Cipher import DES3


import logging
log = logging.getLogger("MatriculaEIDE")



class Pago(models.Model):
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.CharField(_('Concepto'),max_length=250,blank=True)
    fecha_creacion = models.DateField(default=datetime.date.today, auto_now_add=True)
    fecha_pago = models.DateField(null=True,blank=True)
    def get_absolute_url(self):
        return "/pasarela/pago/%i/" % self.id
    def set_as_paid(self):
        log.debug("Vamos a marcar como pagado el pago: %s con la descripcion %s"%(self.id,self.descripcion))
        self.fecha_pago = datetime.date.today()
        log.debug("Mandamos un mail de confirmacion")
        self.send_paiment_confirmation_email()
        log.debug("Guardamos...")
        self.save()
        return True
    def send_paiment_confirmation_email(self):
		subject = "[PagosOnline] Se ha confirmado un pago manual online"
		message_body = u"""Se acaba de confirmar un pago online creado manualmente. Los datos son: \n
        \tid: %s. \n 
        \tfecha creacion: %s. \n 
        \tdescripcion: %s. \n 
        \timporte: %s. \n 
"""%(self.id,self.fecha_creacion,self.descripcion,self.importe)
		mail_admins(subject, message_body)


class payament_info:
    """El objecto donde guardamos la infor para pasarla a la vista"""
    #Estas variables las leemos de la conf
    action_url=""
    Ds_Merchant_MerchantCode = ""
    Ds_Merchant_Terminal = ""
    Ds_Merchant_MerchantName= "EIDE"
    Ds_Merchant_ProductDescription="Pago a EIDE"
    Ds_Merchant_TransactionType="0"
    url_ok = ""
    url_nok = ""    
    clave = ""
    #Estas no cambian entre instalaciones
    cifrado="SHA1"
    Ds_Merchant_Currency="978"
    exponente="2"
    pago_soportado="SSL"
    #Estas las generamos
    Ds_Merchant_Amount = ""
    Ds_Merchant_SumTotal = 0
    order_id = ""
    Ds_Merchant_MerchantSignature = ""
    
    
    def __init__(self, reference, order_id, url_confirmar):
        if reference=="cambridge":
            r = Registration.objects.get(id=order_id)
            #La cantidad la multiplicamos por 100 para tener los 2 decimales en un numero entero
            self.Ds_Merchant_Amount = "%012d" % int(float(r.exam.level.price)*100)
            self.Ds_Merchant_SumTotal = self.Ds_Merchant_Amount
            self.amount_text = "%"%(float(r.exam.level.price))
            #~ self.Ds_Merchant_ProductDescription = ""
            #generamos el order_i con la referencia, subreferencia y el ID del la matricula para luego saber cual es
            self.Ds_Merchant_Order = "%04dCAMB%04d"%(order_id,r.id)
        elif reference == "manual":
            p = Pago.objects.get(id=order_id)
            self.Ds_Merchant_Amount = "%012d" % int(float(p.importe)*100)
            self.Ds_Merchant_SumTotal = self.Ds_Merchant_Amount
            #~ self.Ds_Merchant_ProductDescription = ""
            self.amount_text = "%s €"%p.importe
            self.Ds_Merchant_Order = "%04dMANU%04d"%(int(order_id),p.id)
        #Leemos de los settings
        self.Ds_Merchant_MerchantCode = settings.PAYMENT_INFO2["Ds_Merchant_MerchantCode"]
        self.DS_Merchant_Currency = settings.PAYMENT_INFO2["DS_Merchant_Currency"]
        #~ self.AcquirerBIN=settings.PAYMENT_INFO2["AcquirerBIN"]
        self.Ds_Merchant_Terminal=settings.PAYMENT_INFO2["Ds_Merchant_Terminal"]
        self.Ds_Merchant_TransactionType=settings.PAYMENT_INFO2["Ds_Merchant_TransactionType"]
        self.clave=settings.PAYMENT_INFO2["clave"]
        self.action_url=settings.PAYMENT_INFO2["action_url"]
        self.Ds_Merchant_UrlOK=settings.PAYMENT_INFO2["Ds_Merchant_UrlOK"]
        self.Ds_Merchant_UrlKO=settings.PAYMENT_INFO2["Ds_Merchant_UrlKO"]
        #calculamos el SHA1 de la operación
        #~ texto = self.clave + self.Ds_Merchant_MerchantCode + self.TerminalID + \
            #~ self.order_id + str(self.amount) + self.tipo_moneda + self.exponente + \
            #~ self.cifrado + self.url_ok + self.url_nok;     
            
        texto = self.Ds_Merchant_Amount + self.Ds_Merchant_Order + self. Ds_Merchant_MerchantCode + self.DS_Merchant_Currency +\
            self.Ds_Merchant_TransactionType + url_confirmar + self.clave
        sermepa_dict = {
            "Ds_Merchant_MerchantData": "lalalala", # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": 'ACME',
            "Ds_Merchant_Amount": self.Ds_Merchant_Amount,
            "Ds_Merchant_Terminal": self.Ds_Merchant_Terminal,
            "Ds_Merchant_MerchantCode": self.Ds_Merchant_MerchantCode,
            "Ds_Merchant_Currency": self.Ds_Merchant_Currency,
            "Ds_Merchant_MerchantURL": url_confirmar,
            "Ds_Merchant_UrlOK": self.Ds_Merchant_UrlOK ,
            "Ds_Merchant_UrlKO": self.Ds_Merchant_UrlKO,
            "Ds_Merchant_Order": self.Ds_Merchant_Order,
            "Ds_Merchant_TransactionType": '0',
        }        
        order_encrypted = encrypt_order_with_3DES(self.clave,self.Ds_Merchant_Order)
        self.Ds_Merchant_MerchantSignature = sign_hmac256(order_encrypted, encode_parameters(sermepa_dict))


"""
    Given a dict; create a json object, codify it in base64 and delete their carrier returns
    @var merchant_parameters: Dict with all merchant parameters
    @return Ds_MerchantParameters: Encoded json structure with all parameters
"""
def encode_parameters(merchant_parameters):
    parameters = (json.dumps(merchant_parameters)).encode()
    return ''.join(unicode(base64.encodestring(parameters), 'utf-8').splitlines())


"""
    This method creates a unique key for every request, 
    based on the Ds_Merchant_Order and in the shared secret (SERMEPA_SECRET_KEY).
    This unique key is Triple DES ciphered.
    @var merchant_parameters: Dict with all merchant parameters
    @return order_encrypted: The encrypted order
"""
def encrypt_order_with_3DES(clave,Ds_Merchant_Order):
    pycrypto = DES3.new(base64.standard_b64decode(clave), DES3.MODE_CBC, IV=b'\0\0\0\0\0\0\0\0')
    order_padded = Ds_Merchant_Order.ljust(16, b'\0')
    return pycrypto.encrypt(order_padded)



"""
    Use the order_encrypted we have to sign the merchant data using a HMAC SHA256 algorithm 
    and encode the result using Base64
    @var order_encrypted: Encrypted Ds_Merchant_Order
    @var Ds_MerchantParameters: Redsys aleready encoded parameters
    @return Ds_Signature: Generated signature encoded in base64
"""
def sign_hmac256(order_encrypted, Ds_MerchantParameters):
    hmac_value = hmac.new(order_encrypted, Ds_MerchantParameters, hashlib.sha256).digest()
    return base64.b64encode(hmac_value)
