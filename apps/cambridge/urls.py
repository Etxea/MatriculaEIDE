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
	url(r'^cb/list/$',login_required(
		ListView.as_view(model=ComputerBasedRegistration,template_name='cambridge/lista.html')), 
		name="cambridge_cb_list"),
	url(r'^cb/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=ComputerBasedRegistration,
            success_url = '/cambridge/list',
            template_name='cambridge/cambridge_cb_edit.html')), 
            name="cambridge_cb_edit"),
	url(r'^cb/print/(?P<pk>\d+)/$', imprimir_cambridge_cb, name="cambridge_imprimir_cb"),
	url(r'^cb/view/(?P<pk>\d+)/$', ver, name="cambridge_cb_view"),
	url(r'^cb/new/$',
        CreateView.as_view(
            model=ComputerBasedRegistration,
            success_url = '/cambridge/thanks',
            form_class = ComputerBasedRegistrationForm,
            template_name='cambridge/registration_form_computer.html'), name="cambridge_nueva_computer"),

	
    url(r'^list/$',login_required(
		ListView.as_view(model=Registration,template_name='cambridge/lista.html')
		), name="cambridge_list"),
    url(r'^edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Registration,
            success_url = '/cambridge/list',
            template_name='cambridge/cambridge_edit.html')), name="cambridge_edit"),
	url(r'^view/(?P<pk>\d+)/$', ver, name="cambridge_view"),
    url(r'^print/(?P<pk>\d+)/$', imprimir_cambridge, name="cambridge_imprimir"),
    
    url(r'^new/$',
        CreateView.as_view(
            model=Registration,
            form_class = RegistrationForm,
            success_url = '/cambridge/thanks',
            template_name='cambridge/registration_form.html'), name="cambridge_nueva"),
            

    
    url(r'thanks/$', direct_to_template, {'template': 'cambridge/gracias.html' },name="cambridge_gracias"),
    ##For the exams
    url(r'^exam/list/$',login_required(
		ListView.as_view(model=Exam,template_name='cambridge/exam_list.html')
		), name="cambridge_exam_list"),
    url(r'^exam/new/$', login_required(
        CreateView.as_view(
            model=Exam,
            success_url = '/cambridge/exam/list',
            template_name='cambridge/exam_form.html')), name="cambridge_exam_new"),
	url(r'^exam/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Exam,
            success_url = '/cambridge/exam/list',
            template_name='cambridge/exam_edit.html')), name="cambridge_exam_edit"),
        
    url(r'^cb/exam/list/$',login_required(
		ListView.as_view(model=ComputerBasedExam,template_name='cambridge/cb_exam_list.html')
		), name="cambridge_cb_exam_list"),
    url(r'^cb/exam/new/$',
        CreateView.as_view(
            model=ComputerBasedExam,
            success_url = '/cambridge/cb/exam/list',
            template_name='cambridge/cb_exam_form.html'), name="cambridge_cb_exam_new"),        
	url(r'^cb/exam/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=ComputerBasedExam,
            success_url = '/cambridge/cb/exam/list',
            template_name='cambridge/cb_exam_edit.html')), name="cambridge_cb_exam_edit"),
    
    url(r'^/?$', direct_to_template, {'template': 'cambridge/index.html' },name="cambridge"),
)
