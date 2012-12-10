# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Valores.fecha'
        db.delete_column('sensors_valores', 'fecha')

        # Adding field 'Valores.timestamp'
        db.add_column('sensors_valores', 'timestamp',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Valores.fecha'
        db.add_column('sensors_valores', 'fecha',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 9, 0, 0)),
                      keep_default=False)

        # Deleting field 'Valores.timestamp'
        db.delete_column('sensors_valores', 'timestamp')


    models = {
        'sensors.valores': {
            'Meta': {'object_name': 'Valores'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor_id': ('django.db.models.fields.IntegerField', [], {}),
            'sensor_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {}),
            'ubiid': ('django.db.models.fields.IntegerField', [], {}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['sensors']