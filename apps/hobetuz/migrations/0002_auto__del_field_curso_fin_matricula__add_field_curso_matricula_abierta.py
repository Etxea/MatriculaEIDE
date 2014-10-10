# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Curso.fin_matricula'
        db.delete_column('hobetuz_curso', 'fin_matricula')

        # Adding field 'Curso.matricula_abierta'
        db.add_column('hobetuz_curso', 'matricula_abierta',
                      self.gf('django.db.models.fields.BooleanField')(default=datetime.date.today),
                      keep_default=False)

        # Deleting field 'Registration.accept_photo_conditions'
        db.delete_column('hobetuz_registration', 'accept_photo_conditions')

        # Deleting field 'Registration.centre_name'
        db.delete_column('hobetuz_registration', 'centre_name')

        # Adding field 'Registration.titulacion'
        db.add_column('hobetuz_registration', 'titulacion',
                      self.gf('django.db.models.fields.DecimalField')(default=False, max_digits=1, decimal_places=0),
                      keep_default=False)

        # Adding field 'Registration.fecha_desempleo'
        db.add_column('hobetuz_registration', 'fecha_desempleo',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True),
                      keep_default=False)

        # Adding field 'Registration.empresa'
        db.add_column('hobetuz_registration', 'empresa',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Curso.fin_matricula'
        db.add_column('hobetuz_curso', 'fin_matricula',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today),
                      keep_default=False)

        # Deleting field 'Curso.matricula_abierta'
        db.delete_column('hobetuz_curso', 'matricula_abierta')

        # Adding field 'Registration.accept_photo_conditions'
        db.add_column('hobetuz_registration', 'accept_photo_conditions',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Registration.centre_name'
        db.add_column('hobetuz_registration', 'centre_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Deleting field 'Registration.titulacion'
        db.delete_column('hobetuz_registration', 'titulacion')

        # Deleting field 'Registration.fecha_desempleo'
        db.delete_column('hobetuz_registration', 'fecha_desempleo')

        # Deleting field 'Registration.empresa'
        db.delete_column('hobetuz_registration', 'empresa')


    models = {
        'hobetuz.curso': {
            'Meta': {'object_name': 'Curso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula_abierta': ('django.db.models.fields.BooleanField', [], {'default': 'datetime.date.today'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'hobetuz.registration': {
            'Curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hobetuz.Curso']"}),
            'Meta': {'object_name': 'Registration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'desempleado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'empresa': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fecha_desempleo': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now_add': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'titulacion': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'})
        }
    }

    complete_apps = ['hobetuz']