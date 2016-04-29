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
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View
from django.views.generic.edit import ModelFormMixin


import StringIO
import ho.pisa as pisa
from excel_response3 import ExcelResponse
from django_xhtml2pdf.utils import render_to_pdf_response
from models import *
from forms import *
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
    
@login_required 
def RegistrationExcelView(request):
    objs = Registration.objects.filter(paid=True)
    return ExcelResponse(objs)

class RegistrationListView(ListView):
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),paid=True)

class ExamList(ListView):
    queryset=Exam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/exam_list.html'

class SchoolExamList(ListView):
    queryset=SchoolExam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/school_exam_list.html'

class SchoolListView(ListView):
	model = School

class SchoolExamCreate(CreateView):
    model = SchoolExam
    success_url="/cambridge/schools/exam/list/"
    template_name = "cambridge/school_exam_form.html"
    form_class = SchoolExamForm
    #Limitamos los niveles a los que tiene el colegio
    def get_form_kwargs(self):
        kwargs = super(SchoolExamCreate, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['school_name'] = self.kwargs['school_name']
        return kwargs
    #Añadimos el school_name al contexto
    def get_context_data(self, **kwargs):
        context = super(SchoolExamCreate, self).get_context_data(**kwargs)
        context['school_name'] = self.kwargs['school_name']
        
        return context

class SchoolRegistrationListView(ListView):
    template_name='cambridge/school_registration_list.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas y sean de la escuela
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),exam__in=SchoolExam.objects.all())

class SchoolRegistrationCreateView(RegistrationCreateView):
    form_class = SchoolRegistrationForm
    template_name='cambridge/school_registration_form.html'
    def get(self, request, *args, **kwargs):
        #Comprobamos el password
        if 'school_password' in kwargs:
            school = School.objects.get(name=kwargs['school_name'])
            print "Comprobamos el password",school.password,kwargs['school_password']
            if school.password == kwargs['school_password']:
                return super(SchoolRegistrationCreateView, self).get(request, *args, **kwargs)
            else:
                return redirect('/cambridge/')
        else:
            return redirect('/cambridge/')
    def get_form_kwargs(self):
        kwargs = super(SchoolRegistrationCreateView, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['school_name'] = self.kwargs['school_name']
        return kwargs
    #Añadimos el school_name al contexto
    def get_context_data(self, **kwargs):
        context = super(SchoolRegistrationCreateView, self).get_context_data(**kwargs)
        context['school_name'] = self.kwargs['school_name']
        context['school'] = School.objects.get(name=self.kwargs['school_name'])
        print "tenemos la school",context['school']
        return context


class IndexExamList(ListView):
    model=Exam
    template_name='cambridge/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexExamList, self).get_context_data(**kwargs)
        context.update({
        'examenes_pb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=1).filter(schoolexam__isnull=True),
        'examenes_cb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=2).filter(schoolexam__isnull=True),
        'examenes_fs_pb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=3).filter(schoolexam__isnull=True),
        'examenes_fs_cb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=4).filter(schoolexam__isnull=True)
        })
        return context
             
        #return render_to_response('cambridge/index.html',{'examenes_pb': examenes_pb, 'examenes_cb': examenes_cb,'examenes_fs': examenes_fs})
    
##Venues
class VenueExamList(ListView):
    queryset=VenueExam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/venue_exam_list.html'

class VenueExamCreate(CreateView):
    model = VenueExam
    success_url="/cambridge/venue/exam/list/"
    template_name = "cambridge/venue_exam_form.html"
    form_class = VenueExamForm

class VenueListView(ListView):
	model = Venue

class VenueRegistrationListView(ListView):
    template_name='cambridge/venue_registration_list.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas y sean de la escuela
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),exam__in=VenueExam.objects.all())

class VenueRegistrationCreateView(RegistrationCreateView):
    form_class = VenueRegistrationForm
    template_name='cambridge/venue_registration_form.html'
    #~ def get(self, request, *args, **kwargs):
        #~ #Comprobamos el password
        #~ if 'school_password' in kwargs:
            #~ school = School.objects.get(name=kwargs['school_name'])
            #~ print "Comprobamos el password",school.password,kwargs['school_password']
            #~ if school.password == kwargs['school_password']:
                #~ return super(SchoolRegistrationCreateView, self).get(request, *args, **kwargs)
            #~ else:
                #~ return redirect('/cambridge/')
        #~ else:
            #~ return redirect('/cambridge/')
    def get_form_kwargs(self):
        kwargs = super(VenueRegistrationCreateView, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['venue_name'] = self.kwargs['venue_name']
        return kwargs
    #Añadimos el school_name al contexto
    def get_context_data(self, **kwargs):
        context = super(VenueRegistrationCreateView, self).get_context_data(**kwargs)
        context['venue_name'] = self.kwargs['venue_name']
        context['venue'] = Venue.objects.get(name=self.kwargs['venue_name'])
        return context
