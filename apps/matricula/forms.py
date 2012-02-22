from django import forms
from django.forms import ModelForm
from models import *
from django.forms.models import inlineformset_factory

from django.forms.extras.widgets import SelectDateWidget

class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        widgets = {'fecha_nacimiento': SelectDateWidget(),}
