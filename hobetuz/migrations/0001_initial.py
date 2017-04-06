# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-28 22:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('matricula_abierta', models.BooleanField(default=datetime.date.today, verbose_name='Matricula Abierta')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, editable=False, max_length=6, verbose_name='Password')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre (*)')),
                ('surname', models.CharField(max_length=100, verbose_name='Apellido(s) (*)')),
                ('birth_date', models.DateField(help_text='Formato: AAAA-MM-DD(a\xf1o-mes-d\xeda)', verbose_name='Birth Date')),
                ('telephone', models.CharField(max_length=12, verbose_name=b'Tel. Fijo (*)')),
                ('telephone2', models.CharField(max_length=12, verbose_name=b'Tel. M\xc3\xb3vil (*)')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email (*)')),
                ('titulacion', models.DecimalField(choices=[(1, 'Sin titulaci\xf3n'), (2, 'Graduado Escolar o ESO'), (3, 'Bachillerato, COU o similar'), (4, 'Grado, Licenciatura o Diplomatura'), (5, 'Certificado de Profesionalidad en Turismo y Hosteler\xeda de Nivel 1'), (6, 'Certificado de Profesionalidad en Turismo y Hosteler\xeda de Nivel 2 o 3'), (7, 'Ciclo Grado Medio, FPI, Certificado de Profesionalidad de Nivel 2 en otra especialidad'), (8, 'Ciclo de Grado Superior, FPII; Certificado de Profesionalidad de Nivel 3 en otra especialidad')], decimal_places=0, max_digits=1, verbose_name='Titulaci\xf3n (*)')),
                ('desempleado', models.BooleanField(help_text='haga click en el check si se encuentra en situaci\xf3n de desempleo', verbose_name='Desempleado')),
                ('fecha_desempleo', models.DateField(blank=True, default=datetime.date.today, help_text='Formato: AAAA-MM-DD(a\xf1o-mes-d\xeda)', null=True)),
                ('empresa_nombre', models.CharField(blank=True, max_length=100, verbose_name='Nombre de la empresa')),
                ('empresa_puesto', models.CharField(blank=True, max_length=100, verbose_name='Puesto en la empresa')),
                ('empresa_actividad', models.CharField(blank=True, max_length=200, verbose_name='Actividad de la empresa')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('nivel_ingles', models.DecimalField(blank=True, choices=[(1, 'Cero'), (2, 'Inicial'), (3, 'Intermedio'), (4, 'Avanzado')], decimal_places=0, help_text=b'En caso de que haya escogido este idioma indique su nivel', max_digits=1, null=True, verbose_name='Nivel Ingles')),
                ('nivel_frances', models.DecimalField(blank=True, choices=[(1, 'Cero'), (2, 'Inicial'), (3, 'Intermedio'), (4, 'Avanzado')], decimal_places=0, help_text=b'En caso de que haya escogido este idioma indique su nivel', max_digits=1, null=True, verbose_name='Nivel Frances')),
                ('nivel_aleman', models.DecimalField(blank=True, choices=[(1, 'Cero'), (2, 'Inicial'), (3, 'Intermedio'), (4, 'Avanzado')], decimal_places=0, help_text=b'En caso de que haya escogido este idioma indique su nivel', max_digits=1, null=True, verbose_name='Nivel Aleman')),
                ('nivel_chino', models.DecimalField(blank=True, choices=[(1, 'Cero'), (2, 'Inicial'), (3, 'Intermedio'), (4, 'Avanzado')], decimal_places=0, help_text=b'En caso de que haya escogido este idioma indique su nivel', max_digits=1, null=True, verbose_name='Nivel Chino')),
                ('accept_conditions', models.BooleanField(default=True, help_text='You must accept the conditions to register', verbose_name='Accept the conditions')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hobetuz.Curso', verbose_name=b'Primera Opci\xc3\xb3n (*)')),
                ('curso2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration2_set', to='hobetuz.Curso', verbose_name=b'Segunda Opci\xc3\xb3n')),
                ('curso3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration3_set', to='hobetuz.Curso', verbose_name=b'Tercera Opci\xc3\xb3n')),
                ('curso4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration4_set', to='hobetuz.Curso', verbose_name=b'Cuarta Opci\xc3\xb3n')),
                ('curso5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration5_set', to='hobetuz.Curso', verbose_name=b'Quinta Opci\xc3\xb3n')),
            ],
        ),
    ]