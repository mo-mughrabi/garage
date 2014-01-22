# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModelLookup'
        db.create_table('vehicle_modellookup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('trim', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='S', max_length=1, db_index=True)),
            ('body_style', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_position', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_cylinders', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_power_ps', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_power_rpm', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_torque_nm', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_torque_rpm', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('engine_fuel', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('top_speed_kph', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('drive', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('transmission_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('seats', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('doors', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicle_modellookup_create', null=True, to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicle_modellookup_update', null=True, to=orm['auth.User'])),
            ('approved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicle_modellookup_approve', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('vehicle', ['ModelLookup'])

        # Adding unique constraint on 'ModelLookup', fields ['make', 'model', 'trim', 'year']
        db.create_unique('vehicle_modellookup', ['make', 'model', 'trim', 'year'])

        # Adding model 'ModelLookUpI18n'
        db.create_table('vehicle_modellookup_i18n', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vehicle.ModelLookup'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('make_display', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model_display', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('trim_display', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('vehicle', ['ModelLookUpI18n'])

        # Adding unique constraint on 'ModelLookUpI18n', fields ['model', 'language']
        db.create_unique('vehicle_modellookup_i18n', ['model_id', 'language'])

        # Adding model 'LookupTranslation'
        db.create_table('vehicle_lookup_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['vehicle.Lookup'])),
        ))
        db.send_create_signal('vehicle', ['LookupTranslation'])

        # Adding unique constraint on 'LookupTranslation', fields ['language_code', 'master']
        db.create_unique('vehicle_lookup_translation', ['language_code', 'master_id'])

        # Adding model 'Lookup'
        db.create_table('vehicle_lookup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('vehicle', ['Lookup'])

        # Adding unique constraint on 'Lookup', fields ['key', 'group']
        db.create_unique('vehicle_lookup', ['key', 'group'])

        # Adding model 'Car'
        db.create_table('vehicle_car', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vehicle.ModelLookup'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('primary_image', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='is_primary', unique=True, null=True, to=orm['vehicle.Image'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vehicle.Lookup'], null=True, blank=True)),
            ('mileage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('condition', self.gf('django.db.models.fields.CharField')(default='N', max_length=30)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('for_sale', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('view_count', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('asking_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=3)),
            ('sold_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('sold_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vehicle_car_create', to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicle_car_update', null=True, to=orm['auth.User'])),
            ('approved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicle_car_approve', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('vehicle', ['Car'])

        # Adding model 'Image'
        db.create_table('vehicle_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vehicle.Car'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='vehicle_image_create', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('vehicle', ['Image'])


    def backwards(self, orm):
        # Removing unique constraint on 'Lookup', fields ['key', 'group']
        db.delete_unique('vehicle_lookup', ['key', 'group'])

        # Removing unique constraint on 'LookupTranslation', fields ['language_code', 'master']
        db.delete_unique('vehicle_lookup_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'ModelLookUpI18n', fields ['model', 'language']
        db.delete_unique('vehicle_modellookup_i18n', ['model_id', 'language'])

        # Removing unique constraint on 'ModelLookup', fields ['make', 'model', 'trim', 'year']
        db.delete_unique('vehicle_modellookup', ['make', 'model', 'trim', 'year'])

        # Deleting model 'ModelLookup'
        db.delete_table('vehicle_modellookup')

        # Deleting model 'ModelLookUpI18n'
        db.delete_table('vehicle_modellookup_i18n')

        # Deleting model 'LookupTranslation'
        db.delete_table('vehicle_lookup_translation')

        # Deleting model 'Lookup'
        db.delete_table('vehicle_lookup')

        # Deleting model 'Car'
        db.delete_table('vehicle_car')

        # Deleting model 'Image'
        db.delete_table('vehicle_image')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vehicle.car': {
            'Meta': {'object_name': 'Car'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicle_car_approve'", 'null': 'True', 'to': "orm['auth.User']"}),
            'asking_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '3'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicle.Lookup']", 'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '30'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vehicle_car_create'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'for_sale': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mileage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicle.ModelLookup']"}),
            'primary_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'is_primary'", 'unique': 'True', 'null': 'True', 'to': "orm['vehicle.Image']"}),
            'sold_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sold_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicle_car_update'", 'null': 'True', 'to': "orm['auth.User']"}),
            'view_count': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'vehicle.image': {
            'Meta': {'object_name': 'Image'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicle.Car']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicle_image_create'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'vehicle.lookup': {
            'Meta': {'unique_together': "(('key', 'group'),)", 'object_name': 'Lookup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'vehicle.lookuptranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'LookupTranslation', 'db_table': "'vehicle_lookup_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['vehicle.Lookup']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'vehicle.modellookup': {
            'Meta': {'unique_together': "(('make', 'model', 'trim', 'year'),)", 'object_name': 'ModelLookup'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicle_modellookup_approve'", 'null': 'True', 'to': "orm['auth.User']"}),
            'body_style': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicle_modellookup_create'", 'null': 'True', 'to': "orm['auth.User']"}),
            'doors': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'drive': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_cylinders': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_fuel': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_position': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_power_ps': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_power_rpm': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_torque_nm': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_torque_rpm': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'engine_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'seats': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1', 'db_index': 'True'}),
            'top_speed_kph': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'transmission_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'trim': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vehicle_modellookup_update'", 'null': 'True', 'to': "orm['auth.User']"}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'vehicle.modellookupi18n': {
            'Meta': {'unique_together': "(('model', 'language'),)", 'object_name': 'ModelLookUpI18n', 'db_table': "'vehicle_modellookup_i18n'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'make_display': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vehicle.ModelLookup']"}),
            'model_display': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trim_display': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['vehicle']