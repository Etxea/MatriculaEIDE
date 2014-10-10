# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Registration.empresa'
        db.delete_column('hobetuz_registration', 'empresa')

        # Deleting field 'Registration.Curso'
        db.delete_column('hobetuz_registration', 'Curso_id')

        # Deleting field 'Registration.postal_code'
        db.delete_column('hobetuz_registration', 'postal_code')

        # Deleting field 'Registration.location'
        db.delete_column('hobetuz_registration', 'location')

        # Deleting field 'Registration.sex'
        db.delete_column('hobetuz_registration', 'sex')

        # Deleting field 'Registration.address'
        db.delete_column('hobetuz_registration', 'address')

        # Deleting field 'Registration.birth_date'
        db.delete_column('hobetuz_registration', 'birth_date')

        # Adding field 'Registration.curso'
        db.add_column('hobetuz_registration', 'curso',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hobetuz.Curso']),
                      keep_default=False)

        # Adding field 'Registration.empresa_nombre'
        db.add_column('hobetuz_registration', 'empresa_nombre',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Registration.empresa_puesto'
        db.add_column('hobetuz_registration', 'empresa_puesto',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Registration.empresa_actividad'
        db.add_column('hobetuz_registration', 'empresa_actividad',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Registration.empresa'
        db.add_column('hobetuz_registration', 'empresa',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Registration.Curso'
        db.add_column('hobetuz_registration', 'Curso',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['hobetuz.Curso']),
                      keep_default=False)

        # Adding field 'Registration.postal_code'
        db.add_column('hobetuz_registration', 'postal_code',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=0),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Registration.location'
        raise RuntimeError("Cannot reverse this migration. 'Registration.location' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Registration.location'
        db.add_column('hobetuz_registration', 'location',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Registration.sex'
        raise RuntimeError("Cannot reverse this migration. 'Registration.sex' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Registration.sex'
        db.add_column('hobetuz_registration', 'sex',
                      self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Registration.address'
        raise RuntimeError("Cannot reverse this migration. 'Registration.address' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Registration.address'
        db.add_column('hobetuz_registration', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Registration.birth_date'
        raise RuntimeError("Cannot reverse this migration. 'Registration.birth_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Registration.birth_date'
        db.add_column('hobetuz_registration', 'birth_date',
                      self.gf('django.db.models.fields.DateField')(),
                      keep_default=False)

        # Deleting field 'Registration.curso'
        db.delete_column('hobetuz_registration', 'curso_id')

        # Deleting field 'Registration.empresa_nombre'
        db.delete_column('hobetuz_registration', 'empresa_nombre')

        # Deleting field 'Registration.empresa_puesto'
        db.delete_column('hobetuz_registration', 'empresa_puesto')

        # Deleting field 'Registration.empresa_actividad'
        db.delete_column('hobetuz_registration', 'empresa_actividad')


    models = {
        'hobetuz.curso': {
            'Meta': {'object_name': 'Curso'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula_abierta': ('django.db.models.fields.BooleanField', [], {'default': 'datetime.date.today'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'hobetuz.registration': {
            'Meta': {'object_name': 'Registration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hobetuz.Curso']"}),
            'desempleado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'empresa_actividad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'empresa_nombre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'empresa_puesto': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fecha_desempleo': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now_add': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'titulacion': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'})
        }
    }

    complete_apps = ['hobetuz']