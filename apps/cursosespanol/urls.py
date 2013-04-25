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

from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from views import *
from forms import *
from models import *


urlpatterns = patterns('espanol/',
    url(r'^list/$',login_required(RegistrationListView.as_view()), name="espanol_list"),
    url(r'^edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Registration,
            success_url = '/espanol/list',
            form_class = RegistrationEditForm,
            template_name='espanol/edit.html')), name="espanol_edit"),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Registration,
            success_url="/espanol/list/")), name="espanol_delete"),
    url(r'^view/(?P<pk>\d+)/$',login_required(RegistrationView.as_view()), name="espanol_view"),
    url(r'^pay/(?P<pk>\d+)/$',RegistrationPayment.as_view(),name="espanol_pagar"),
    url(r'^new/$',RegistrationCreateView.as_view(), name="espanol_nueva"),
    url(r'thanks/$', direct_to_template, {'template': 'espanol/gracias.html' },name="espanol_gracias"),
    url(r'^/?$', direct_to_template, {"template": "index.html"}, name="espanol_index"),

)
