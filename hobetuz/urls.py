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


urlpatterns = patterns('hobetuz/',
    url(r'^list/$',login_required(RegistrationList.as_view()), name="hobetuz_list"),
    url(r'^new/$',RegistrationCreateView.as_view(), name="hobetuz_nueva"),
    url(r'^excel/$',RegistrationExcelView, name="hobetuz_excel"),
    url(r'^edit/(?P<pk>\d+)/$',login_required(RegistrationUpdateView.as_view()), name="hobetuz_edit"),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Registration,
            success_url="/hobetuz/list/")), name="hobetuz_delete"),
    url(r'^view/(?P<pk>\d+)/$', ver, name="hobetuz_view"),
    url(r'^print/(?P<pk>\d+)/$', imprimir_hobetuz, name="hobetuz_imprimir"),
    
    ## Genericas
    url(r'thanks/$', direct_to_template, {'template': 'hobetuz/gracias.html' },name="hobetuz_gracias"),
    #~ ##Para los cursos
    url(r'^curso/list/$',login_required(CursoList.as_view()), name="hobetuz_curso_lista"),
    url(r'^curso/delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Curso,
            success_url="/hobetuz/curso/list/")), name="hobetuz_curso_delete"),
    url(r'^curso/new/$', login_required(
        CreateView.as_view(
            model=Curso,
            form_class = CursoForm,
            success_url = '/hobetuz/curso/list',
            template_name='hobetuz/curso_form.html')), name="hobetuz_curso_nuevo"),
    url(r'^curso/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Curso,
            success_url = '/hobetuz/curso/list',
            template_name='hobetuz/curso_edit.html')), name="hobetuz_curso_edit"),
    url(r'^/?$', HobetuzPortada.as_view(),name="hobetuz"),
)
