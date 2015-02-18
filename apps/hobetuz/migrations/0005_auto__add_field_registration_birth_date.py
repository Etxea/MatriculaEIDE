# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Registration.birth_date'
        db.add_column('hobetuz_registration', 'birth_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 2, 18, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Registration.birth_date'
        db.delete_column('hobetuz_registration', 'birth_date')


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
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hobetuz.Curso']"}),
            'curso2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registration2_set'", 'null': 'True', 'to': "orm['hobetuz.Curso']"}),
            'curso3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registration3_set'", 'null': 'True', 'to': "orm['hobetuz.Curso']"}),
            'curso4': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registration4_set'", 'null': 'True', 'to': "orm['hobetuz.Curso']"}),
            'curso5': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registration5_set'", 'null': 'True', 'to': "orm['hobetuz.Curso']"}),
            'desempleado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'empresa_actividad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'empresa_nombre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'empresa_puesto': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fecha_desempleo': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nivel_aleman': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '1', 'decimal_places': '0', 'blank': 'True'}),
            'nivel_chino': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '1', 'decimal_places': '0', 'blank': 'True'}),
            'nivel_frances': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '1', 'decimal_places': '0', 'blank': 'True'}),
            'nivel_ingles': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '1', 'decimal_places': '0', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now_add': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'titulacion': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'})
        }
    }

    complete_apps = ['hobetuz']