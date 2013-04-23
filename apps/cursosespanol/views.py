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
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View
from django.views.generic.edit import ModelFormMixin

from models import *
from forms import *


class RegistrationView(DetailView):
	model=Registration
	template_name='espanol/view.html'

class RegistrationPayment(DetailView):
	model=Registration
	template_name='espanol/payment.html'

	
class RegistrationCreateView(CreateView):
	model = Registration
	form_class = RegistrationForm
	template_name='registration_form.html'
	def get_success_url(self):
		return '/espanol/pay/%d'%self.object.id
#		#Comprobamos si el pago es por txartela:
#		if True:
#			return self.object.generate_payment_url()
#		else:
#			## FIXME usar un reverse o lazy_reverse
#			return '/cambridge/thanks/'

@login_required	
def RegistrationExcelView(request):
    objs = Registration.objects.all()
    return ExcelResponse(objs)

class RegistrationListView(ListView):
	#model=ComputerBasedRegistration
	template_name='espanol/list.html'
