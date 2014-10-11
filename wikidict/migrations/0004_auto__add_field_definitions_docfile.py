# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Definitions.docfile'
        db.add_column(u'wikidict_definitions', 'docfile',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Definitions.docfile'
        db.delete_column(u'wikidict_definitions', 'docfile')


    models = {
        u'wikidict.definitions': {
            'Meta': {'object_name': 'Definitions'},
            'Terms': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms_definitions'", 'to': u"orm['wikidict.Terms']"}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '65', 'blank': 'True'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'docfile': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'}),
            'vote_rank': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'vote_rank2': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'wikidict.terms': {
            'Meta': {'object_name': 'Terms'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'default': "'1984-06-04'"}),
            'term': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'term_pinyin': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'}),
            'visit_times': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['wikidict']