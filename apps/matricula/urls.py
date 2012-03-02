from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView

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

    url(r'detalle/(?P<pk>\d+)$',
        login_required(UpdateView.as_view(
            model=Matricula,
            template_name='matricula/matricula_edit.html')), name="matricula_detalle"),

    url(r'imprimir/(?P<pk>\d+)$', imprimir_matricula, name="matricula_imprimir"),
    url(r'nueva$',
        CreateView.as_view(
            model=Matricula,
            template_name='matricula/matricula_form.html'), name="matricula_nueva"),
    url(r'lista$',list_detail.object_list, matricula_list_info, name="matricula_lista"),
    url(r'gracias$', direct_to_template, {'template': 'matricula/gracias.html' },name="matricula_gracias"),
    url(r'/?$', direct_to_template, {'template': 'matricula/index.html' },name="matricula"),
)
