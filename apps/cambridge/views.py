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

from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin

import StringIO
import ho.pisa as pisa

from django_xhtml2pdf.utils import render_to_pdf_response
#from utils import  render_to_pdf_response

from models import *
from forms import *


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def ver(request, pk):
	registration = get_object_or_404(Registration, id=pk)
	payload = {'registration': registration}
	file_data = render_to_string('cambridge/imprimir.html', payload, RequestContext(request))
	myfile = StringIO.StringIO()
	return HttpResponse( file_data )



def imprimir(registration,request):
	payload = {'registration': registration}
	response_pdf = render_to_pdf_response('cambridge/matricula_imprimir.html', 
		payload, pdfname='cambridge-%s.pdf'%registration.id)
	response_html = render_to_response('cambridge/matricula_imprimir.html', 
		payload)

	return response_pdf

@login_required
def imprimir_cambridge(request, pk):
	logger.debug("Vamos a imprimir una matricula normal")
	registration = Registration.objects.get(id=pk)
	return imprimir(registration,request)


@login_required
def imprimir_cambridge_cb(request, pk):
	logger.debug("Vamos a imprimir una matricula normal Computer based")
	registration = ComputerBasedRegistration.objects.get(id=pk)
	return imprimir(registration)

class ComputerBasedRegistrationListView(ListView):
	#model=ComputerBasedRegistration
	template_name='cambridge/lista.html'
	#Limitamos a las matrocilas de examenes posteriores al día de hoy
	queryset=ComputerBasedRegistration.objects.filter(exam__exam_date__gt=datetime.date.today())

class ComputerBasedRegistrationCreateView(CreateView, ModelFormMixin):
	model = ComputerBasedRegistration
	form_class = ComputerBasedRegistrationForm
	template_name='cambridge/registration_form_computer.html'
	def get_success_url(self):
		#Comprobamos si el pago es por txartela:
		if True:
			return self.object.generate_payment_url()
		else:
			## FIXME usar un reverse o lazy_reverse
			return '/cambridge/thanks/'

class ComputerBasedRegistrationUpdateView(UpdateView):
	model=ComputerBasedRegistration,
	success_url = '/cambridge/list',
	template_name='cambridge/cambridge_cb_edit.html'
	
class PaperBasedRegistrationCreateView(CreateView):
	model = Registration
	form_class = RegistrationForm
	template_name='cambridge/registration_form.html'
	def get_success_url(self):
		#Comprobamos si el pago es por txartela:
		if True:
			return self.object.generate_payment_url()
		else:
			## FIXME usar un reverse o lazy_reverse
			return '/cambridge/thanks/'
	
class RegistrationListView(ListView):
	#model=ComputerBasedRegistration
	template_name='cambridge/lista.html'
	#Limitamos a las matrocilas de examenes posteriores al día de hoy
	queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today())
