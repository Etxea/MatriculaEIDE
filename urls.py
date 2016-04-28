from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^41F198A7ACB0BA4FDACC67D322E2BBB7.txt",direct_to_template, {
        "template": "41F198A7ACB0BA4FDACC67D322E2BBB7.txt",
    }, name="validate"),
    url(r"^index$", direct_to_template, {
        "template": "homepage.html",
    }, name="index"),
    url(r"^cookies$", direct_to_template, {
        "template": "cookielaw/politica_cookies.html",
    }, name="cookies"),
    url(r"^$", redirect_to, {
        "url": "/index",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^cambridge/", include("cambridge.urls")),
    url(r"^hobetuz/", include("hobetuz.urls")),
    url(r"^pagos/", include("pagosonline.urls")),
    url(r"^pasarela/", include("pasarelapago.urls")),
    url(r"^espanol/", include("cursosespanol.urls")),
    url(r"^cocina/", include("cocina.urls")),
    url(r"^intensivos/", include("intensivos.urls")),
    url(r"^inscripciones/", include("inscripciones.urls")),
    #~ url(r'^sermepa/', include('sermepa.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
