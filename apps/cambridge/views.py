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

    #return response_html
    return response_pdf

@login_required
def imprimir_cambridge(request, pk):
    logger.debug("Vamos a imprimir una matricula normal")
    registration = Registration.objects.get(id=pk)
    return imprimir(registration,request)

class RegistrationPayment(DetailView):
    model=Registration
    template_name='cambridge/payment.html'

    

class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name='cambridge/registration_form.html'
    def get_success_url(self):
        return '/cambridge/pay/%d'%self.object.id
#       #Comprobamos si el pago es por txartela:
#       if True:
#           return self.object.generate_payment_url()
#       else:
#           ## FIXME usar un reverse o lazy_reverse
#           return '/cambridge/thanks/'


class SchoolRegistrationCreateView(RegistrationCreateView):
    form_class = SchoolRegistrationForm
    template_name='cambridge/registration_form.html'
    
    def get_form_kwargs(self):
        kwargs = super(SchoolRegistrationCreateView, self).get_form_kwargs()
        #recogemos  y añadimos kwargs a la form
        print self.kwargs
        kwargs['school_name'] = self.kwargs['school_name']
        return kwargs
    
@login_required 
def RegistrationExcelView(request):
    objs = Registration.objects.filter(paid=True)
    return ExcelResponse(objs)

class RegistrationListView(ListView):
    #model=ComputerBasedRegistration
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),paid=True)

class ExamList(ListView):
    queryset=Exam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/exam_list.html'

class SchoolExamList(ListView):
    queryset=SchoolExam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/school_exam_list.html'

class SchoolExamCreate(CreateView):
    model = SchoolExam
    success_url="/cambridge/schools/exam/list/"
    form_class = SchoolExamForm

class IndexExamList(ListView):
    model=Exam
    template_name='cambridge/index.html'
    def get_context_data(self, **kwargs):
		context = super(IndexExamList, self).get_context_data(**kwargs)
		context.update({
		'examenes_pb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=1),
		'examenes_cb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=2),
		'examenes_fs_pb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=3),
		'examenes_fs_cb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=4)
		})
		return context
             
        #return render_to_response('cambridge/index.html',{'examenes_pb': examenes_pb, 'examenes_cb': examenes_cb,'examenes_fs': examenes_fs})
	
