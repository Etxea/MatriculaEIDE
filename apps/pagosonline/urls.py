from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "pago.html"}, name="pago"),
    url(r"^ok/$", direct_to_template, {"template": "pago_ok.html"}, name="pago_ok"),
    url(r"^ko/$", direct_to_template, {"template": "pago_ko.html"}, name="pago_ko"),
    url(r"^confirmar/$", direct_to_template, {"template": "pago_confirmar.html"}, name="pago_confirmar"),
)
