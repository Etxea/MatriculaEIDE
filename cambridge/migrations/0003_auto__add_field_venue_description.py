# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Venue.description'
        db.add_column('cambridge_venue', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Venue.description'
        db.delete_column('cambridge_venue', 'description')


    models = {
        'cambridge.exam': {
            'Meta': {'object_name': 'Exam'},
            'exam_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'exam_type': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        'cambridge.level': {
            'Meta': {'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'cambridge.registration': {
            'Meta': {'object_name': 'Registration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'accept_photo_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'eide_alumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Exam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'minor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now_add': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'tutor_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'tutor_surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'cambridge.school': {
            'Meta': {'object_name': 'School'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cambridge.schoolexam': {
            'Meta': {'object_name': 'SchoolExam', '_ormbases': ['cambridge.Exam']},
            'exam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cambridge.Exam']", 'unique': 'True', 'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.School']"})
        },
        'cambridge.schoollevel': {
            'Meta': {'object_name': 'SchoolLevel', '_ormbases': ['cambridge.Level']},
            'level_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cambridge.Level']", 'unique': 'True', 'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.School']"})
        },
        'cambridge.venue': {
            'Meta': {'object_name': 'Venue'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cambridge.venueexam': {
            'Meta': {'object_name': 'VenueExam', '_ormbases': ['cambridge.Exam']},
            'exam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cambridge.Exam']", 'unique': 'True', 'primary_key': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Venue']"})
        }
    }

    complete_apps = ['cambridge']