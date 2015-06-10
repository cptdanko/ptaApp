# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table('pta_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('pta', ['Role'])

        # Adding model 'Staff'
        db.create_table('pta_staff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mob_no', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('adress', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pta.Role'])),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('pta', ['Staff'])

        # Adding model 'Language'
        db.create_table('pta_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('pta', ['Language'])

        # Adding model 'Patient'
        db.create_table('pta_patient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('original_address', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('bed_no', self.gf('django.db.models.fields.IntegerField')()),
            ('ward_no', self.gf('django.db.models.fields.IntegerField')()),
            ('pta_cleared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pta.Language'])),
        ))
        db.send_create_signal('pta', ['Patient'])

        # Adding model 'Question'
        db.create_table('pta_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('pta', ['Question'])

        # Adding model 'Answer'
        db.create_table('pta_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pta.Question'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('isAnswerRight', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pta', ['Answer'])

        # Adding model 'PatientResponses'
        db.create_table('pta_patientresponses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pta.Patient'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answerStatus', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pta.Question'])),
        ))
        db.send_create_signal('pta', ['PatientResponses'])

        # Adding model 'PTAQuestionaire'
        db.create_table('pta_ptaquestionaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pta.Patient'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('correctAnswers', self.gf('django.db.models.fields.IntegerField')()),
            ('totalQuestions', self.gf('django.db.models.fields.IntegerField')()),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('pta', ['PTAQuestionaire'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table('pta_role')

        # Deleting model 'Staff'
        db.delete_table('pta_staff')

        # Deleting model 'Language'
        db.delete_table('pta_language')

        # Deleting model 'Patient'
        db.delete_table('pta_patient')

        # Deleting model 'Question'
        db.delete_table('pta_question')

        # Deleting model 'Answer'
        db.delete_table('pta_answer')

        # Deleting model 'PatientResponses'
        db.delete_table('pta_patientresponses')

        # Deleting model 'PTAQuestionaire'
        db.delete_table('pta_ptaquestionaire')


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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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
        'pta.answer': {
            'Meta': {'object_name': 'Answer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isAnswerRight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pta.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pta.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'pta.patient': {
            'Meta': {'object_name': 'Patient'},
            'bed_no': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pta.Language']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'original_address': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'pta_cleared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ward_no': ('django.db.models.fields.IntegerField', [], {})
        },
        'pta.patientresponses': {
            'Meta': {'object_name': 'PatientResponses'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'answerStatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pta.Patient']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pta.Question']"})
        },
        'pta.ptaquestionaire': {
            'Meta': {'object_name': 'PTAQuestionaire'},
            'correctAnswers': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pta.Patient']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'totalQuestions': ('django.db.models.fields.IntegerField', [], {})
        },
        'pta.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'pta.role': {
            'Meta': {'object_name': 'Role'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pta.staff': {
            'Meta': {'object_name': 'Staff'},
            'adress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mob_no': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pta.Role']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['pta']