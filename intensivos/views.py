from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View, DeleteView
from django.views.generic.edit import ModelFormMixin

from models import *
from forms import *

class RegistrationDetailView(DetailView):
    model=Registration
    template_name='intensivos/detalle.html'

class RegistrationDeleteView(DeleteView):
    model=Registration
    success_url = '/intensivos/list/'

class RegistrationUpdateView(UpdateView):
    model=Registration  
    success_url = '/intensivos/list/'

class RegistrationPayment(DetailView):
    model=Registration
    template_name='intensivos/payment.html'
    
class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name='intensivos/registration_form.html'
    def get_context_data(self, **kwargs):
        context = super(RegistrationCreateView, self).get_context_data(**kwargs)
        context['lista_intensivos'] = Intensivo.objects.all()
        return context
        
    def get_success_url(self):
        return '/intensivos/thanks/'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()    
        self.object.password = ''.join([choice(letters) for i in xrange(6)])
        for intensivo in form.cleaned_data['intensivos']:
            print "Abadimos intensivo",intensivo
            self.object.intensivos.add(intensivo)
        
        self.object.send_confirmation_email()
        return super(ModelFormMixin, self).form_valid(form)

def RegistrationExcelView(request):
    objs = Registration.objects.all()
    return ExcelResponse(objs)

class RegistrationListView(ListView):
    model = Registration
    template_name='intensivos/lista.html'




class IntensivoCreateView(CreateView):
    model = Intensivo
    form_class = IntensivoForm
    template_name='intensivos/course_form.html'
    def get_success_url(self):
        return '/intensivos/course/list/'

class IntensivoListView(ListView):
    model = Intensivo
    template_name='intensivos/course_list.html'


class IntensivoDeleteView(DeleteView):
    model=Intensivo
    template_name='intensivos/course_delete_confirm.html'
    success_url = '/intensivos/course/list/'

class IntensivoUpdateView(UpdateView):
    model=Intensivo  
    template_name='intensivos/course_form.html'
    form_class = IntensivoForm
    success_url = '/intensivos/course/list/'
