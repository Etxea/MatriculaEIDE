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
from django.views.generic.simple import direct_to_template
from models import *
from cambridge.models import ComputerBasedRegistration,Registration

import logging
log = logging.getLogger("MatriculaEIDE")


def make_payment(request, reference,sub_reference, order_id,amount):
    """ Recibimos un texto de referencia, el ID de la orden y una cantidad en euros (sin decimales)"""
    return direct_to_template(request,
        template= "pago.html",
        extra_context={"payament_info": payament_info(amount, reference, sub_reference, order_id),
            ##El precio hay que multiplicarlo por 100 para cuadrar los 2 decimales que nos exige la pasarela
            "amount": amount})

#def confirm_payment(request, reference):
def confirm_payment(request):
    ## FIXME habría que poner algun filtro a la confirmación del pago.
    log.debug("Recivimos una confirmación de pago")
    log.debug(request.POST)
    try:
        reference = request.POST["Referencia"]
        #log.debug( reference)
        registration, registration_id = reference.split('-')
        registration_type, registration_subtype = registration.split('.')
        log.debug( "tenemos una matricula de %s del tipo %s con el id %s"%(registration_type, registration_subtype, registration_id))
        r = None
        #Buscamos la matricula 
        if registration_type=="cambridge":
            if registration_subtype=="pb":
                print "Hola"
                r = Registration.objects.get(id=registration_id)
            elif registration_subtype=="cb":
                r = ComputerBasedRegistration.objects.get(id=registration_id)
            else:
                log.debug( "No sabemos que matricula de cambridge!" )
        #Comprobamos si tenemos una matricula
        if r:
            log.debug( "Tenemos la matricula")
            log.debug(r)
            r.set_as_paid()
            return direct_to_template(request,template="pago_confirmar.html")
        else:
            return direct_to_template(request,template="pago_noconfirmar.html")
    except:
        return direct_to_template(request,template="pago_noconfirmar.html")
    
