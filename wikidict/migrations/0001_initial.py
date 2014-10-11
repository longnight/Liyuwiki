# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Terms'
        db.create_table(u'wikidict_terms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, blank=True)),
            ('term_pinyin', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'wikidict', ['Terms'])

        # Adding model 'Definitions'
        db.create_table(u'wikidict_definitions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Terms', self.gf('django.db.models.fields.related.ForeignKey')(related_name='term_definitions', to=orm['wikidict.Terms'])),
            ('definition', self.gf('django.db.models.fields.TextField')(max_length=150)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(default='anonymous', max_length=65)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('author_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('vote_rank', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('vote_rank2', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, blank=True)),
        ))
        db.send_create_signal(u'wikidict', ['Definitions'])


    def backwards(self, orm):
        # Deleting model 'Terms'
        db.delete_table(u'wikidict_terms')

        # Deleting model 'Definitions'
        db.delete_table(u'wikidict_definitions')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'secretballot.vote': {
            'Meta': {'unique_together': "(('token', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'wikidict.definitions': {
            'Meta': {'object_name': 'Definitions'},
            'Terms': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'term_definitions'", 'to': u"orm['wikidict.Terms']"}),
            'author': ('django.db.models.fields.CharField', [], {'default': "'anonymous'", 'max_length': '65'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'max_length': '150'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'}),
            'vote_rank': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'vote_rank2': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'wikidict.terms': {
            'Meta': {'object_name': 'Terms'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'term_pinyin': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wikidict']