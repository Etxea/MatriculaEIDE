# Create your views here.
from django.views.generic.simple import direct_to_template

def make_payment(request, reference, order_id,amount):
    """ Recivimos un texto de referencia, el ID de la orden y una cantidad en euros (sin decimales)"""
    return direct_to_template(request,
        template= "pago.html",
        extra_context={"reference":reference, 
            "order_id": order_id,
            ##El precio hay que multiplicarlo por 100 para cuadrar los 2 decimales que nos exige la pasarela
            "amount": amount})
