# encoding: utf-8
import datetime
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
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Level'])),
            ('exam_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('registration_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('cambridge', ['Exam'])

        # Adding model 'SchoolExam'
        db.create_table('cambridge_schoolexam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Level'])),
            ('exam_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('registration_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('cambridge', ['SchoolExam'])

        # Adding model 'ComputerBasedExam'
        db.create_table('cambridge_computerbasedexam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Level'])),
            ('exam_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('registration_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('cambridge', ['ComputerBasedExam'])

        # Adding model 'Registration'
        db.create_table('cambridge_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=0)),
            ('sex', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('dni', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('eide_alumn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('centre_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, auto_now_add=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_conditions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_photo_conditions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('minor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tutor_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('tutor_surname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('exam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.Exam'])),
        ))
        db.send_create_signal('cambridge', ['Registration'])

        # Adding model 'SchoolRegistration'
        db.create_table('cambridge_schoolregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=0)),
            ('sex', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('dni', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('eide_alumn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('centre_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, auto_now_add=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_conditions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_photo_conditions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('minor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tutor_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('tutor_surname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('exam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.SchoolExam'])),
        ))
        db.send_create_signal('cambridge', ['SchoolRegistration'])

        # Adding model 'ComputerBasedRegistration'
        db.create_table('cambridge_computerbasedregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=0)),
            ('sex', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('dni', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('eide_alumn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('centre_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, auto_now_add=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_conditions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accept_photo_conditions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('minor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tutor_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('tutor_surname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('exam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cambridge.ComputerBasedExam'])),
        ))
        db.send_create_signal('cambridge', ['ComputerBasedRegistration'])


    def backwards(self, orm):
        
        # Deleting model 'Level'
        db.delete_table('cambridge_level')

        # Deleting model 'Exam'
        db.delete_table('cambridge_exam')

        # Deleting model 'SchoolExam'
        db.delete_table('cambridge_schoolexam')

        # Deleting model 'ComputerBasedExam'
        db.delete_table('cambridge_computerbasedexam')

        # Deleting model 'Registration'
        db.delete_table('cambridge_registration')

        # Deleting model 'SchoolRegistration'
        db.delete_table('cambridge_schoolregistration')

        # Deleting model 'ComputerBasedRegistration'
        db.delete_table('cambridge_computerbasedregistration')


    models = {
        'cambridge.computerbasedexam': {
            'Meta': {'object_name': 'ComputerBasedExam'},
            'exam_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        'cambridge.computerbasedregistration': {
            'Meta': {'object_name': 'ComputerBasedRegistration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accept_photo_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'eide_alumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.ComputerBasedExam']"}),
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
        'cambridge.exam': {
            'Meta': {'object_name': 'Exam'},
            'exam_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
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
            'accept_photo_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
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
        'cambridge.schoolexam': {
            'Meta': {'object_name': 'SchoolExam'},
            'exam_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.Level']"}),
            'registration_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'})
        },
        'cambridge.schoolregistration': {
            'Meta': {'object_name': 'SchoolRegistration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accept_photo_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'eide_alumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cambridge.SchoolExam']"}),
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
        }
    }

    complete_apps = ['cambridge']
