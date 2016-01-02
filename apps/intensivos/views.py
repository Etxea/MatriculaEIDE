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

class RegistrationPayment(DetailView):
	model=Registration
	template_name='intensivos/payment.html'
	
class RegistrationCreateView(CreateView):
	model = Registration
	form_class = RegistrationForm
	template_name='intensivos/registration_form.html'
	def get_success_url(self):
		return '/intensivos/thanks/'

def RegistrationExcelView(request):
    objs = Registration.objects.all()
    return ExcelResponse(objs)

class RegistrationListView(ListView):
	model = Registration
	template_name='intensivos/lista.html'
