# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Curso'
        db.create_table('hobetuz_curso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fin_matricula', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('hobetuz', ['Curso'])

        # Adding model 'Registration'
        db.create_table('hobetuz_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hobetuz.Curso'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=0)),
            ('sex', self.gf('django.db.models.fields.DecimalField')(max_digits=1, decimal_places=0)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('telephone2', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('desempleado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('centre_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, auto_now_add=True, blank=True)),
            ('accept_conditions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('accept_photo_conditions', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('hobetuz', ['Registration'])


    def backwards(self, orm):
        # Deleting model 'Curso'
        db.delete_table('hobetuz_curso')

        # Deleting model 'Registration'
        db.delete_table('hobetuz_registration')


    models = {
        'hobetuz.curso': {
            'Meta': {'object_name': 'Curso'},
            'fin_matricula': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'hobetuz.registration': {
            'Curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hobetuz.Curso']"}),
            'Meta': {'object_name': 'Registration'},
            'accept_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'accept_photo_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'centre_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'desempleado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now_add': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.DecimalField', [], {'max_digits': '1', 'decimal_places': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['hobetuz']