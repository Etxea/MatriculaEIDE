# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-29 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intensivos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intensivo',
            name='nivel',
        ),
        migrations.AlterField(
            model_name='intensivo',
            name='fin',
            field=models.DateField(help_text='Formato: AAAA-MM-DD(a\xf1o-mes-d\xeda)', verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='intensivo',
            name='inicio',
            field=models.DateField(help_text='Formato: AAAA-MM-DD(a\xf1o-mes-d\xeda)', verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='birth_date',
            field=models.DateField(help_text='Formato: AAAA-MM-DD(a\xf1o-mes-d\xeda)', verbose_name='Birth Date'),
        ),
    ]