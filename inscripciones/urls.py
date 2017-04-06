# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.simple import direct_to_template

from views import *

urlpatterns = patterns('inscripciones/',
    url(r'^list/$',login_required(RegistrationListView.as_view()), name="inscripciones_list"),
    url(r'^new/$',RegistrationCreateView.as_view(), name="inscripciones_nueva"),
    url(r'^edit/(?P<pk>\d+)/$',login_required(RegistrationUpdateView.as_view()), name="inscripciones_edit"),
    url(r'^delete/(?P<pk>\d+)/$', login_required(RegistrationDeleteView.as_view()), name="inscripciones_delete"),
    url(r'^view/(?P<pk>\d+)/$', login_required(RegistrationDetailView.as_view()), name="inscripciones_detalle"),
    url(r'thanks/$', direct_to_template, {'template': 'inscripciones/gracias.html' },name="inscripciones_gracias"),
    url(r'^/?$', direct_to_template,{'template': 'portada.html' },name="inscripciones"),
)
