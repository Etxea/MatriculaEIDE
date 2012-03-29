# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ComputerBasedRegistration.born_date'
        db.delete_column('cambridge_computerbasedregistration', 'born_date')

        # Adding field 'ComputerBasedRegistration.birth_date'
        db.add_column('cambridge_computerbasedregistration', 'birth_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 29)), keep_default=False)

        # Deleting field 'SchoolRegistration.born_date'
        db.delete_column('cambridge_schoolregistration', 'born_date')

        # Adding field 'SchoolRegistration.birth_date'
        db.add_column('cambridge_schoolregistration', 'birth_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 29)), keep_default=False)

        # Deleting field 'Registration.born_date'
        db.delete_column('cambridge_registration', 'born_date')

        # Adding field 'Registration.birth_date'
        db.add_column('cambridge_registration', 'birth_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 29)), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'ComputerBasedRegistration.born_date'
        db.add_column('cambridge_computerbasedregistration', 'born_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 29)), keep_default=False)

        # Deleting field 'ComputerBasedRegistration.birth_date'
        db.delete_column('cambridge_computerbasedregistration', 'birth_date')

        # Adding field 'SchoolRegistration.born_date'
        db.add_column('cambridge_schoolregistration', 'born_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 29)), keep_default=False)

        # Deleting field 'SchoolRegistration.birth_date'
        db.delete_column('cambridge_schoolregistration', 'birth_date')

        # Adding field 'Registration.born_date'
        db.add_column('cambridge_registration', 'born_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 29)), keep_default=False)

        # Deleting field 'Registration.birth_date'
        db.delete_column('cambridge_registration', 'birth_date')


    models = {
        'cambridge.computerbasedexam': {
            'Meta': {'object_name': 'ComputerBasedExam'},
            'exam_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_date': ('django.db.models.fields.DateField', [], {}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cambridge.computerbasedregistration': {
            'Meta': {'object_name': 'ComputerBasedRegistration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'eide_alumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.ComputerBasedExam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'cambridge.exam': {
            'Meta': {'object_name': 'Exam'},
            'exam_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_date': ('django.db.models.fields.DateField', [], {}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cambridge.level': {
            'Meta': {'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'cambridge.registration': {
            'Meta': {'object_name': 'Registration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'eide_alumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Exam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'cambridge.schoolexam': {
            'Meta': {'object_name': 'SchoolExam'},
            'exam_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_date': ('django.db.models.fields.DateField', [], {}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cambridge.schoolregistration': {
            'Meta': {'object_name': 'SchoolRegistration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'eide_alumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.SchoolExam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['cambridge']
