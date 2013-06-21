from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, permission_required
from views import *

urlpatterns = patterns("",
    #url(r"^confirmar/(?P<reference>[-\.\w]+)/$", confirm_payment, name="pago_confirmar"),
    url(r"^lista$", login_required(pagos_lista.as_view()), name="pago_lista"),
    url(r"^nuevo/$", login_required(crear_pago_manual.as_view()), name="pago_manual_crear"),
    url(r"^pago/(?P<pago_id>\d+)/$", pagar_manual, name="pago_manual_pagar"),
    url(r"^(?P<reference>\w+)/(?P<order_id>\d+)/$", make_payment , name="pago"),
    url(r"^confirmar/$", confirm_payment, name="pago_confirmar"),
    url(r"^ok/$", direct_to_template, {"template": "pago_ok.html"}, name="pago_ok"),
    url(r"^ko/$", direct_to_template, {"template": "pago_ko.html"}, name="pago_ko"),
)
