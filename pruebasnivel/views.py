# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View, DeleteView, TemplateView
from django.core.urlresolvers import reverse_lazy
import calendar
from datetime import date
from models import *
from forms import *


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'inscripciones/detalle.html'


class ReservationDeleteView(DeleteView):
    model = Reservation
    success_url = '/inscripciones/list/'


class ReservationUpdateView(UpdateView):
    model = Reservation
    success_url = '/inscripciones/list/'


class ReservationPayment(DetailView):
    model = Reservation
    template_name = 'inscripciones/payment.html'


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'pruebasnivel/reservation_form.html'

    # ~ def get_context_data(self, **kwargs):
    # ~ context = super(ReservationCreateView, self).get_context_data(**kwargs)
    # ~ context['lista_inscripciones'] = Intensivo.objects.all()
    # ~ return context
    def get_initial(self):
        initial = super(ReservationCreateView, self).get_initial()
        initial['venue'] = self.kwargs['venue']
        day = int(self.kwargs['day'])
        month = int(self.kwargs['month'])
        year = int(self.kwargs['year'])
        initial['registration_date'] = date(year,month,day)
        return initial

    def get_success_url(self):
        return '/pruebasdenivel/thanks/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.password = ''.join([choice(letters) for i in xrange(6)])
        self.object.send_confirmation_email()
        return super(ModelFormMixin, self).form_valid(form)

def ReservationExcelView(request):
    objs = Reservation.objects.all()
    return ExcelResponse(objs)


class ReservationListView(ListView):
    model = Reservation
    template_name = 'inscripciones/lista.html'

class ReservationHome(TemplateView):
    template_name="pruebasnivel/home.html"

class ReservationThanks(TemplateView):
    template_name = "pruebasnivel/thanks.html"

class OccupationView(TemplateView):
    template_name = "pruebasnivel/occupation.html"
    def get_context_data(self, **kwargs):
        context = super(OccupationView, self).get_context_data(**kwargs)
        cal = calendar.Calendar()
        venue_id = int(kwargs['venue'])
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        month_cal = cal.monthdayscalendar(year, month)
        context['month_cal'] = month_cal
        context['month'] = month
        context['year'] = year
        context['venue_name'] = "EIDE Ora"
        context['venue_id'] = venue_id
        return context

class AvailiabilityCreate(CreateView):
    template_name = "pruebasnivel/availiability_form.html"
    model = Availability
    fields = ['venue','hour','weekday']
    def get_initial(self):
        initial = super(AvailiabilityCreate, self).get_initial()
        initial['venue'] = self.kwargs['venue']
        initial['weekday'] = int(self.kwargs['day'])
        initial['hour'] = int(self.kwargs['hour'])
        return initial

    def get_success_url(self, **kwargs):
        return reverse_lazy('pruebasnivel_disponibilidad', args=(self.object.venue,))

class AvailiabilityUpdate(UpdateView):
    template_name = "pruebasnivel/availiability_form.html"
    model = Availability

class AvailiabilityDelete(DeleteView):
    template_name = "pruebasnivel/availiability_deleteform.html"
    model = Availability
    def get_success_url(self, **kwargs):
        return reverse_lazy('pruebasnivel_disponibilidad', args=(self.object.venue,))


class AvailiabilityView(ListView):
    model = Availability
    template_name = "pruebasnivel/availiability.html"
    def get_queryset(self):
        venue_id = int(self.kwargs['venue'])
        return Availability.objects.filter(venue=venue_id)
    def get_context_data(self, **kwargs):
        context = super(AvailiabilityView, self).get_context_data(**kwargs)
        venue_id = int(self.kwargs['venue'])
        context['week_days'] = WEEKDAYS
        context['hours'] = HOURS
        context['venue_name'] = VENUES[venue_id][1]
        context['venue_id'] = venue_id
        return context