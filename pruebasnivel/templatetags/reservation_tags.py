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
from pruebasnivel.models import *

register = template.Library()

@register.simple_tag(name="venue_availiable")
def venue_availiable(venue, week_day, hour, *args, **kwargs):
    ava = Availability.objects.filter(venue=int(venue),weekday=int(week_day),hour=int(hour))
    if len(ava) == 0:
        return False
    else:
        return True

@register.simple_tag(name="venue_availiability_id")
def venue_availiability_id(venue, week_day, hour, *args, **kwargs):
    ava = Availability.objects.get(venue=int(venue), weekday=int(week_day), hour=int(hour))
    return ava.pk