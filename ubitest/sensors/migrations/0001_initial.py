# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Valores'
        db.create_table('sensors_valores', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor_id', self.gf('django.db.models.fields.IntegerField')()),
            ('sensor_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ubiid', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')()),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('sensors', ['Valores'])


    def backwards(self, orm):
        # Deleting model 'Valores'
        db.delete_table('sensors_valores')


    models = {
        'sensors.valores': {
            'Meta': {'object_name': 'Valores'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor_id': ('django.db.models.fields.IntegerField', [], {}),
            'sensor_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ubiid': ('django.db.models.fields.IntegerField', [], {}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['sensors']