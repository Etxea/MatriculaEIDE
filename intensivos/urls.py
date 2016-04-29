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
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, RedirectView

from views import *
from forms import *
from models import *


urlpatterns = patterns('intensivos/',
    url(r'^course/list/$',IntensivoListView.as_view(), name="intesivos_course_list"),
    url(r'^course/new/$',IntensivoCreateView.as_view(), name="intensivos_course_new"),
    url(r'^course/edit/(?P<pk>\d+)/$',IntensivoUpdateView.as_view(), name="intensivos_course_edit"),
    url(r'^course/delete/(?P<pk>\d+)/$',IntensivoDeleteView.as_view(), name="intensivos_course_delete"),
    
    url(r'^list/$',login_required(RegistrationListView.as_view()), name="intesivos_list"),
    url(r'^new/$',RegistrationCreateView.as_view(), name="intensivos_nueva"),
    #~ url(r'^excel/$',RegistrationExcelView, name="intensivos_excel"),
    url(r'^edit/(?P<pk>\d+)/$',login_required(RegistrationUpdateView.as_view()), name="intensivos_edit"),
    url(r'^delete/(?P<pk>\d+)/$', login_required(RegistrationDeleteView.as_view()), name="intensivos_delete"),
    url(r'^view/(?P<pk>\d+)/$', login_required(RegistrationDetailView.as_view()), name="intensivos_detalle"),
    url(r'thanks/$', direct_to_template, {'template': 'intensivos/gracias.html' },name="intensivos_gracias"),
    #url(r'^/?$', direct_to_template,{'template': 'portada.html' },name="intensivos"),
    url(r'^/?$', RedirectView.as_view(url='/intensivos/new/'),name="intensivos"),
)
