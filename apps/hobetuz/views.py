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
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View
from django.views.generic.edit import ModelFormMixin

import StringIO
import ho.pisa as pisa
from excel_response import ExcelResponse

from django_xhtml2pdf.utils import render_to_pdf_response
#from utils import  render_to_pdf_response

from models import *
from forms import *


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

#~ 
#~ def ver(request, pk):
	#~ registration = get_object_or_404(Registration, id=pk)
	#~ payload = {'registration': registration}
	#~ file_data = render_to_string('hobetuz/imprimir.html', payload, RequestContext(request))
	#~ myfile = StringIO.StringIO()
	#~ return HttpResponse( file_data )
#~ 
#~ 
#~ 
#~ def imprimir(registration,request):
	#~ payload = {'registration': registration}
	#~ response_pdf = render_to_pdf_response('hobetuz/matricula_imprimir.html', 
		#~ payload, pdfname='hobetuz-%s.pdf'%registration.id)
	#~ response_html = render_to_response('hobetuz/matricula_imprimir.html', 
		#~ payload)
#~ 
	#~ return response_pdf
#~ 
#~ @login_required
#~ def imprimir_hobetuz(request, pk):
	#~ logger.debug("Vamos a imprimir una matricula normal")
	#~ registration = Registration.objects.get(id=pk)
	#~ return imprimir(registration,request)
#~ 

class RegistrationList(ListView):
	model=Registration
	template_name='hobetuz/lista.html'

#~ class RegistrationPayment(DetailView):
	#~ model=Registration
	#~ template_name='hobetuz/payment.html'
#~ 
class RegistrationUpdateView(UpdateView):
	model=Registration
	success_url = '/hobetuz/list'
	form_class = RegistrationForm
	template_name='hobetuz/registration_edit.html'
	
class RegistrationCreateView(CreateView):
	model = Registration
	form_class = RegistrationForm
	template_name='hobetuz/registration_form.html'
	def get_success_url(self):
		## FIXME usar un reverse o lazy_reverse
		return '/hobetuz/thanks/'
#~ 
#~ @login_required	
#~ def RegistrationExcelView(request):
    #~ objs = Registration.objects.filter(paid=True)
    #~ return ExcelResponse(objs)
#~ 
#~ class RegistrationListView(ListView):
	#~ #model=ComputerBasedRegistration
	#~ template_name='hobetuz/lista.html'
	#~ #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
	#~ queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),paid=True)

class CursoList(ListView):
    queryset=Curso.objects.all()
    template_name='hobetuz/curso_list.html'

class HobetuzPortada(ListView):
    queryset=Curso.objects.filter(matricula_abierta=True)
    template_name='hobetuz/portada.html'

