# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View
from django.views.generic.edit import ModelFormMixin

from models import *
from forms import *


class RegistrationDetailView(DetailView):
	model=Registration
	template_name='intesivos/detalle.html'

class RegistrationDeleteView(DeleteView):
	model=Registration
	

class RegistrationPayment(DetailView):
	model=Registration
	template_name='intesivos/payment.html'

	
class RegistrationCreateView(CreateView):
	model = Registration
	form_class = RegistrationForm
	template_name='registration_form.html'
	def get_success_url(self):
		return self.object.generate_payment_url()

def RegistrationExcelView(request):
    objs = Registration.objects.all()
    return ExcelResponse(objs)

class RegistrationListView(ListView):
	model = Registration
	template_name='espanol/list.html'
