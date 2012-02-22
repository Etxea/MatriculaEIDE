from django.db import models
from django.contrib.localflavor import generic

# Create your models here.

SEXO = (
    (1, 'Hombre'),
    (2, 'Mujer'),
)


class Matricula(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    sexo = models.DecimalField(max_digits=1, decimal_places=0,choices=SEXO)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    num_dni = models.CharField(max_length=9)
    estado_civil = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
