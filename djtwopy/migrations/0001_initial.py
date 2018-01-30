# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DtThread'
        db.create_table(u'djtwopy_dtthread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('res', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'djtwopy', ['DtThread'])

        # Adding model 'DtComment'
        db.create_table(u'djtwopy_dtcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['djtwopy.DtThread'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('line', self.gf('django.db.models.fields.CharField')(max_length=4096, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('mailaddr', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('datestr', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(max_length=4096, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('be', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('body_html', self.gf('django.db.models.fields.TextField')(max_length=8192, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'djtwopy', ['DtComment'])

        # Adding unique constraint on 'DtComment', fields ['thread', 'number']
        db.create_unique(u'djtwopy_dtcomment', ['thread_id', 'number'])


    def backwards(self, orm):
        # Removing unique constraint on 'DtComment', fields ['thread', 'number']
        db.delete_unique(u'djtwopy_dtcomment', ['thread_id', 'number'])

        # Deleting model 'DtThread'
        db.delete_table(u'djtwopy_dtthread')

        # Deleting model 'DtComment'
        db.delete_table(u'djtwopy_dtcomment')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'djtwopy.dtcomment': {
            'Meta': {'unique_together': "(('thread', 'number'),)", 'object_name': 'DtComment'},
            'be': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'blank': 'True'}),
            'body_html': ('django.db.models.fields.TextField', [], {'max_length': '8192', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'datestr': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'mailaddr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['djtwopy.DtThread']"}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'djtwopy.dtthread': {
            'Meta': {'object_name': 'DtThread'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'res': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['djtwopy']