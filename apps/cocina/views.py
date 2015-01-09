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
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View, TemplateView
from django.views.generic.edit import ModelFormMixin

import StringIO
import ho.pisa as pisa
from excel_response import ExcelResponse

from django_xhtml2pdf.utils import render_to_pdf_response, generate_pdf
#from utils import  render_to_pdf_response

from models import *
from forms import *


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def ver(request, pk):
	registration = get_object_or_404(Registration, id=pk)
	payload = {'registration': registration, 'request': request}
	file_data = render_to_string('cocina/detalle.html', payload, RequestContext(request))
	myfile = StringIO.StringIO()
	return HttpResponse( file_data )

def imprimir(registration,request):
	payload = {'registration': registration}
	#response_pdf = render_to_pdf_response('cocina/matricula_imprimir.html',payload, pdfname='cocina-%s.pdf'%registration.id)
	#response_pdf = render_to_pdf_response('cocina/detalle.html',payload, pdfname='cocina-%s.pdf'%registration.id)
	response_html = render_to_response('cocina/detalle.html',payload, RequestContext(request))
	#return response_pdf
	return response_html

@login_required
def imprimir_cocina(request, pk):
	registration = Registration.objects.get(id=pk)
	return imprimir(registration,request)


class RegistrationList(ListView):
	model=Registration
	template_name='cocina/lista.html'

#~ class RegistrationPayment(DetailView):
	#~ model=Registration
	#~ template_name='cocina/payment.html'
#~ 
class RegistrationUpdateView(UpdateView):
	model=Registration
	success_url = '/cocina/list'
	form_class = RegistrationForm
	template_name='cocina/registration_edit.html'
	
class RegistrationCreateView(CreateView):
	model = Registration
	form_class = RegistrationForm
	template_name='cocina/registration_form.html'
	def get_success_url(self):
		## FIXME usar un reverse o lazy_reverse
		return '/cocina/thanks/'

@login_required	
def RegistrationExcelView(request):
    objs = Registration.objects.all()
    return ExcelResponse(objs)
#~ 
#~ class RegistrationListView(ListView):
	#~ #model=ComputerBasedRegistration
	#~ template_name='cocina/lista.html'
	#~ #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
	#~ queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),paid=True)

class CocinaPortada(TemplateView):
    
    template_name='cocina/portada.html'

