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
from django import template
from django.core.urlresolvers import reverse_lazy
from pruebasnivel.models import *
from datetime import date

register = template.Library()

@register.simple_tag(name="venue_availiable")
def venue_availiable(venue, week_day, hour, *args, **kwargs):
    #print "%s %s %s"%(venue,week_day,hour)
    ava = Availability.objects.filter(venue=int(venue),weekday=int(week_day),hour=int(hour))
    if len(ava) == 0:
        return False
    else:
        return True

@register.simple_tag(name="venue_occupation")
def venue_occupation(venue, year, month, day, hour,  *args, **kwargs):
    venue = int(venue)
    year = int(year)
    month = int(month)
    day= int(day)
    hour = int(hour)
    registration_date = date(year, month, day)
    week_day = registration_date.weekday()+1
    if venue_availiable(venue, week_day, hour):
        reservations = Reservation.objects.filter(venue=venue,registration_date=registration_date,hour=hour)
        reseva_url = reverse_lazy('pruebasnivel_reservar',kwargs={'venue':venue,'year':year,'month':month,'day':day,'hour':hour})
        num_reservas=len(reservations)
        libres = 4-num_reservas
        if num_reservas==0:
            return '<a href="%s"><span class="glyphicon glyphicon-plus-sign text-success">%s plazas</span></a>'%(reseva_url,libres)
        elif num_reservas<2:
            return '<a href="%s"><span class="glyphicon glyphicon-plus-sign text-success">%s plazas</span></a>'%(reseva_url,libres)
        elif num_reservas<3:
            return '<a href="%s"><span class="glyphicon glyphicon-plus-sign text-warning">%s plazas</span></a>' %(reseva_url,libres)
        else:
           return '<span class="glyphicon glyphicon-ban-circle text-danger">0 plazas</span>'
    else:
        return '<span class="glyphicon glyphicon-ban-circle danger"></span>'



@register.simple_tag(name="venue_availiability_id")
def venue_availiability_id(venue, week_day, hour, *args, **kwargs):
    ava = Availability.objects.get(venue=int(venue), weekday=int(week_day), hour=int(hour))
    return ava.pk