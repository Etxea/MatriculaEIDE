from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import make_payment,confirm_payment

urlpatterns = patterns("",
    #url(r"^confirmar/(?P<reference>[-\.\w]+)/$", confirm_payment, name="pago_confirmar"),
    url(r"^(?P<reference>\w+)/(?P<order_id>\d+)/$", make_payment , name="pago"),
    url(r"^confirmar/$", confirm_payment, name="pago_confirmar"),
    url(r"^ok/$", direct_to_template, {"template": "pago_ok.html"}, name="pago_ok"),
    url(r"^ko/$", direct_to_template, {"template": "pago_ko.html"}, name="pago_ko"),
)
