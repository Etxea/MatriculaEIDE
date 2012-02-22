from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.views.generic.simple import direct_to_template
from views import *
from forms import *
from models import Matricula


matricula_info = {
    'model' :   Matricula,
    'post_save_redirect': '/matricula/gracias',
}

matricula_list_info = {
    'queryset' :   Matricula.objects.all(),
    "template_name": 'matricula/lista.html',
    'allow_empty': True,
}
matricula_detail_info = {
    "queryset" : Matricula.objects.all(),
    "template_name": 'matricula/detalle.html',
    "template_object_name" : "matricula",
}

info_dict = {
    'queryset': Matricula.objects.all(),
}
urlpatterns = patterns('matricula/',
    url(r'detalle/(?P<object_id>\d+)/$', list_detail.object_detail, matricula_detail_info, name="matricula_detalle"),
    url(r'nueva$', create_update.create_object, matricula_info, name="matricula_nueva" ),
    url(r'lista$',list_detail.object_list, matricula_list_info, name="matricula_lista"),
    url(r'gracias$', direct_to_template, {'template': 'matricula/gracias.html' },name="matricula_gracias"),
    url(r'/?$', direct_to_template, {'template': 'matricula/index.html' },name="matricula"),
)
