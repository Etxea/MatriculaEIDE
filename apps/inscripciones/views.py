# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View, DeleteView
from django.views.generic.edit import ModelFormMixin

from models import *
from forms import *

class RegistrationDetailView(DetailView):
    model=Registration
    template_name='inscripciones/detalle.html'

class RegistrationDeleteView(DeleteView):
    model=Registration
    success_url = '/inscripciones/list/'

class RegistrationUpdateView(UpdateView):
    model=Registration  
    success_url = '/inscripciones/list/'

class RegistrationPayment(DetailView):
    model=Registration
    template_name='inscripciones/payment.html'
    
class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    #~ fields = "__all__"
    #~ exclude = ["paid", "registration_date"]
    template_name='inscripciones/registration_form.html'
    #~ def get_context_data(self, **kwargs):
        #~ context = super(RegistrationCreateView, self).get_context_data(**kwargs)
        #~ context['lista_inscripciones'] = Intensivo.objects.all()
        #~ return context
        
    def get_success_url(self):
        return '/inscripciones/thanks/'
    #~ def form_valid(self, form):
        #~ self.object = form.save(commit=False)
        #~ self.object.save()    
        #~ self.object.password = ''.join([choice(letters) for i in xrange(6)])
        #~ for intensivo in form.cleaned_data['inscripciones']:
            #~ print "Abadimos intensivo",intensivo
            #~ self.object.inscripciones.add(intensivo)
        
        #~ self.object.send_confirmation_email()
        #~ return super(ModelFormMixin, self).form_valid(form)

def RegistrationExcelView(request):
    objs = Registration.objects.all()
    return ExcelResponse(objs)

class RegistrationListView(ListView):
    model = Registration
    template_name='inscripciones/lista.html'

