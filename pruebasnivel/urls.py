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

from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', ReservationHome.as_view(), name="pruebasnivel_home"),
    url(r'^thanks/$', ReservationThanks.as_view(), name="pruebasnivel_thanks"),
    url(r'^reservas/(?P<venue>\d+)/(?P<year>\d+)/(?P<month>\d+)/$',OccupationView.as_view(),name="pruebasnivel_occupation"),
    url(r'^reservar/(?P<venue>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$',ReservationCreateView.as_view(),name="pruebasnivel_reservar"),
    url(r'^disponibilidad/(?P<venue>\d+)/$',AvailiabilityView.as_view(),name="pruebasnivel_disponibilidad"),
    url(r'^disponibilidad/(?P<venue>\d+)/(?P<day>\d+)/(?P<hour>\d+)/add/$',AvailiabilityCreate.as_view(),name="pruebasnivel_disponibilidad_nueva"),
    url(r'^disponibilidad/(?P<pk>\d+)/delete/$',AvailiabilityDelete.as_view(),name="pruebasnivel_disponibilidad_borrar"),
    url(r'^disponibilidad/(?P<pk>\d+)/$',AvailiabilityUpdate.as_view(),name="pruebasnivel_disponibilidad_editar"),
]