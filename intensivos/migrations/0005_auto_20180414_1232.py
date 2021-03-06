# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-04-14 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intensivos', '0004_auto_20171215_0729'),
    ]

    operations = [
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
            model_name='intensivo',
            name='venue',
            field=models.CharField(default=b'EIDE', max_length=50, verbose_name='Lugar de impartici\xf3n'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Direcci\xf3n'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='birth_date',
            field=models.DateField(help_text='Formato: AAAA-MM-DD(a\xf1o-mes-d\xeda)', verbose_name='Fecha NAc.'),
        ),
    ]
