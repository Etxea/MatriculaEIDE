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
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from views import *
from forms import *
from models import Registration


urlpatterns = patterns('cambridge/',
	url(r'^cb/list/$',login_required(ListView.as_view(model=ComputerBasedRegistration,template_name='cambridge/lista.html')), name="cambridge_lista"),
    url(r'^list/$',login_required(ListView.as_view(model=Registration,template_name='cambridge/lista.html')), name="cambridge_lista"),
    url(r'^edit/(?P<pk>\d+)$',
        login_required(UpdateView.as_view(
            model=Registration,
            template_name='cambridge/registration_edit.html')), name="cambridge_edit"),

    url(r'^print/(?P<pk>\d+)$', imprimir_cambridge, name="cambridge_imprimir"),
    url(r'^cb/print/(?P<pk>\d+)$', imprimir_cambridge_cb, name="cambridge_imprimir_cb"),
    url(r'^new$',
        CreateView.as_view(
            model=Registration,
            template_name='cambridge/registration_form.html'), name="cambridge_nueva"),
	url(r'^cb/new$',
        CreateView.as_view(
            model=ComputerBasedRegistration,
            template_name='cambridge/registration_form_computer.html'), name="cambridge_nueva_computer"),

    
    url(r'gracias$', direct_to_template, {'template': 'cambridge/gracias.html' },name="cambridge_gracias"),
    url(r'^/?$', direct_to_template, {'template': 'cambridge/index.html' },name="cambridge"),
)
