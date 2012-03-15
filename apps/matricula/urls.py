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


urlpatterns = patterns('matricula/',

    url(r'detalle/(?P<pk>\d+)$',
        login_required(UpdateView.as_view(
            model=Registration,
            template_name='matricula/matricula_edit.html')), name="matricula_detalle"),

    url(r'imprimir/(?P<pk>\d+)$', imprimir_matricula, name="matricula_imprimir"),
    url(r'nueva$',
        CreateView.as_view(
            model=Registration,
            template_name='matricula/matricula_form.html'), name="matricula_nueva"),
	url(r'nueva/cb/$',
        CreateView.as_view(
            model=ComputerBasedRegistration,
            template_name='matricula/matricula_form_computer.html'), name="matricula_nueva_computer"),

    url(r'lista$',login_required(ListView.as_view(model=Registration,template_name='matricula/lista.html')), name="matricula_lista"),
    url(r'gracias$', direct_to_template, {'template': 'matricula/gracias.html' },name="matricula_gracias"),
    url(r'/?$', direct_to_template, {'template': 'matricula/index.html' },name="matricula"),
)
