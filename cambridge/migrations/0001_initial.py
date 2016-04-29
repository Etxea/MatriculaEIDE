# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Level'
        db.create_table('cambridge_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('cambridge', ['Level'])

        # Adding model 'Exam'
        db.create_table('cambridge_exam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exam_type', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Level'])),
            ('exam_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('registration_end_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('cambridge', ['Exam'])

        # Adding model 'School'
        db.create_table('cambridge_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cambridge', ['School'])

        # Adding model 'Venue'
        db.create_table('cambridge_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cambridge', ['Venue'])

        # Adding model 'SchoolLevel'
        db.create_table('cambridge_schoollevel', (
            ('level_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cambridge.Level'], unique=True, primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.School'])),
        ))
        db.send_create_signal('cambridge', ['SchoolLevel'])

        # Adding model 'SchoolExam'
        db.create_table('cambridge_schoolexam', (
            ('exam_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cambridge.Exam'], unique=True, primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.School'])),
        ))
        db.send_create_signal('cambridge', ['SchoolExam'])

        # Adding model 'VenueExam'
        db.create_table('cambridge_venueexam', (
            ('exam_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cambridge.Exam'], unique=True, primary_key=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Venue'])),
        ))
        db.send_create_signal('cambridge', ['VenueExam'])

        # Adding model 'Registration'
        db.create_table('cambridge_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Exam'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=0)),
            ('sex', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('eide_alumn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('centre_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, auto_now_add=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_conditions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('accept_photo_conditions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('minor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tutor_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('tutor_surname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('cambridge', ['Registration'])


    def backwards(self, orm):
        # Deleting model 'Level'
        db.delete_table('cambridge_level')

        # Deleting model 'Exam'
        db.delete_table('cambridge_exam')

        # Deleting model 'School'
        db.delete_table('cambridge_school')

        # Deleting model 'Venue'
        db.delete_table('cambridge_venue')

        # Deleting model 'SchoolLevel'
        db.delete_table('cambridge_schoollevel')

        # Deleting model 'SchoolExam'
        db.delete_table('cambridge_schoolexam')

        # Deleting model 'VenueExam'
        db.delete_table('cambridge_venueexam')

        # Deleting model 'Registration'
        db.delete_table('cambridge_registration')


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