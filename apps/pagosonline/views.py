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
from django.contrib.csrf.middleware import csrf_exempt
from models import *
from cambridge.models import Registration

import logging
log = logging.getLogger("MatriculaEIDE")


def make_payment(request, reference, order_id):
    """ Recibimos un texto de referencia, el ID de la orden y una cantidad en euros (sin decimales)"""
    return direct_to_template(request,
        template= "pago.html",
        extra_context={"payament_info": payament_info(reference, order_id)})

@csrf_exempt
def confirm_payment(request):
    ## FIXME habría que poner algun filtro a la confirmación del pago.
    log.debug("Recibimos una confirmación de pago")
    log.debug(request.POST)
    try:
        #Leemos el bumero de operación donde tenemo s la referencia a la matricula
        log.debug("Vamos a leer el Num_operacion para ver que vamos a confirmar")
        reference = request.POST["Num_operacion"]
        log.debug("tenemos la referencia: %s"%reference)
        registration_type = reference.split('-')[0]
        registration_id = reference.split('-')[1]
        log.debug( "tenemos una matricula de %s con el id %s"%(registration_type, registration_id))
        r = None
        log.debug("Vamos a buscarla")
        #Buscamos la matricula 
        if registration_type=="cambridge":
            log.debug("Es cambridge")
            r = Registration.objects.get(id=registration_id)
        else:
            log.debug( "No sabemos que tipo de matricula es!" )
        #Comprobamos si tenemos una matricula
        if r:
            log.debug( "Tenemos la matricula")
            log.debug(r)
            r.set_as_paid()
            return direct_to_template(request,template="pago_confirmar.html")
        else:
            return direct_to_template(request,template="pago_noconfirmar.html")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.debug("No hemos sido capaces de validar el pago de la matricula")
        log.debug(exc_type)
        log.debug(exc_value)
        log.debug(exc_traceback)
        return direct_to_template(request,template="pago_noconfirmar.html")
    
